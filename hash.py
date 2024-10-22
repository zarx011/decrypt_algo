# file for hash/dict/IOC Vignere decryption algorithm for demonstration

# import string
from collections import Counter
import hashlib

# create dictionary from common_words.txt to group by length
def load_dict(filename='common_words.txt'):
    with open(filename, 'r') as file:
        # read lines & strip whitespace & store as dictionary
        return {line.strip().lower(): len(line.strip()) for line in file if line.strip()}  # make lowercase
    
# psuedo 'global variable' for file
common_words = load_dict('common_words.txt')
print(f"Common words loaded: {len(common_words)} words.")

# func to hash a key
def hash_key(key):
    return hashlib.md5(key.encode()).hexdigest()

# func to remove non-alphabetic char and preprocess ciphertext
def preprocess(ciphertext):
    return ''.join([char.lower() for char in ciphertext if char.isalpha()])

# func to apply current key to decrypt ,shifts ciphertext to alpha 
def apply_curr_key(ciphertext, key):
    key_len = len(key)
    decrypted_text = []

    for i, char in enumerate(ciphertext):
        if char.isalpha():
            # calculate decrypted char
            shift = ord(key[i % key_len].lower()) - ord('a')
            decrypted_char = chr((ord(char.lower()) - ord('a') - shift) % 26 + ord('a'))
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)
 
    
# func to check valid words using hash table lookup
def is_valid(decrypted_text, common_words):
    words = decrypted_text.split()
    return all(word in common_words for word in words if word)

# func to find words from dict by length
def find_by_len(common_words, length):
    return [word for word in common_words.keys() if len(word) == length]  # access keys of dict

# func to divide ciphertext into col based on guessed key_len
def group_by_len(ciphertext, key_len):
  return [ciphertext[i::key_len] for i in range(key_len)]  # filter out empty
  
  '''  cols = ['' for _ in range(key_len)]
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            cols[i % key_len] += char.lower()

   # print(f"Grouped columns for key length {key_len}: {cols}")  # debug
   '''

# helper func to calculate IoC for single col of ciphertext
def calc_ioc(col_text):
   cleaned_col_text = preprocess(col_text)
   print(f"cleaned_col_text: {cleaned_col_text}")
   # calculate frequencies
   freq = Counter(cleaned_col_text)
   n = len(cleaned_col_text)
   # avoid /0 error
   if n <= 1:
       return 0
   # calculate ioc
   ioc = sum(f * (f-1) for f in freq.values()) / (n *(n - 1))
   return ioc

   ''' n = len(col_text)
    if n <= 1:
        return 0.0
    frequencies = Counter(col_text)
    numerator = sum(f * (f - 1) for f in frequencies.values())
    denominator = n * (n - 1)

    if numerator == 0 or denominator == 0:
        return None
    
#    print(f"Frequencies: {frequencies}, Numerator: {numerator}, Denominator: {denominator}")  # debug
    print(f"n: {n}, Numerator: {numerator}, Denominator: {denominator}")


    return numerator / denominator 
    '''

# func to calculate IoC for each guessed len
def len_with_ioc(ciphertext, max_key_len = 12):
    best_len = None
    best_ioc = 0.068 # for english language
    # to iterate each column
    for key_len in range(1, min(max_key_len, len(ciphertext)) + 1):
        cols = group_by_len(ciphertext, key_len)
        print(f"Cols for key length {key_len}: {cols}")

        if not cols:
                continue # skip if empty
        # only include valid ioc values
        ioc_vals = [calc_ioc(col) for col in cols]
        print(f"IoC values: {ioc_vals}")
        valid_ioc = [ioc for ioc in ioc_vals if ioc is not None]

        if not valid_ioc:
            continue
        # calculate avergae from sum
        #avg_ioc = sum(calc_ioc(col) for col in cols) / len(cols)
        avg_ioc = sum(valid_ioc) / len(valid_ioc)
        print(f"avg ioc: {avg_ioc}")
        # compare w target IoC of 0.068 [english language]
        if abs(avg_ioc - 0.068) < abs(best_ioc - 0.068):
            best_ioc = avg_ioc
            best_len = key_len
    return best_len if best_len != None else "appears as none - invalid"
  
# main decrypt func (combining IoC, Greedy and Hash) validation
def combined_decrypt_vignere(ciphertext, max_key_len=12):
    cleaned_ciphertext = preprocess(ciphertext)
    print(f"Cleaned ciphertext: {cleaned_ciphertext}")

    likely_len = len_with_ioc(cleaned_ciphertext, max_key_len)
    # variable for possible keys
    possible_keys = find_by_len(common_words, likely_len)
    # set hash for keys already tested
    tested = set()
    # iterate through all possible keys
    for key in possible_keys:
        key_hash = hash_key(key)
        print(f"Testing key: {key}, Decrypted text: {decrypted_text}")
        # skip if already tested
        if key_hash in tested:
            print(f"Skipping already tested key: {key}")
            continue
        # decrypt w/ current possible key
        decrypted_text = apply_curr_key(cleaned_ciphertext, key)

        if is_valid(decrypted_text, common_words):
            return key, decrypted_text  # return first valid decryption found
        # add hash of the tested key to set
        tested.add(key_hash)
        print(f"Is valid: {is_valid(decrypted_text, common_words)}")

    # if no valid decryption found
    return None, None

# entry point
if __name__ == "__main__":
  #  ciphertext = input("Enter the encrypted message: ")
        #-----------------------------------------------------------------------------------------------------------------------
    # example encrypted message - "this is a test with valid word" using key "key"
    ciphertext = "dlgc mq k xccx usxf fejsh uyvb"  

    cleaned_ciphertext = preprocess(ciphertext)

    # determine best key length
    key_length = len_with_ioc(cleaned_ciphertext)
    print(f"Most likely key length: {key_length}")

    key, decrypted_text = combined_decrypt_vignere(cleaned_ciphertext, max_key_len=12)

    if key:
        print(f"Decryption successful!\nKey: {key}\nDecrypted Text: {decrypted_text}")
    else:
        print(f"Decryption failed.\nKey: {key}\nDecrypted Text: {decrypted_text}")
