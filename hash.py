# file for hash/dict/IOC Vignere decryption algorithm for demonstration

import string
from collections import Counter
import hashlib


# func to shift characters
def shift_decrypt(char, key_char):
    if char.isalpha():
        shift = ord(key_char.lower()) - ord('a')
        return chr((ord(char.lower()) - ord('a') - shift) % 26 + ord('a'))
    return char

# func to apply current key to decrypt 
def decrypt_with_key(ciphertext, key):
    plaintext = []
    key_len = len(key)
    #key_index = 0  # separate counter for key idx
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(key[i % key_len].lower()) - ord('a')
            decrypted_char = chr((ord(char.lower()) - ord('a') - shift) % 26 + ord('a'))
            plaintext.append(decrypted_char)
        else:
            plaintext.append(char)  # preserve non-alphabetic chars

    return ''.join(plaintext)

# load set of common english words
def load_common_words(filename='common_words.txt'):
    with open(filename, 'r') as file:
        # read lines & strip whitespace, then convert to a set
        return {line.strip() for line in file if line.strip()}

# func to count valid words using hash table lookup
def is_valid(decrypted_text, valid_words):
    words = decrypted_text.split()
   # return sum(1 for word in words if word.lower() in common_words)
    return all(word in valid_words for word in words)


# func (greedy heuristic) to get most frequent letters
def get_most_frequent(ciphertext):
    letter_count = {char: 0 for char in string.ascii_lowercase}
    for char in ciphertext:
        if char.isalpha():
            letter_count[char.lower()] += 1

'''
    letter_count = {char: 0 for char in string.ascii_lowercase}
    for char in ciphertext:
        if char.isalpha():
            letter_count[char.lower()] += 1
    sorted_letters = sorted(letter_count, key=letter_count.get, reverse=True)
    return sorted_letters[:5]  # return the top 5 most freq letters
    '''

# helper func to calculate IoC for single col of ciphertext
def calc_ioc(col_text):
    n = len(col_text)
    if n <= 1:
        return 0.0
    frequencies = Counter(col_text)
    numerator = sum(f * (f - 1) for f in frequencies.values())
    denominator = n * (n - 1)
    return numerator / denominator if denominator != 0 else 0.0

'''
    n = len(col_text)
    if n <= 1:
        return 0.0

    #frequencies = Counter(col_text)
    frequencies = Counter(col_text)
    print(f"Frequencies for column '{col_text}': {frequencies}")  # Debugging output

    numerator = sum(f * (f - 1) for f in frequencies.values())
    denominator = n * (n - 1)

    print(f"Numerator: {numerator}, Denominator: {denominator}")  # Debugging output

    # Prevent division by zero
    if denominator == 0:
        return 0.0

    return numerator / denominator
    '''

# func to divide ciphertext into col based on guessed key_len
def group_by_len(ciphertext, key_len):
    cols = ['' for _ in range(key_len)]
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            cols[i % key_len] += char.lower()
    print(f"Grouped columns for key length {key_len}: {cols}")  # debug
    return [col for col in cols if col]  # filter out empty 

# func to calculate IoC for each guessed len
def len_with_ioc(ciphertext, max_key_len = 10):
    best_len = 3
    best_ioc = 0.068

    for key_len in range(1, max_key_len + 1):
        cols = group_by_len(ciphertext, key_len)
        if not cols:
                continue # skip if empty
        
        ioc_sum = sum(calc_ioc(col) for col in cols)
        print(f"IOC sum {ioc_sum}")
        avg_ioc = ioc_sum / len(cols) if cols else 0.0
        print(f"Avg IOC {avg_ioc}")

        # compare w target IoC of 0.068 [english language]
        if abs(avg_ioc - 0.068) < abs(best_ioc - 0.068):
            best_ioc = avg_ioc
            print(f"Best IOC {best_ioc}")
            best_len = key_len
            print(f"Best len {best_len}")

    return best_len if best_ioc > 0 else 1

''''
    best_len = 1
    best_ioc = 0.0

    for key_len in range(1, max_key_len + 1):
        cols = group_by_len(ciphertext, key_len)
       # print(f"Checking key length: {key_len} | Columns: {cols}")  # Debugging output

        ioc_sum = 0.0
        for col in cols:
            ioc_sum += calc_ioc(col)
        
        avg_ioc = ioc_sum / len(cols) if cols else 0.0  # Use len(cols) instead of key_len to avoid division by zero

        print(f"Key Length: {key_len} | Avg. IoC: {avg_ioc}")

        if abs(avg_ioc - 0.068) < abs(best_ioc - 0.068):
            best_ioc = avg_ioc
            best_len = key_len
  

    return best_len
    '''
  
''''  best_len = 1
    best_ioc = 0.0

    for key_len in range(1, max_key_len + 1):
        cols = group_by_len(ciphertext, key_len)
        ioc_sum = 0.0

        for col in cols:
            ioc_sum += calc_ioc(col)

        avg_ioc = ioc_sum / key_len # average IoC for current len

    #    print(f"Key Length: {key_len} | Avg. IoC: {avg_ioc}")

        # update best key_len based on IoC value [IoC ~ 0.068 - for texts in english]
        if abs(avg_ioc - 0.068) < abs(best_ioc - 0.068):
            best_ioc = avg_ioc
            best_len = key_len
            '''
# func to find keys of same length from txt
def find_keys_of_len(common_words, length):
    return [word for word in common_words if len(word) == length]

# func to hash a key
def hash_key(key):
    return hashlib.md5(key.encode()).hexdigest()
  
# main decrypt func (combining IoC, Greedy and Hash) valudation
def combined_decrypt_vignere(ciphertext, max_key_len=10):
    common_words = load_common_words()
    likely_key_len = len_with_ioc(ciphertext, max_key_len)

    print(f"Most likely key length from IoC: {likely_key_len}")

    candidate_keys = find_keys_of_len(common_words, likely_key_len)

    # set hash
    tested_keys = set()

    for key in candidate_keys:
        key_hash = hash_key(key)

    # skip if already been tested
        if key_hash in tested_keys:
            print(f"Skipping already tested key: {key}")
            continue
        
        # decrypt w/  candidate key
        decrypted_text = decrypt_with_key(ciphertext, key)

        print(f"processing decrypted text {decrypted_text} using key {candidate_keys}")
        
        # check if the decrypted text is valid
        if is_valid(decrypted_text, common_words):
            return key, decrypted_text  # Return the first valid decryption found

        # Add the hash of the tested key to the set
        tested_keys.add(key_hash)
        
    return None, "No valid found"



'''''
    for key in candidate_keys:
        if len(key) == likely_key_len:
            decrypted_text = decrypt_with_key(ciphertext, key)
            print(f"processing decrypted text {decrypted_text} using key {candidate_keys}")
            if count_valid(decrypted_text, common_words):
                return key, decrypted_text
    return None, "Decryption Failed"
'''

'''''   
  #  best_decrypt = None
  #  max_valid = 0

    # use IoC to find most likely key_len
    best_key_len = len_with_ioc(ciphertext, max_key_len)
    print(f"Most likely key length from IoC: {best_key_len}")

    for key in common_words:
        if len(key) == best_key_len:
            decrypted_text = decrypt_with_key(ciphertext, key)
            valid_count = is_valid(decrypted_text, common_words)

            # if more than 1/2 of words are valid
            if valid_count > len(decrypted_text.split()) * 0.5:
                print(f"Found valid decryption with key: {key}")
                return key, decrypted_text
            
    return None, "Decryption failed"

 
'for key in common_words:
        if len(key) == best_key_len:
            # decrypt & count amt of valid words 
            decrypted_text = decrypt_with_key(ciphertext, key)
            valid_count = count_valid(decrypted_text, common_words)

            # check if more than half of words are valid
            if valid_count > len(decrypted_text.split()) * 0.5:
          #      print("Found valid decryption!")  # ---------------------------------------- debugging
                return key, decrypted_text
            '''

# func to remove non-alphabetic char and preprocess ciphertext
def preprocess(ciphertext):
    return ''.join([char.lower() for char in ciphertext if char.isalpha()])

# entry point
if __name__ == "__main__":
    ciphertext = input("Enter the encrypted message: ")
    cleaned_ciphertext = ''.join(c for c in ciphertext if c.isalpha() or c.isspace())  # Clean the input
    key, decrypted_text = combined_decrypt_vignere(cleaned_ciphertext, max_key_len=10)
    
    if key:
        print(f"Decryption successful!\nKey: {key}\nDecrypted Text: {decrypted_text}")
    else:
        print("Decryption failed")

# -------------------------------------------------------------------------------------------

'''
from collections import Counter
import string

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
    return letter_count  # Return full counts for all letters

# helper func to calculate IoC for single col of ciphertext
def calc_ioc(encrypted_message, min_key_length, max_key_length):
    ioc_values = {}

    for key_length in range(min_key_length, max_key_length + 1):
        columns = [''.join(encrypted_message[i::key_length]) for i in range(key_length)]
        numerator = 0
        denominator = 0

        for col in columns:
            freq = {chr(i): 0 for i in range(97, 123)}  # Frequency dictionary for a-z
            for char in col:
                if char in freq:
                    freq[char] += 1

            col_length = len(col)
            numerator += sum(count * (count - 1) for count in freq.values())
            denominator += col_length * (col_length - 1)

        if denominator > 0:
            avg_ioc = numerator / denominator
            ioc_values[key_length] = avg_ioc
        else:
            ioc_values[key_length] = 0

    return ioc_values

# func to divide ciphertext into col based on guessed key_len
def group_by_len(ciphertext, key_len):
    cols = ['' for _ in range(key_len)]
    for i, char in enumerate(ciphertext):
        cols[i % key_len] += char.lower()
    print(f"Grouped columns for key length {key_len}: {cols}")  # Debugging output

    return [col for col in cols if col]  # filter out empty columns

# func to analyze key lengths based on Index of Coincidence
def analyze_key_length(ciphertext, max_key_len=10):
    best_len = 1
    best_ioc = 0.0

    for key_len in range(1, max_key_len + 1):
        cols = group_by_len(ciphertext, key_len)
        print(f"Checking key length: {key_len} | Columns: {cols}")  # Debugging output

        ioc_sum = 0.0
        for col in cols:
            ioc_sum += calc_ioc(col)
        
        avg_ioc = ioc_sum / len(cols) if cols else 0.0  # Use len(cols) instead of key_len to avoid division by zero
        print(f"Key Length: {key_len} | Avg. IoC: {avg_ioc}")

        if abs(avg_ioc - 0.068) < abs(best_ioc - 0.068):
            best_ioc = avg_ioc
            best_len = key_len

    return best_len

# main decrypt func (combining IoC, Greedy and Hash) validation
def combined_decrypt_vignere(ciphertext, max_key_len):
    common_words = load_common_words('common_words.txt')

    # use IoC to find most likely key_len
    best_key_len = analyze_key_length(ciphertext, max_key_len)
    print(f"Most likely key length from IoC: {best_key_len}")  # Debugging output

    for key in common_words:
        if len(key) == best_key_len:
            decrypted_text = decrypt_with_key(ciphertext, key)
            valid_count = count_valid(decrypted_text, common_words)

            if valid_count > len(decrypted_text.split()) * 0.5:
                print(f"Found valid decryption with key: {key}")
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

        '''