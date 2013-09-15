#!/usr/bin/python
import re

class Highline:
    def __init__(self):
        pass

    def __check_int(self, input, range=None):
        if not range:
            return input
        if input >= range[0] and input < range[-1]:
            return input
        else:
            raise ValueError("Incorrect int: not in range %d to %d" %(range[0], range[-1]))

    def __check_str(self, input, validate=None):
        if not validate:
            return input
        if re.match(validate, input):
            return input
        else:
            raise ValueError("Incorrect string")

    def __check_input(self, input, kind, args):
        if kind == int:
            return self.__check_int(input, **args)
        elif kind == str:
            return self.__check_str(input, **args)

    def prompt(self, display, kind, **args):
        while(True):
            answer = raw_input(display)
            try:
                answer = kind(answer)
            except ex:
                print "Incorrect value"
                continue
            try:
                self.__check_input(answer, kind, args)
                return answer
            except ValueError, ex:
                if ex.args:
                    print args[0]
                else:
                    print "Sorry invalid input"

    def prompt_if(self, question, kind=str, validate=None):
        answer = self.prompt(question, kind, validate=validate)
        if answer[0] == 'y' or answer[0] == 'Y':
            return True
        else:
            return False


def test():
    highline = Highline()
    print highline.prompt("Enter your age please: ", int,
                          range=(0,30))
    print highline.prompt_if("Would you like to continue?")


if __name__ == "__main__":
    test()
