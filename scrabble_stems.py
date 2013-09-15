#! /usr/bin/python
from optparse import OptionParser
from collections import defaultdict
import pdb

pathname = "/home/ricky/scowl-7.1/final/"
alpha = "abcdefghijklnmopqrstuvwxyz"

def get_words_of_length(word_list, length=7):
    words = []
    [words.append(word.lower()) for word in word_list if "'" not in word and len(word) == length]
    return words

def scrabble_stems(word_list, n):
    # sort list to make it easier to check
    word_list = map(lambda x: ''.join(sorted(x)), word_list)
    length_seven_words = get_words_of_length(word_list)
    holder = defaultdict(dict)
    for word in length_seven_words:
        for letter in word:
            steam = word.replace(letter, '')
            holder[steam][letter] = True
    # use a list instead of dict for easier sorting, elements
    # are (k,len(v)) of the dict
    results = []
    for k, v in holder.iteritems():
        if len(v.keys()) >= n:
            results.append((k, len(v.keys())))
    results = sorted(results, key=lambda x: x[1], reverse=True)
    for result in results:
        print "Steam %s: count %d" %result

def main():
    usage = "usage: %prog filename [options]"
    parser = OptionParser(usage)
    parser.add_option("-n", dest="n", help="cutoff")

    (options, args) = parser.parse_args()
    if not options.n:
        options.n = 1
    word_file = open(pathname + args[0])
    word_list = map(lambda x: x.strip("\n"),word_file.readlines())
    word_file.close()
    scrabble_stems(word_list, int(options.n))
    
if __name__ == "__main__":
    main()
