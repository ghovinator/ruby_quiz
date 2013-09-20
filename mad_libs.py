#!/usr/bin/python
import re

def get_ml_word(ml_string):
    """Takes input of ((foo:bar)) and returns a list of words
    in (()) separated by :"""
    ml_string = ml_string[2:-2]
    return [word.strip() for word in ml_string.split(':')]

def find_ml_strings(input):
    """Return list of all the ((foo:klsdjf)) in the input string"""
    result = []
    [result.append('((' + word[:word.index('))')] + '))')
     for word in input.split('((') if "))" in word]
    return result

def get_ml_input(ml):
    """Take a list of madlibs and ask the user via stdin to enter
    a replacement word. Return a dict keyed by madlibs and values from
    the user."""
    result = {}
    # can this be a list generator?
    for ml_word in ml:
        ml_word = get_ml_word(ml_word)
        if ml_word[0] not in result:
            result[ml_word[0]] = raw_input("%s:" %ml_word[1] if len(ml_word) == 2 else "%s:" %ml_word[0])
    return result

def replace_input_ml(input, ml_string, replace):
    """Takes original input, the list of mad libs in it and
    words to replace those mad libs with. Returns a string
    with the madlibs replaced."""
    for ml in ml_string:
        ml_word = get_ml_word(ml)
        replace_word = replace[ml_word[0]]
        input = input.replace(ml, replace_word)
    return input


def driver():
    """Driver that runs the mad libs program."""
    input = raw_input("Please enter the madlib string:")
    ml_strings = find_ml_strings(input)
    ml_replace = get_ml_input(ml_strings)
    print replace_input_ml(input, ml_strings, ml_replace)

def test():
    """Simple test to make sure mad libs semi works."""
    input = "This is ((amazing)) if ((done correctly)) right on ((do:doo)) ((do))"
    ml_string = find_ml_strings(input)
    assert ml_string == ["((amazing))", "((done correctly))", "((do:doo))", "((do))"]
    replace_word = {'do': "bugger", 'done correctly': "really", "amazing": "right" }
    assert replace_input_ml(input, ml_string, replace_word) == \
        "This is right if really right on bugger bugger"
    
if __name__ == "__main__":
    driver()
    #test()
