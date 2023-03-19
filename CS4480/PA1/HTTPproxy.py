# Place your imports here
from datetime import datetime, time
import re
import sys
import signal
from optparse import OptionParser
from socket import *
from urllib.parse import urlparse
import threading


# Signal handler for pressing ctrl-c
def ctrl_c_pressed(signal, frame):
    sys.exit(0)


# TODO: Put function definitions here

def thread_cache():
    """
    Cache the response from the server
    :return:
    """
    lock = threading.Lock()
    cache = {}
    enabled = False

    def resolve(path: str):
        """
        resolve function with thread_cache
        :param path: Path string
        :return: Boolean
        """
        nonlocal enabled, cache
        lock.acquire()
        if path == '/proxy/cache/enable':
            enabled = True
            lock.release()
            return True
        if path == '/proxy/cache/disable':
            enabled = False
            lock.release()
            return True
        if path == '/proxy/cache/flush':
            cache = {}
            lock.release()
            return True
        lock.release()
        return False

    def get_cache(requested_url: str):
        """
        Get the response from the cache
        :param requested_url:
        :return: cached url
        """
        lock.acquire()
        if not enabled:
            lock.release()
            return None

        obj = cache.get(requested_url, None)
        lock.release()
        return obj

    def put_cache(requested_url: str, response: str):
        """
        Put the response in the cache
        :param requested_url: requested_url string
        :param response: response from string
        :return: functions
        """
        lock.acquire()
        if enabled:
            cache[requested_url] = response
        lock.release()

    return resolve, get_cache, put_cache


def block_list():
    """
    Handle everything in block list
    :return:
    """
    blocked = {}
    enabled = False
    lock = threading.Lock()

    def resolve(path: str):
        """
        resolve function with blocklist
        :param path: Path string
        :return: Boolean
        """
        nonlocal enabled, blocked
        lock.acquire()
        if path == '/proxy/blocklist/enable':
            enabled = True
            lock.release()
            return True
        if path == '/proxy/blocklist/disable':
            enabled = False
            lock.release()
            return True
        if path == '/proxy/blocklist/flush':
            blocked = {}
            lock.release()
            return True
        if path.startswith('/proxy/blocklist/add/'):
            blocked[path[21:]] = True
            lock.release()
            return True
        if path.startswith('/proxy/blocklist/remove/'):
            s = path[24:]
            if s in blocked:
                del blocked[s]
            lock.release()
            return True
        lock.release()
        return False

    def handler(url: str):
        """
        handle if blocklist is enabled or not
        :param url: url String
        :return: Boolean
        """
        lock.acquire()
        if not enabled:
            lock.release()
            return True
        for key in blocked:
            if key in url:
                lock.release()
                return False
        lock.release()
        return True

    return resolve, handler


def send_error(error: int, tcp: socket):
    """
    Handle error and close connection
    :param error: All error happen in proxy
    :param tcp: socket get message to client
    :return: void
    """
    msg = ''
    response = ''
    if error == 400:
        msg = "Bad Request"
    elif error == 403:
        msg = "Forbidden"
    elif error == 501:
        msg = "Not Implemented"
    else:
        raise Exception('Invalid error code')
    response = f"HTTP/1.0 {error} {msg}\r\n\r\n"
    try:
        tcp.send(response.encode())
        tcp.close()

    except Exception as e:
        print('error:', e)


def send_ok(tcp: socket):
    """
    Send ok to client
    :param tcp: socket get message to client
    :return: void
    """
    print('sending ok')
    try:
        tcp.send("HTTP/1.0 200 OK\r\n\r\n".encode())
    except Exception as e:
        print(e)


def get_request(tcp: socket, data: str):
    """
    keep receiving data from server
    :param tcp:
    :param data:
    :return:
    """
    try:
        while True:
            if data.endswith('\r\n\r\n'):
                break

            data += tcp.recv(1024).decode()
            print(data)

    except TimeoutError as e:
        print(e)
    return data


def handle_first_line(line: str, hostname: str, path: str, send_port: int, client_tcp: socket):
    """
    handle_first_line of request
    :param line:
    :param hostname:
    :param path:
    :param send_port: the default port to send to
    :param client_tcp:
    :return: hostname, path, send_port
    """
    method = ''
    http_version = ''
    hostname_regex = '^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$'
    split_data = line.split(' ')
    if len(split_data) != 3:
        send_error(400, client_tcp)
        return None

    method = split_data[0]
    url = split_data[1]
    http_version = split_data[2]

    # Make sure the url is valid
    try:
        parsed = urlparse(url)
        if bool(parsed.port):
            send_port = parsed.port
        if parsed.hostname and re.search(hostname_regex, parsed.hostname):
            hostname = parsed.hostname
        if parsed.path is not None:
            path = parsed.path
    except Exception as e:
        print(e)
        send_error(400, client_tcp)
        return None

    if http_version != 'HTTP/1.0':
        send_error(400, client_tcp)
        return None

    # Make sure the url is valid:
    # - hostname is not empty
    # - the path is to set proxy
    if parsed.netloc == '' and not (parsed.path and parsed.path.startswith('/proxy/')):
        send_error(400, client_tcp)
        return None

    if parsed.path is None:
        send_error(400, client_tcp)
        return None

    if parsed.path == '':
        send_error(400, client_tcp)
        return None

    if 'GET' not in method:
        if 'HEAD' not in method or 'POST' not in method:
            send_error(501, client_tcp)  # Not implemented
        else:
            send_error(400, client_tcp)  # Bad request

        return None
    return hostname, path, send_port


# call the cache from thread
cache_resolve, cache_get, cache_put = thread_cache()
block_resolve, block_handler = block_list()


def send_request(headers: list[str], path: str, hostname: str, send_port: int, client_tcp: socket, cached=False):
    """
    Send all decoded message through proxy
    :param headers: Header lines
    :param path: Path to destination
    :param hostname: port hostname
    :param send_port: as name
    :param client_tcp: tcp socket for client
    :param cached: if in cache or not
    :return: status_code, headers, response
    """

    to_server_socket = socket(AF_INET, SOCK_STREAM)
    to_server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    to_server_socket.connect((hostname, send_port))

    # Make sure the format is right
    req = f'GET {path} HTTP/1.0\r\nHost: {hostname}\r\n'
    headers.append('Connection: close')
    for header in headers:
        req += f'{header}\r\n'

    req += '\r\n'  # end of request
    to_server_socket.send(req.encode())
    response = bytes()
    while True:
        message = to_server_socket.recv(1024)
        if len(message) > 0:
            # if it's a 304, don't send to client (we already have the cached version)
            if cached and len(response) == 0 and message.startswith(b'HTTP/1.0 304 '):
                client_tcp = None
            response += message
            if client_tcp:
                client_tcp.send(message)
            continue
        break
    # decode headers and status code

    decoded_str = response.split(b'\r\n\r\n')[0].decode()  # get the first part of the response (do not decode the body)
    status_code = int(decoded_str.split(' ')[1])
    headers = decoded_str.split('\r\n')[1:]
    return status_code, headers, response


def send_conditional_get(headers: list[str], path: str, host: str, send_port: int, client_tcp: socket):
    """
    handle conditional get situation
    :param headers: Header lines
    :param path: Path to destination
    :param host: port hostname
    :param send_port: as name
    :param client_tcp: tcp socket for client
    :return: Boolean
    """

    has_if_modified = False
    for line in headers:
        if line.startswith('If-Modified-Since:'):
            has_if_modified = True
            break
    if not has_if_modified:
        now = datetime.now()
        # to gmt
        headers.append(f'If-Modified-Since: {now.strftime("%a, %d %b %Y %H:%M:%S GMT")}')
    status, headers, response = send_request(headers, path, host, send_port, client_tcp, True)
    if status == 304:
        return (True,)
    return (False, status, headers, response)


def extract_header(http_message: bytes, key: str):
    """
    Extract the header information
    :param http_message: http message from server
    :param key: get the key word we need
    :return: extracted header, String
    """
    key = key + ':'
    lines = http_message.split(b'\r\n\r\n', 1)[0].decode()
    lines = lines.split('\r\n')
    for line in lines[1:]:
        if line.startswith(key):
            return line[len(key):].strip()
    return None


def client_connect(client_tcp: socket):
    """
    accept and handle request
    :param client_tcp:
    :return: None
    """
    print('connected')
    send_port = 80  # default port
    hostname = ''
    path = '/'  # default path
    request = ''
    headers = []
    header_regex = "([\w-]+): (.*)"
    check = ''
    request = get_request(client_tcp, request)

    # for each line
    req_from_client = request.split("\r\n\r\n", 1)[0].split("\r\n")

    check = handle_first_line(req_from_client[0], hostname, path, send_port, client_tcp)
    if check is None:
        return None
    hostname, path, send_port = check

    if path.startswith('/proxy/'):
        # it's a request to the proxy
        if path.startswith('/proxy/cache/'):
            if cache_resolve(path):
                send_ok(client_tcp)
                client_tcp.close()
                return None
        elif path.startswith('/proxy/blocklist/'):
            if block_resolve(path):
                send_ok(client_tcp)
                client_tcp.close()
                return None
        # send_error(400, client_tcp) # Bad request
        # return None

    # test block list
    url = req_from_client[0].split(' ')[1]
    if not block_handler(url):
        send_error(403, client_tcp)
        return None

    # test cache
    req_from_client = req_from_client[1:]  # remove first line
    # Handle rest of headers
    if len(req_from_client) > 0:
        for line in req_from_client:
            if not re.search(header_regex, line):
                send_error(400, client_tcp)
                client_tcp.close()
                return None
            if line.startswith('Connection:'):  # ignore Connection header
                continue
            headers.append(line)

    cache = cache_get(url)
    if cache is not None:
        last_modified = extract_header(cache, 'Last-Modified')
        if last_modified is not None:
            headers.append(f'If-Modified-Since: {last_modified}')

        check = send_conditional_get(headers, path, hostname, send_port, client_tcp)
        if check[0]:
            client_tcp.send(cache)
            client_tcp.close()
            return None
        status, headers, response = check[1:]
    else:
        status, headers, response = send_request(headers, path, hostname, send_port, client_tcp)

    if status == 200:
        cache_put(url, response)

    client_tcp.close()


# Start of program execution
# Parse out the command line server address and port number to listen to
parser = OptionParser()
parser.add_option('-p', type='int', dest='serverPort')
parser.add_option('-a', type='string', dest='serverAddress')
(options, args) = parser.parse_args()

port = options.serverPort
address = options.serverAddress
if address is None:
    address = 'localhost'
if port is None:
    port = 2100

# Set up signal handling (ctrl-c)
signal.signal(signal.SIGINT, ctrl_c_pressed)

# TODO: Set up sockets to receive requests
to_client_skt = socket(AF_INET, SOCK_STREAM)
to_client_skt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
print(f'listening on {address}:{port}')
to_client_skt.bind((address, port))
to_client_skt.listen(1)
print('proxy ready receive')

# IMPORTANT!
# Immediately after you create your proxy's listening socket add
# the following code (where "skt" is the name of the socket here):
# Without this code the autograder may cause some tests to fail
# spuriously.
thread_count = 0
while True:
    client_tcp, address = to_client_skt.accept()
    print('connection accepted')
    thread = threading.Thread(target=client_connect, args=(client_tcp,))
    thread.start()
    thread_count += 1
    print(f'Num of thread {thread_count}')

    # TODO: accept and handle connections
# to_client_skt.close()
