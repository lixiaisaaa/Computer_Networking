def decode(encoded):
    encoded = encoded[::-1]
    Final_string = ''
    number = ''
    for i in range(len(encoded)):
        print(Final_string)
        number = number + encoded[i]
        if (int(number) >= 65 and int(number) <= 90) or (int(number) >= 97 and int(number) <= 122) or (int(number) == 32):
            character = chr(int(number))
            Final_string += character
            number = ''
    return Final_string


# Test
encoded = "23511011501782351112179911801562340161171141148"
print(decode(encoded))  # Expected output: "Truth Always win"


