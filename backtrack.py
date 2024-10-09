# transferred psuedocode from docs & tried to format to python syntax
# need to finish valid func & see if it runs

# file for backtracking decruption algorithm for demonstration

import string

# implementing backtracking

# func to decrypt a char with key
def shift_decrypt(char, key_char):
    if char.isalpha():
        # shift pos of key_char - pos of 'a'
        shift = ord(key_char.lower()) - ord('a') # ord -> numerical equiv.
        # shift char backwards by shift position
        return chr((ord(char.lower()) - ord('a') - shift) % 26 + ord('a'))
    return char # non-letter characters unchanged

# func to apply current key to decrypt ciphertext
def decrypt_wkey(ciphertext, key):
    key_len = len(key)
    plaintext = []
    # for i=0 to len-1
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            key_char = key[i % key_len]
            plaintext.append(shift_decrypt(ciphertext[i], key_char))
        else:
            plaintext.append(char) # non-letter characters unchanged
    return ''.join(plaintext) # return plaintext   


def is_valid(decrypted_text):
    # do later but going to add psuedocode from doc 
    # just for sake of having smth here

    # split decrypted text into words
     #  word_list = []
     #   valid__count = 0   
       # for each word in word_list:
            # if word is in dictionary then:
    #      valid_count += 1
    # return valid_word_count > threshold # ex: ~50% of words
    return None, None

# func to try different key combinations w/ backtracking
def backtrack(ciphertext, key_len, curr_key = '', index = 0):
    if len(curr_key) == key_len:
        decrypted_text = decrypt_wkey(ciphertext, curr_key)
        # if found valid decryption
        if is_valid(decrypted_text):
            return curr_key, decrypted_text
        return None, None # invalid decryption

   #  for each letter in alphabet
   # new_key = curr_key + letter
   # res_key, res_text = backtrack(ciphertext, key_len, new_key, index++ )
   # if not none:
   # return res_key, res_text --> return first valid key found

    for letter in string.ascii_lowercase:
         new_key, decrypted_text = backtrack(ciphertext, key_len, curr_key + letter, index + 1)
         if new_key:
            return new_key, decrypted_text
    
    return None, None # no valid decryption at this level

 # func to decrypt using multiple keylengths and backtracking
def decrypt_vigenere(ciphertext, max_key_len): # max_key_len = 10, 11, etc.
    for key_len in range(1, max_key_len + 1):
        key, decrypted_text = backtrack(ciphertext, key_len)
        if key:
            return f"Key: {key}, Decrypted Text: {decrypted_text}"
    return "Decryption failed"