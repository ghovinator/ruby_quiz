#!/usr/bin/python

ones_and_teens = { 0: '',
                  1: 'one',
                  2: 'two',
                  3: 'three',
                  4: 'four',
                  5: 'five',
                  6: 'six',
                  7: 'seven',
                  8: 'eight',
                  9: 'nine',
                  10: 'ten',
                  11: 'eleven',
                  12: 'twelve',
                  13: 'thirteen',
                  14: 'fourteen',
                  15: 'fifthteen',
                  16: 'sixteen',
                  17: 'seventeen',
                  18: 'eighteen',
                  19: 'nineteen' }

ten_place = { 2: 'twenty',
              3: 'thirty',
              4: 'forty',
              5: 'fifty',
              6: 'sixty',
              7: 'seventy',
              8: 'eighty',
              9: 'ninety' }
                     
orders = ['', 'thousand', 'million', 'billion', 'trillion']

def print_to_hundreth(num, index=0):
    result_str = ''
    if num / 100:
        result_str += ones_and_teens[num / 100] + ' hundred '
    # check if i'm in the teens
    if (num % 100) in ones_and_teens:
        if num % 100:
            if result_str:
                result_str += 'and '
            result_str += ones_and_teens[(num % 100)]
    else:
        if result_str:
            result_str += 'and '
        result_str += ten_place[(num / 10) % 10]
        if num % 10:
            result_str += '-' + ones_and_teens[num % 10]
    return result_str.strip()

def number_to_word(num):
    results = []
    index = 0
    if num == 0:
        return 'zero'
    while(num):
        hundreth = num % 1000
        if index:
            result_str = print_to_hundreth(hundreth, index) + ' ' + orders[index]
        else:
            result_str = print_to_hundreth(hundreth, index)
        results.append(result_str)
        index += 1
        num /= 1000
    return ' '.join(reversed(results))

def is_odd(numeral):
    if not numeral:
        return False
    last_word = numeral.split()[-1]
    for num, num_str in ones_and_teens.iteritems():
        if last_word == num_str and num % 2:
            return True
    return False

def sort_english_numerals():
    numerals = []
    for i in range(10000000000):
        numerals.append(number_to_word(i))
    numerals.sort()
    for numeral in numerals:
        if is_odd(numeral):
            return numeral

def test():
    assert print_to_hundreth(100) == 'one hundred'
    assert print_to_hundreth(104) == 'one hundred and four'
    assert print_to_hundreth(64) == 'sixty-four'
    assert print_to_hundreth(20) == 'twenty'
    assert print_to_hundreth(17) == 'seventeen'
    print number_to_word(1003456)

test()
print sort_english_numerals()
