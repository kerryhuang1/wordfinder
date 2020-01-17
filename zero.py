import random
import string

with open('word_dictionary.txt') as word_file:
    allwords = set(word_file.read().split())

min_dfs_length, max_dfs_length = 2, 10  
possible_dfs_words = set(word for word in allwords if min_dfs_length <= len(word) <= max_dfs_length)
valid_dfs_prefixes = set(word[:size] for word in possible_dfs_words for size in range(1, len(word)))

commons = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'D', 'H', 'U']