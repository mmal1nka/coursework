def encrypt(message, key):
    symbols = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ,.!?1234567890@#$%&*^()+:;/[]{}~<>|"
    encrypted = ""
    for i in message:
        if i not in symbols:
            return encrypted
    for i in key:
        if i not in symbols:
            return encrypted
    if len(message) == 0 or len(key) == 0 or len(message) < len(key):
        return encrypted
    else:
        letter_to_index = dict(zip(symbols, range(len(symbols))))
        index_to_letter = dict(zip(range(len(symbols)), symbols))
        split_text = [
            message[i: i + len(key)] for i in range(0, len(message), len(key))
        ]
        for each_split in split_text:
            i = 0
            for letter in each_split:
                number = (letter_to_index[letter] + letter_to_index[key[i]]) % len(symbols)
                encrypted += index_to_letter[number]
                i += 1

        return encrypted


def decrypt(message, key):
    symbols = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ,.!?1234567890@#$%&*^()+:;/[]{}~<>|"
    decrypted = ""
    for i in message:
        if i not in symbols:
            return decrypted
    for i in key:
        if i not in symbols:
            return decrypted
    if len(message) == 0 or len(key) == 0:
        return decrypted
    else:
        letter_to_index = dict(zip(symbols, range(len(symbols))))
        index_to_letter = dict(zip(range(len(symbols)), symbols))
        split_encrypted = [
            message[i: i + len(key)] for i in range(0, len(message), len(key))
        ]

        for each_split in split_encrypted:
            i = 0
            for letter in each_split:
                number = (letter_to_index[letter] - letter_to_index[key[i]]) % len(symbols)
                decrypted += index_to_letter[number]
                i += 1

        return decrypted

