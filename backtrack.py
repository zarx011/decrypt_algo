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
    valid_count = sum(1 for word in word_list if word in common_words)
    
    print(f"Decrypted Text: {decrypted_text}, Valid Words: {valid_count}/{len(word_list)}")
    
    return valid_count > len(word_list) * 0.5

# backtracking func for key combinations
def backtrack(ciphertext, key_len, curr_key='', common_words=set()):
    if len(curr_key) == key_len:
        if curr_key in common_words:  # check if valid word
            decrypted_text = decrypt_wkey(ciphertext, curr_key)
            print(f"Trying key: {curr_key} , Decrypted Text: {decrypted_text}")  # debugging
            if is_valid(decrypted_text, common_words):
                return curr_key, decrypted_text
        return None, None  # no valid decryption

    # recursively try all letters in alpha
    for letter in string.ascii_lowercase:
        new_key, decrypted_text = backtrack(ciphertext, key_len, curr_key + letter, common_words)
        if new_key:
            return new_key, decrypted_text

    return None, None  # no valid decryption

# func to decrypt w/ multiple key lengths
def decrypt_vigenere(ciphertext, max_key_len, common_words):
    for key_len in range(1, max_key_len + 1):
        print(f"Trying key length: {key_len}")
        key, decrypted_text = backtrack(ciphertext, key_len, common_words=common_words)
        if key:
            return f"Key: {key}, Decrypted Text: {decrypted_text}"
    return "Decryption failed"

# load a set of common end words
def load_common_words():
    return {"the", "and", "hello", "world", "this", "is", "an", "example", "test",
            "cipher", "key", "for", "backtracking", "algorithm", "there", "was",
            "with", "a", "to", "of", "words", "message", "book", "fun", "secret", "vignere"}

# test call
if __name__ == "__main__":
    common_words = load_common_words()  #lLoad common words
   
    ciphertext = input("Enter the encrypted message: ").strip().lower()  # input handling
    result = decrypt_vigenere(ciphertext, max_key_len=10, common_words=common_words)
    print(result)
