

# Vigenère Cipher Decryption Algorithms

Repository demonstrates two approaches to decrypting text-encrypted messages using the Vigenère cipher
without a known key implemented with python

1. backtracking algorithm (backtrack.py):  uses a brute-force approach combined with a dictionary of common words (list taken from the Bag of Words dataset of the UC Irving Machine Learning Database
   -- edited with previously generated collection created using ChatGPT for a total of ~45k words
   [common_words.txt] file)

2. hash/ioc-based algorithm (hash.py): incorporates the Index of Coincidence (IoC), hashing, and a dictionary for efficient key guessing/storage


# Features

backtrack.py
- attempts to decrypt ciphertext by iterating through all possible keys of specified length in common_words.txt
- uses dictionary of common english words to validate potential decryptions - key and ciphertext required to be located in common_words.txt file in order for program to validate (limitation)
- simplified for demonstration purposes, is considered the worst case decryption approach when
  considering algorithmic runtime

hash.py
- analyzes ciphertext to suggest likely key lengths using IoC 
- hashes & tracks tested keys to avoid redundant computations [md5 hashing pre-imported py lib]
- prioritizes efficiency while maintain accuracy in decryption


# Functionality

1. shift decrypt: decrypts single characher (char) using a given key
2. key application: applies current key to decrypt entire ciphertext
3. validation: checks decrypted text against dictionary of common_words
4. backtracking: tests all possible keys for given length to find valid decryption
5. ioc analysis: calculates IoC to predict likely key length to prioritize testing


# Requirements

- python3 (3.7 or above)
- common_words.txt file containing common words, one word per-line, to later be converted to dictionary


# Usage

to run backtrack.py:  python3 backtrack.py
to run hash.py:       python3 hash.py

for both files, enter encrypted message when prompted -- the script will then attempt to decrypt and display the result, including the found key and decrypted text


# Example(s)

Enter the encrypted message: ______________

backtrack.py output:
Found valid decryption!
Key: '______________' | Decrypted Text: '________'
Decryption took ____ seconds

hash.py output:
Found valid decryption!
Key: '______________' | Decrypted Text: '________'
Decryption took ____ seconds


# Implementation Notes

backtrack.py
- strengths: straightforward, exhaustive, easy to understand
- limitations: inefficient for longer ciphertexts or large key spaces

hash.py:
- strengths: optimized for perfroamnce, reduces redundant key tests
- limitations: relies on IoC trhresholds, may skip valid keys if thresholds are off

# NOTE: 
for both , must ensure that the encrypted text (plaintext message) AND the key only contain words found in common_words.txt as the project is modified to only validate words found in the dictionary
