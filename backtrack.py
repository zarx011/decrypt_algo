
# file for backtracking Vignere (no key) decryption algorithm for demonstration

import string
import time

# func to decrypt a char w/ key [shift first]
def shift_decrypt(char, key_char):
    if char.isalpha():
        shift = ord(key_char.lower()) - ord('a')
        return chr((ord(char.lower()) - ord('a') - shift) % 26 + ord('a'))
    return char

# func to apply current key to decrypt 
def decrypt_with_key(ciphertext, key):
    key_len = len(key)
    plaintext = []
    key_index = 0  # counter for key idx
    for char in ciphertext:
        if char.isalpha():
            key_char = key[key_index % key_len]  # only use for alphabetic chars
            plaintext.append(shift_decrypt(char, key_char))
            key_index += 1  # increment idx
        else:
            plaintext.append(char)  # preserve non-alphabetic 
    return ''.join(plaintext)

# func to validate decrypted text
def is_valid(decrypted_text, common_words):
    word_list = decrypted_text.split()
    if not word_list:  # if empty
        return False
    valid_count = sum(1 for word in word_list if word in common_words)
    return valid_count > len(word_list) * 0.5

# backtracking func for key combinations
def backtrack(ciphertext, key_len, curr_key='', common_words=set()):
    failed_attempts = 0  # count failed attempts
    for curr_key in common_words:
        if len(curr_key) == key_len:  # check if curr len matches
            decrypted_text = decrypt_with_key(ciphertext, curr_key)  # decrypt
            # validity case handling
            if is_valid(decrypted_text, common_words):  # if valid
                print("Found valid decryption!") 
                return curr_key, decrypted_text  # return when valid
            else:
               failed_attempts += 1

    return None, None  # if no valid decryption

# func to decrypt w/ multiple key lengths
def decrypt_vigenere(ciphertext, max_key_len, common_words):
    for key_len in range(1, max_key_len + 1):
        key, decrypted_text = backtrack(ciphertext, key_len, common_words=common_words)
        if key:
            return f"Key: '{key}' | Decrypted Text: '{decrypted_text}'"
    return "Decryption failed"

# load set of common english words
def load_common_words(filename='common_words.txt'):
    with open(filename, 'r') as file:
        # read lines/strip whitespace & convert to a set
        return {line.strip() for line in file if line.strip()}

# test call
if __name__ == "__main__":
    common_words = load_common_words()  #l oad from file
    ciphertext = input("Enter the encrypted message: ").strip().lower()  # input handling
    
    start_time = time.time() # start timer
    result = decrypt_vigenere(ciphertext, max_key_len=10, common_words=common_words)
    end_time = time.time() # end timer

    print(result)
    print(f"Decryption took {end_time - start_time:.2f} seconds")