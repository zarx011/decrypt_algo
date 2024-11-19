# file for hash/dict/IOC Vignere decryption algorithm for demonstration
from collections import Counter
import time

# create dictionary from common_words.txt to group by len
def load_dict(filename='common_words.txt'):
    with open(filename, 'r') as file:
        # read lines & strip whitespace & store as dict
        return {line.strip().lower(): len(line.strip()) for line in file if line.strip()} # make lowercase

# 'global' variable for file
common_words = load_dict('common_words.txt') # max word len = 22

# func to check valid words using hash lookup
def is_valid(decrypted_text, common_words):
    words = decrypted_text.split()
    common_words_set = set(common_words)  
    for word in words:
        if word not in common_words_set: 

            return False
    return True

# func to find words from dict by length
def find_by_len(common_words, length):
    return [word for word in common_words.keys() if len(word) == length]  # access keys of dict

# func to hash a key arithmetically 
def hash_key(key):
    val = 0
    pr = 7 # prime num to reduce collisions
    for i, char in enumerate(key):
        val += (ord(char) * pr**i)
    return val & 0xFFFFFFFF

# func to ensure only alphabetic char are processed
def preprocess(ciphertext):
    return (''.join([char.lower() for char in ciphertext if char.isalpha() or char.isspace()]))

# func to apply current key to decrypt char shift
def shift_char(ciphertext, key):
    cleaned_txt = preprocess(ciphertext) # preprocess txt
    len_key = len(key)
    shifted = []
    key_idx = 0
    for char in cleaned_txt:
        # calculate shift based on current key
        if char == ' ':  # directly append spaces
            shifted.append(' ')
        else:
            shift = ord(key[key_idx % len_key].lower()) - ord('a')
            decrypted_char = chr((ord(char.lower()) - ord('a') - shift) % 26 + ord('a'))
            shifted.append(decrypted_char)
            key_idx += 1
    return ''.join(shifted)

# func to 
# max len is for key
def calc_ioc(ciphertext, max_len=22):
    cleaned_txt = preprocess(ciphertext) # preprocess txt
    
    def group_by_len(cleaned_txt, len_key):
        groups = ['' for _ in range(len_key)] 
        for i, char in enumerate(cleaned_txt):
            if char != ' ':  # ignore spaces
                idx = i % len_key  # group index
                groups[idx] += char  # append char to appropriate group
      #  return [''.join(group) for group in groups]
        return [group for group in groups if group]
    
    def ioc_col(col_text):
        freq = Counter(col_text)
        n = len(col_text)
        if n <= 1:
            return 0.0
        # calc IoC formula
        return sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))    
    
    # iterate over potentential key_len & calc
    iocs = []
    for len_key in range(1, max_len + 1):
        txt_groups = group_by_len(cleaned_txt, len_key)
        avg_ioc = sum(ioc_col(col) for col in txt_groups) / len(txt_groups)
        iocs.append((len_key, avg_ioc))
    return iocs

# decrypt function
def decrypt_vignere(ciphertext, max_len=22):
    # calculate ioc for different key lengths
    key_iocs = calc_ioc(ciphertext)
    
    # sort by ioc val & choose best key_lengths
    key_iocs.sort(key=lambda x: x[1], reverse=True)
    # attempt decryption w/ best key len
    best_len,_ = key_iocs[0]
   # print(f"Using key length {best_len} based on IoC analysis.") # debug
    
    # find all possible keys from best len
    keys = find_by_len(common_words, best_len)
    # set to track hashed keys in O(1) time
    tried_keys = set()

    for key in keys:
        # hash key to later add to set
        hash = str(hash_key(key))

        if hash in tried_keys:
            continue # skip if already used

        # decrypt using key
        decrypted_text = shift_char(ciphertext, key)
        # validity check
        if is_valid(decrypted_text, common_words):
           return key, decrypted_text  # return first valid found
            

        # add hash of key to tried set
        tried_keys.add(hash)
        
    # if no valid found 
    print("No valid decryption found")
    #return None

    



#------------------------------------------------------------------------------------------------------------------

# entry point
if __name__ == "__main__":
   # ciphertext = input("Enter the encrypted message: ")
    # preprocess before decryption
   # cleaned_ciphertext = preprocess(ciphertext)

    start_time = time.time() # start timer

    # run the decrypt algorithm 

    end_time = time.time() # end timer
  
    # 'this is test using common word from list' using 'key'
    print(decrypt_vignere('dlgc mq diqd yqsre mskwsl gspn jpyq jswr'))

    # determine best key length
    
    # print time taken for decryption
    print(f"Decryption took {end_time - start_time:.2f} seconds")
