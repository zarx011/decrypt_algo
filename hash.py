
# file for hash/dict/IOC Vignere decryption algorithm for demonstration

import string
from collections import Counter

# func to shift characters
def shift_decrypt(char, key_char):
    if char.isalpha():
        shift = ord(key_char.lower()) - ord('a')
        return chr((ord(char.lower()) - ord('a') - shift) % 26 + ord('a'))
    return char

# func to apply current key to decrypt 
def decrypt_with_key(ciphertext, key):
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

# load set of common english words
def load_common_words(filename='common_words.txt'):
    with open(filename, 'r') as file:
        # read lines & strip whitespace, then convert to a set
        return {line.strip() for line in file if line.strip()}

# func to count valid words using hash table lookup
def count_valid(decrypted_text, common_words):
    words = decrypted_text.split()
    return sum(1 for word in words if word.lower() in common_words)

# -func (greedy heuristic) to get most frequent letters
def get_most_frequent(ciphertext):
    letter_count = {char: 0 for char in string.ascii_lowercase}
    for char in ciphertext:
        if char.isalpha():
            letter_count[char.lower()] += 1
    sorted_letters = sorted(letter_count, key=letter_count.get, reverse=True)
    return sorted_letters[:5]  # return the top 5 most freq letters

# helper func to calculate IoC for single col of ciphertext
def calc_ioc(col_text):
    n = len(col_text)
    if n<= 1:
        return 0.0

    frequencies = Counter(col_text)
    numerator = sum(f* (f - 1) for f in frequencies.values())
    denominator = n * (n-1)

    return numerator / denominator 

# func to divide ciphertext into col based on guessed key_len
def group_by_len(ciphertext, key_len):
    cols = ['' for _ in range(key_len)]
    for i, char in enumerate(ciphertext):
        cols[i % key_len] += char.lower()
    return cols

# func to calculate IoC for each guessed len
def len_with_ioc(ciphertext, max_key_len = 10):
    best_len = 1
    best_ioc = 0.0

    for key_len in range(1, max_key_len + 1):
        cols = group_by_len(ciphertext, key_len)
        ioc_sum = 0.0

        for col in cols:
            ioc_sum += calc_ioc(col)

        avg_ioc = ioc_sum / key_len # average IoC for current len

      #  print(f"Key Length: {key_len} | Avg. IoC: {avg_ioc}")

        # update best key_len based on IoC value [IoC ~ 0.068 - for texts in english]
        if abs(avg_ioc - 0.068) < abs(best_ioc - 0.068):
            best_ioc = avg_ioc
            best_len = key_len

    return best_len

# main decrypt func (combining IoC, Greedy and Hash) valudation
def combined_decrypt_vignere(ciphertext, max_key_len):
    common_words = load_common_words('common_words.txt')
  #  best_decrypt = None
  #  max_valid = 0

    # use IoC to find most likely key_len
    best_key_len = len_with_ioc(ciphertext, max_key_len)
    # print(f"Most likely key length from IoC: {best_key_len}")

    for key in common_words:
        if len(key) == best_key_len:
            # decrypt & count amt of valid words 
            decrypted_text = decrypt_with_key(ciphertext, key)
            valid_count = count_valid(decrypted_text, common_words)

            # check if more than half of words are valid
            if valid_count > len(decrypted_text.split()) * 0.5:
            #    print("Found valid decryption!")  # debugging
                return key, decrypted_text
            
    return None, "Decryption failed"

# func to remove non-alphabetic char and preprocess ciphertext
def preprocess(ciphertext):
    return ''.join([char.lower() for char in ciphertext if char.isalpha()])

if __name__ == "__main__":
    common_words = load_common_words()  # load from file
    ciphertext = input("Enter the encrypted message: ").strip().lower()  # input handling
    cleaned_ciphertext = preprocess(ciphertext)

    result = combined_decrypt_vignere(cleaned_ciphertext, max_key_len=10)

    if isinstance(result, tuple) and result[0]:  # if key found
        print(f"Key: {result[0]} | Decrypted Text: {result[1]}")
    else:
        print(result)  # if decryption failed