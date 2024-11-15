# file for hash/dict/IOC Vignere decryption algorithm for demonstration
from collections import Counter
import hashlib
import time

# create dictionary from common_words.txt to group by len
def load_dict(filename='common_words.txt'):
    with open(filename, 'r') as file:
        # read lines & strip whitespace & store as dictionary
        return {line.strip().lower(): len(line.strip()) for line in file if line.strip()}  # make lowercase
    
# psuedo 'global variable' for file
common_words = load_dict('common_words.txt')
#print([word for word in common_words.keys() if len(word) == 3])

# func to hash a key
def hash_key(key): 
    return hashlib.md5(key.encode()).hexdigest()

# func to ensure only alphabetic characters are processed
def preprocess(ciphertext):
    return (''.join([char.lower() for char in ciphertext if char.isalpha() or char.isspace()]))

# func to apply current key to decrypt ,shifts ciphertext to a-lpha 
def apply_curr_key(ciphertext, key):
    key_len = len(key)
    decrypted_text = []
    key_idx = 0 # to track key usage for alphabetic char only
    # iterate through chars
    for char in ciphertext:
        if char.isalpha():
            # calculate shift based on key
            shift = ord(key[key_idx % key_len].lower()) - ord('a')
            decrypted_char = chr((ord(char.lower()) - ord('a') - shift) % 26 + ord('a'))
            decrypted_text.append(decrypted_char)
            key_idx += 1
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)

# func to find words from dict by length
def find_by_len(common_words, length):
    return [word for word in common_words.keys() if len(word) == length]  # access keys of dict

# func to divide ciphertext into col based on guessed key_len
def group_by_len(ciphertext, key_len):
    return [ciphertext[i::key_len] for i in range(key_len)]  # filter out empty
  
# helper func to calculate IoC for single col of ciphertext
def calc_ioc(col_text):
   cleaned_col_text = preprocess(col_text)
   # calculate frequencies
   freq = Counter(cleaned_col_text)
   n = len(cleaned_col_text)
   # avoid /0 error
   if n <= 1:
       return 0.0
   # calculate ioc
   ioc = sum(f * (f-1) for f in freq.values()) / (n *(n - 1))
   return ioc

# 'psuedo global' var to define threshold 
ioc_threshold = 0.0068 # ioc for english language

# func to calculate IoC for each guessed len
def len_with_ioc(ciphertext, max_key_len):
    # to iterate each column
    ioc_vals = []
    for key_len in range(1, max_key_len + 1):
        cols = [''.join([ciphertext[i] for i in range(j, len(ciphertext), key_len)]) for j in range(key_len)]
        # calculate ioc for each col
        col_vals = [calc_ioc(col) for col in cols]
        # avg ioc for curr key_len
        avg_ioc = sum(col_vals) / len(col_vals)
        # append len & avg if ioc meets threshold
        if avg_ioc >= ioc_threshold:
            ioc_vals.append((key_len, avg_ioc)) 
    return ioc_vals
  
# func to check valid words using hash lookup
def is_valid(decrypted_text, common_words):
    words = decrypted_text.split()
    for word in words:
        valid = word in common_words
        if not valid:
            return False # return early if invalud
    return True

# main decrypt func (combining IoC, greedy and hash validation)
def combined_decrypt_vignere(ciphertext, max_key_len):
    # only consider alphabetic chars
    cleaned_ciphertext = preprocess(ciphertext)
    likely_len = len_with_ioc(cleaned_ciphertext, max_key_len)
    # variable for possible keys
    possible_keys = []
    # iterate through likely len to find valid words of len
    for length, _ in likely_len:
        possible_keys.extend(find_by_len(common_words, length))
    # set hash for keys already tested
    tested = set()
    # iterate through all possible keys
    for key in possible_keys:
        key_hash = hash_key(key)
       # print(f"Testing key: {key}")
        # skip if already tested
        if key_hash in tested:
         #   print(f"Skipping already tested key: {key}")
            continue
        # decrypt w/ current possible key
        decrypted_text = apply_curr_key(cleaned_ciphertext, key)
        #print(f"Testing key '{key}' - Decrypted text: '{decrypted_text}'")  # Debug output

     #   print(f"Decrypted text: {decrypted_text}")
        # validity check
        if is_valid(decrypted_text, common_words):
           return key, decrypted_text  # return first valid found
        # add hash of the tested key to set
        tested.add(key_hash)
    # if no valid decryption found
    return None, None

# entry point
if __name__ == "__main__":
    ciphertext = input("Enter the encrypted message: ")
    # preprocess before decryption
    cleaned_ciphertext = preprocess(ciphertext)

    start_time = time.time() # start timer
    # run the decrypt algorithm 
    key, decrypted_text = combined_decrypt_vignere(cleaned_ciphertext, max_key_len=25)
    end_time = time.time() # end timer

    # determine best key length
    if key:
        print(f"Decryption successful!\nKey: {key} | Decrypted Text: {decrypted_text}")
    else:
        print(f"Decryption failed.\nKey: {key} | Decrypted Text: {decrypted_text}")
    # print time taken for decryption
    print(f"Decryption took {end_time - start_time:.2f} seconds")