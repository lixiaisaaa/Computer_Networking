def better_compression(s):
    freq = {}
    i = 0
    while i < len(s):
        char = s[i]
        i += 1
        num_start = i
        while i < len(s) and s[i].isdigit():
            i += 1
        num = int(s[num_start:i])

        if char in freq:
            freq[char] += num
        else:
            freq[char] = num

    result = []
    for char in sorted(freq.keys()):
        result.append(char + str(freq[char]))

    return ''.join(result)

s = "c4b5a13c1a33"
print(better_compression(s))