#! /usr/bin/python
from pymongo import MongoClient

db = MongoClient().animal_quiz
questions = db.questions

def insert_question_helper(question, y=None, n=None, animal=False, update=False):
    if update:
        questions.update({"question": question}, {"$set": {"y": y, "n": n}})
    else:
        questions.insert({"question": question, "y": y, "n": n, "animal": animal})

def insert_question(question, y_or_n=None, user_input=None, animal=False, update=False):
    if user_input:
        if user_input == "y":
            insert_question_helper(question, y=y_or_n, animal=animal, update=update)
        else:
            insert_question_helper(question, n=y_or_n, animal=animal, update=update)
    else:
        insert_question_helper(question, animal=animal)

def get_animal_from_question(question):
    words = question["question"].split()
    return words[-2] + " " + words[-1][:-1]

def ask_for_help(question):
    animal = raw_input("You win.  Help me learn from my mistake before you go... What animal were you thinking of?\n")
    follow_question = raw_input("Give me a question to distinguish %s from %s.\n" % (animal, get_animal_from_question(question)))
    answer = raw_input("For %s, what is the answer to your question?  (y or n)\n" % animal)
    animal_question = "Is it %s?" % animal
    insert_question(animal_question, animal=True)
    insert_question(follow_question, y_or_n=animal_question, animal=False,
                    user_input=answer)
    insert_question(question["question"], y_or_n=follow_question,
                    user_input="n", update=True)
    print "Thanks."

def main():
    print "Think of an animal..."
    while(True):
        current_question = questions.find_one({"question": "Is it an elephant?"})
        while(True):
            user_input = raw_input(current_question["question"] + "  (y or n)\n")
            # assume good 
            if current_question[user_input]:
                current_question = questions.find_one({"question": current_question[user_input]})
            else:
                if current_question["animal"]:
                    if user_input == 'y':
                        print "I win.  Pretty smart, aren't I?"
                        break
                ask_for_help(current_question)
                current_question = questions.find_one({"question": "Is it an elephant?"})
                break
        if (raw_input("Play again?  (y or n)\n") == "n"):
            break

if __name__ == "__main__":
    main()
