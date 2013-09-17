#!/usr/bin/python
import random
class LanguageFilter:
    def __init__(self, banned_words):
        self.banned_words = sorted(banned_words)
        self.clean_calls = 0

    def is_clean(self, text):
        self.clean_calls += 1
        if isinstance(text, str):
            text = text.split()
        for word in text:
            if word in self.banned_words:
                return False
        return True
    
    def verify(self, words):
        return True if sorted(words) == self.banned_words else False

filter = LanguageFilter(["six"])
assert not filter.is_clean("I'll be home at six")
assert filter.is_clean("Do not taunt the happy fun ball!")
assert not filter.verify("ball")
assert filter.clean_calls == 2

def populate_word_list(size):
    f = open("/usr/share/dict/words")
    word_set = set()
    for word in f.readlines():
        word_set.add(word.lower().strip())
        if len(word_set) == size:
            break
    f.close()
    return list(word_set)

def divide_and_conquer(language_filter, words):
    def helper(check):
        if len(check) < 2:
            return check
        mid = len(check) / 2 
        left = check[:mid]
        right = check[mid:]
        result = []
        if not language_filter.is_clean(left):
            result.extend(helper(left))
        if not language_filter.is_clean(right):
            result.extend(helper(right))
        return result
    banned_words = helper(words)
    return language_filter.verify(banned_words)

def brute_force(language_filter, words):
    banned_words = []
    for word in words:
        if not language_filter.is_clean(word):
            banned_words.append(word)
    return language_filter.verify(banned_words)

def test(find_banned_words, word_size, banned_size):
    words = populate_word_list(word_size)
    words.sort()
    banned_words = list(set([random.choice(words) for i in range(banned_size)]))
    test_filter = LanguageFilter(banned_words)
    assert find_banned_words(test_filter, words)
    print test_filter.clean_calls


test(brute_force, 10000, 1000)
test(divide_and_conquer, 10000, 1000)
