#!/usr/bin/python
from optparse import OptionParser

number_dict = {'2': 'ABC',
               '3': 'DEF',
               '4': 'GHI',
               '5': 'JKL',
               '6': 'MNO',
               '7': 'PQRS',
               '8': 'TUV',
               '9': 'WXYZ'}

default_dictionary = "/home/ricky/scowl-7.1/final/american-words.95"

def get_word_dictionary(dictionary):
    try:
        if dictionary:
            df = open(dictionary)
        else:
            df = open(default_dictionary)
    except IOError:
        print "Bad dictionary file"
        exit(1)
    lines = map(lambda x: x.strip("\n").upper(), df.readlines())
    df.close()
    return lines

def break_word(word, min_length=2):
    return [(word[:length], word[length:]) for length in range(min_length, len(word)) if len(word) - length >= min_length]
        

def create_word(number, dict_list):
    number = [letter for letter in number if letter.isdigit()]
    if len(number) != 7:
        return []
    result = []
    for first in number_dict[number[0]]:
        for second in number_dict[number[1]]:
            for third in number_dict[number[2]]:
                for fourth in number_dict[number[3]]:
                    for five in number_dict[number[4]]:
                        for sixth in number_dict[number[5]]:
                            for seventh in number_dict[number[6]]:
                                word = first + second + third + fourth + five + sixth + seventh
                                if word in dict_list:
                                    result.append(word)
                                for word1, word2 in break_word(word):
                                    if word1 in dict_list and word2 in dict_list:
                                        result.append(word1 + "-" + word2)
    return result

                            

def driver():
    usage = "usage: %prog filename [options]"
    parser = OptionParser(usage)
    parser.add_option("-d", dest="dictionary", help="dictionary to use")
    
    (option, args) = parser.parse_args()
    # get word list
    word_list = get_word_dictionary(option.dictionary)
    if not args:
        while(True):
            number = raw_input('Number(blank to exit): ')
            if not number:
                break
            for word in create_word(number, word_list):
                print word
    else:
        try:
            input_file = open(args[0])
            for number in input_file:
                for word in  create_word(number, word_list):
                    print word
            input_file.close()
        except IOError:
            print "Bad file given"
        
        
        
if __name__ == "__main__":
    driver()
