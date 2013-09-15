#!/usr/bin/python
import sys

def prep_message(message):
    converted_message = [letter.upper() for letter in message if letter.isalpha()]
    if len(converted_message) % 5:
        converted_message += ['X'] * (5 - (len(converted_message) % 5))
    result = []
    for i in range(len(converted_message) / 5):
        start = i * 5
        result.append(converted_message[start : start + 5])
    return result

def convert_message(messages, to_numbers=False):
    result = []
    for message in messages:
        if to_numbers:
            result.append([ord(letter) - 64 for letter in message])
        else:
            result.append([chr(int(number) + 64) for number in message])
    return result

def add_key_message(number_message, number_keystream, sub=False):
    result = []
    for nm, nk in zip(number_message, number_keystream):
        inner_result = []
        for mes, key in zip(nm, nk):
            if sub:
                if mes <= key:
                    inner_result.append(mes + 26 - key)
                else:
                    inner_result.append(mes - key)
            else:
                inner_result.append((key + mes) % 26)
        result.append(inner_result)
    return result

def move_joker(joker, count, keys):
    index = keys.index(joker)
    keys.remove(joker)
    wrap = index + count - len(keys)
    if wrap > 0:
        keys = keys[:wrap] + [joker] + keys[wrap:]
    else:
        keys = keys[:index + count] + [joker] + keys[index + count:]
    # make sure that keys is used in the output because we are
    # modifying it
    return keys

def triple_cut(keys):
    # max index should be plus 1 because it is everything passed it
    # min index is fine because it is everything up to it and 
    # splicing is always non inclusive of the end
    max_index = max(keys.index("A"), keys.index("B")) + 1
    min_index = min(keys.index("A"), keys.index("B"))
    return keys[max_index:] + keys[min_index:max_index] + keys[:min_index]

def card_value(card):
    if card == "A" or card == "B":
        return 53
    c, s = card[0], card[1]
    additive = 0
    if s == 'D':
        additive = 13
    elif s == 'H':
        additive = 26
    elif s == 'S':
        additive = 39
    val = 1 if c == "A" else\
          13 if c == "K" else\
          12 if c == "Q" else\
          11 if c == "J" else\
          10 if c == "T" else\
          int(c)
    return val + additive

def bottom_cut(keys):
    bottom = card_value(keys[-1])
    return keys[bottom:-1] + keys[:bottom] + [keys[-1]]

def find_output(keys):
    val = card_value(keys[0])
    output_val = card_value(keys[val])
    if output_val == 53:
        return ''
    return chr(64 + (output_val % 26))
    
def compute_solitaire(keys):
    keys = move_joker("A", 1, keys)
    keys = move_joker("B", 2, keys)
    keys = triple_cut(keys)
    keys = bottom_cut(keys)
    return find_output(keys), keys

def generate_keystream(messages):
    keys = [c + s for s in "CDHS" for c in "A23456789TJQK"]
    keys += ["A", "B"]    
    result = []
    for message in messages:
        inner_result = []
        for letter in message:
            outcome, keys = compute_solitaire(keys)
            while not outcome:
                outcome, keys = compute_solitaire(keys)
            inner_result.append(outcome)
        result.append(inner_result)
    return result

def encryption(original_message):
    # prep message, should trim the message
    messages = prep_message(original_message)
    # create keystream from message
    keystream = generate_keystream(messages)
    # convert message to numbers
    number_message = convert_message(messages, to_numbers=True)
    # convert keystream to numbers
    number_keystream = convert_message(keystream, to_numbers=True)
    # add message and keystream mod 26
    number_key_message = add_key_message(number_message, number_keystream)
    # convert back to letters
    output = convert_message(number_key_message)
    for message in output:
        print ''.join(message),
        print '',

def decryption(original_message):
    # maybe prep the og message somehow TODO
    messages = prep_message(original_message)
    # create keystream from message
    keystream = generate_keystream(messages)
    # convert message to numbers
    number_message = convert_message(messages, to_numbers=True)
    # convert keystream to numbers
    number_keystream = convert_message(keystream, to_numbers=True)
    # keystream - message: 1 - 22 = 5(27-22)
    number_key_message = add_key_message(number_message, number_keystream,
                                         sub=True)
    # convert back to letters
    output = convert_message(number_key_message)
    for message in output:
        print ''.join(message),
        print '',

def driver():
    if len(sys.argv) == 2:
        print "Error: Please provide a message and [encrypt|decrypt]."
        return
    if sys.argv[2] == "encrypt":
        encryption(sys.argv[1])
    else:
        decryption(sys.argv[1])

def test():
    assert [['H', 'E', 'L', 'L', 'O'], ['W', 'O', 'R', 'L', 'D']] == prep_message("hell233o wor____lD")
    assert convert_message([[8, 5, 12, 12, 15], [23, 15, 18, 12, 4]]) == \
    [['H', 'E', 'L', 'L', 'O'], ['W', 'O', 'R', 'L', 'D']]
    assert convert_message([['H', 'E', 'L', 'L', 'O'], ['W', 'O', 'R', 'L', 'D']], to_numbers=True) == [[8, 5, 12, 12, 15], [23, 15, 18, 12, 4]]
    assert add_key_message([[8, 5, 12, 12, 15], [23, 15, 20, 12, 4]],
                           [[8, 5, 12, 12, 15], [23, 15, 18, 14, 24]]) == \
        [[16, 10, 24, 24, 4], [20, 4, 12, 0, 2]]
    assert add_key_message([[8, 5, 12, 12, 15], [23, 15, 20, 12, 4]],
                           [[8, 5, 12, 12, 15], [23, 15, 18, 14, 24]],
                           sub=True) == \
        [[26, 26, 26, 26, 26], [26, 26, 2, 24, 6]]
    assert [['D', 'W', 'J', 'X', 'H'], ['Y', 'R', 'F', 'D', 'G'], ['T', 'M', 'S', 'H', 'P'], ['U', 'U', 'R', 'X', 'J']] == \
        generate_keystream([["C", "O", "D", "E", "I"],
                            ["N", "R", "U", "B", "Y"],
                            ["L", "I", "V", "E", "L"],
                            ["O", "N", "G", "E", "R"]])

    encryption("code in ruby live longer")
    print ''
    decryption("GLNCQ  MJAFF  FVOMB  JIYCB")
    

if __name__ == "__main__":
    #driver()
    test()
