import string

# func to decrypt a char w/ key
def shift_decrypt(char, key_char):
    if char.isalpha():
        shift = ord(key_char.lower()) - ord('a')
        return chr((ord(char.lower()) - ord('a') - shift) % 26 + ord('a'))
    return char

# func to apply current key to decrypt 
def decrypt_wkey(ciphertext, key):
    key_len = len(key)
    plaintext = []
   # for i, char in enumerate(ciphertext):
    #    if char.isalpha():
       #     key_char = key[i % key_len]
       #     plaintext.append(shift_decrypt(ciphertext[i], key_char))
      #  else:
          #  plaintext.append(char)
    key_index = 0  # separate counter for key index
    for char in ciphertext:
        if char.isalpha():
            key_char = key[key_index % key_len]  # only use for alphabetic characters
            plaintext.append(shift_decrypt(char, key_char))
            key_index += 1  # increment only for letters
        else:
            plaintext.append(char)  # preserve non-alphabetic characters

    return ''.join(plaintext)

# func to validate decrypted text
def is_valid(decrypted_text):
    common_words = {
        "the", "and", "hello", "world", "this", "is", "an", "example", "test",
        "cipher", "key", "for", "backtracking", "algorithm", "there", "was",
        "with", "a", "to", "of", "words", "message", "solution"
    }
    
    word_list = decrypted_text.split()
    valid_count = 0

    # count words in common words set
    for word in word_list:
        if word in common_words:
            valid_count += 1
    
    # debugging print to see  decrypted text & valid word count
    print(f"Decrypted Text: {decrypted_text}, Valid Words: {valid_count}/{len(word_list)}")
    
    return valid_count > len(word_list) * 0.5

# backtracking func for key combinations
def backtrack(ciphertext, key_len, curr_key='', index=0):
    # base case: if curr key length matches desired length
    if len(curr_key) == key_len:
        decrypted_text = decrypt_wkey(ciphertext, curr_key)
        if is_valid(decrypted_text):
            return curr_key, decrypted_text
        return None, None  # no valid decryption

    # recursively try all letters in alphabet
    for letter in string.ascii_lowercase:
        new_key, decrypted_text = backtrack(ciphertext, key_len, curr_key + letter, index + 1)
        if new_key:
            return new_key, decrypted_text

    return None, None  # no valid decryption after trying all letters

# func to decrypt using multiple key len
def decrypt_vigenere(ciphertext, max_key_len):
    for key_len in range(1, max_key_len + 1):
        print(f"Trying key length: {key_len}")
        key, decrypted_text = backtrack(ciphertext, key_len)
        if key:
            return f"Key: {key}, Decrypted Text: {decrypted_text}"
    return "Decryption failed"

# test call
if __name__ == "__main__":
    # ciphertext = "rijvs uyvjn"  # "hello world" encrypted with key "key"
   # ciphertext = "rijvs uyvjn"  # "hello" encrypted with key "key"
    ciphertext = "rgfy"

    result = decrypt_vigenere(ciphertext, max_key_len=5)
    print(result)
