# seems to stop checking once key_len = 6 even though max set at 10
# doesn't seem to work for keys other than "key"
# something is weird with it in general but not sure exactly what yet

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
    key_index = 0  # separate counter for key idx
    for char in ciphertext:
        if char.isalpha():
            key_char = key[key_index % key_len]  # only use for alphabetic characters
            plaintext.append(shift_decrypt(char, key_char))
            key_index += 1  # increment only for letters
        else:
            plaintext.append(char)  # preserve non-alphabetic chars

    return ''.join(plaintext)

# func to validate decrypted text
def is_valid(decrypted_text, common_words):
    word_list = decrypted_text.split()
    if not word_list:  # if empty
        return False
    valid_count = sum(1 for word in word_list if word in common_words)
    
    print(f"Decrypted Text: {decrypted_text}, Valid Words: {valid_count}/{len(word_list)}")
    
    return valid_count > len(word_list) * 0.5

# backtracking func for key combinations
def backtrack(ciphertext, key_len, curr_key='', common_words=set()):
    #print(f"Current key: {curr_key}, Length: {len(curr_key)}")  # debug

    #if len(curr_key) == key_len:
      #  print("Reached desired key length:", curr_key)
      #  decrypted_text = decrypt_wkey(ciphertext, curr_key)

      #  print(f"Trying key: {curr_key}, Decrypted Text: {decrypted_text}")  # debugging

      #  if is_valid(decrypted_text, common_words):
         #   print("Found valid decryption!")
          #  return curr_key, decrypted_text  # return when valid
      #  else:
          #  print(f"Decryption using key '{curr_key}' failed or not valid.")
      #  return None, None  # if no valid decryption

        # recursively try all letters in alphabet
 #   for letter in string.ascii_lowercase:
    #    print(f"Trying letter: {letter} with current key: {curr_key}")  # Debugging
     #   new_key, decrypted_text = backtrack(ciphertext, key_len, curr_key + letter, common_words)
      #  if new_key:  # if valid key found, stop
        #   return new_key, decrypted_text  # return immediately after finding

    # if no valid key, return None
  #  return None, None
    
    print(f"Trying key length: {key_len}")  # debug
    for curr_key in common_words:
        if len(curr_key) == key_len:  # dheck if curr length matches
            decrypted_text = decrypt_wkey(ciphertext, curr_key)  # decrypt
            print(f"Trying key: '{curr_key}', Decrypted Text: '{decrypted_text}'")  # debugging
            
            if is_valid(decrypted_text, common_words):  # check validity
                print("Found valid decryption!")  # debugging 
                return curr_key, decrypted_text  # return when valid
            else:
                print(f"Decryption using key '{curr_key}' failed or not valid.")
    
    return None, None  # if no valid decryption


# func to decrypt w/ multiple key lengths
def decrypt_vigenere(ciphertext, max_key_len, common_words):
    for key_len in range(1, max_key_len + 1):
        print(f"Trying key length: {key_len}")

        key, decrypted_text = backtrack(ciphertext, key_len, common_words=common_words)
        if key:
            return f"Key: {key}, Decrypted Text: {decrypted_text}"
    return "Decryption failed"

# load set of common english words
def load_common_words(filename='common_words.txt'):
    with open(filename, 'r') as file:
        # read lines & strip whitespace, then convert to a set
        return {line.strip() for line in file if line.strip()}

# test call
if __name__ == "__main__":
    common_words = load_common_words()  #load from file
    
    ciphertext = input("Enter the encrypted message: ").strip().lower()  # input handling
    result = decrypt_vigenere(ciphertext, max_key_len=10, common_words=common_words)
    print(result)