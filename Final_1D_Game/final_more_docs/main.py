import random
import math
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
from math_questions import *


def _clear_screen():
    """
    OS independent method of clearing the terminal.

    Credits
    -------
    https://stackoverflow.com/questions/2084508/clear-terminal-in-python

    """
    os.system("cls" if os.name in ("nt", "dos", "ce") else "clear")


def delay_print(s):
    """
    Pretty print strings character by character! Fabulous!

    Parameters
    ----------
    s: str
        String to print slowly.

    Credits
    -------
    https://stackoverflow.com/questions/9246076/how-to-print-one-character-at-a-time-on-one-line

    """
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.03)

# ========== Game Classes ========== 
class Question(object):
    """ 
    This is a class that can parse each question in the JSON file, returning an easy to work with Question object.

    A question consists of 3 forms in the json file:
    Form 1: Randomly generated answer (based on the ranges set)
        {"question": "<question statement>",
        "callback_func": "<func>",
        "question_type": "dynamic",
        "answer_type": "mcq/open",
        "args_ranges": [ ["int/float", start, stop], ["int/float", start, stop], ...]
        }
    Form 2: Static/Fixed answer MCQ
        {"question": "<question statement>",
        "callback_func": "<func>",
        "question_type": "static",
        "answer_type": "mcq",
        "options": [<option_1>, <option_2>, <option_3>, <option_4>]
        }
    Form 3: Static/Fixed answer Open Ended Question
        {"question": "<question statement>",
        "callback_func": "<func>",
        "question_type": "static",
        "answer_type": "open",
        "answer": "<answer>" 
        }
    
    Methods
    ------- 
    get_question(self): dictionary 
        Dictionary contains keys "question", a str, and "options" as tuple if question type is MCQ.
        Dictionary contains only "question" key if question type if Open.

    check_answer(self, guess): Bool
        Checks if answer matches that of the options.
    """
    def __init__(self, question, options, answer):
        """ 
        Parameters
        ---------- 
        question: str
            This is the question prompt that is given to the player.
        options: list
            Represents the options given the player if available, else will be an empty list.
        answer: str
            The correct answer to the question. This will be a string from 1 to 4 in the case of MCQs, and for open-ended questions, this will be the correct answer string.
        """
        self.question = question 
        self.options = options 
        self.answer = answer 
        if len(self.options) == 0:
            self.question_type = "open"
        else:
            self.question_type = "mcq"

    @staticmethod
    def _parse_random_rng(args_ranges):
        """ 
        Helper function that parses the list of return number types and their ranges, for the callback functions to use as input.

        Parameters
        ----------
        args_ranges: list
            List of form [[val_type, (start, end)], ...], representing type of RNG return value and ranges, where val_type is either int or float. 
            E.g [["float", [1.0, 2.3]], ["int", [1, 10]], ["float", [1.0, 100]]]

        Returns
        -------
        random_inputs: list
            List of random integers or floats generated based on the ranges
            E.g [1.3, 2, 10.1]
        """
        random_inputs = []
        for rng_type, val_range in args_ranges:
                if rng_type == "int":
                    random_inputs.append(random.randint(*map(int, val_range)))
                else:  
                    random_inputs.append(round(random.uniform(*val_range), 2))
        return random_inputs


    @classmethod
    def from_dynamic(cls, full_question):
        """ 
        Constructor for dynamic questions.

        Parameters:
        -----------
        cls: Current Question Class

        full_question: dictionary
            Dictionary containing a question of the appropriate form for a dynamic MCQ/Open Ended question.

        Returns
        ------- 
        Question
            Question object that stores the question, options and answer.

            The question is a string that stores the randomly geenerated question.

            Options is an empty array if answer type is open, else it will be an array of 4 options.

            If answer type is open, answer is a string representing the correct answer. 
            If the answer type is MCQ, answer is a string that stores a number from 1 to 4 representing the correct option. 
        """
        random_inputs = Question._parse_random_rng(full_question["args_ranges"])  # _parse_random_rng need change
        question = full_question["question"]
        answer = str(globals()[full_question["callback_func"]](*random_inputs))
        options = []
        if full_question["answer_type"] == "mcq":
            options.append(answer)
            for _ in range(3):  
                other_random_inputs = Question._parse_random_rng(full_question["args_ranges"])
                other_ans = str(globals()[full_question["callback_func"]](*other_random_inputs))
                options.append(other_ans)
            random.shuffle(options)
            answer = str(options.index(answer) + 1)
        return cls(question.format(*random_inputs), options, answer) 

    @classmethod
    def from_static(cls, full_question):
        """
        Constructor for static questions.

        Parameters:
        -----------
        cls: Current Question Class

        full_question: dictionary
            Dictionary containing a question of the appropriate form for a static MCQ/Open Ended question.

        Returns
        ------- 
        Question
            Question object that stores the question, options and answer.

            The question is a string that stores the randomly geenerated question.

            Options is an empty array if answer type is open, else it will be an array of 4 options. Options will be read from the "options" key in the full_question dictionary if available.

            If answer type is open, answer is a string representing the correct answer. This will be read from the "answer" key in the full_question dictionary.
            If the answer type is MCQ, answer is a string that stores a number from 1 to 4 representing the correct option. This will be read from the "answer" key in the full_question dictionary.
        """
        question = full_question["question"]
        options = []
        answer = full_question["answer"]
        if full_question["answer_type"] == "mcq":
            options = full_question["options"]
            random.shuffle(options)
            answer = str(options.index(answer) + 1)
        return cls(question, options, answer)

    def get_question(self):
        if self.question_type == "open":
            return {"question": self.question}
        return {"question": self.question, "options": self.options}

    def get_question_type(self):
        return self.question_type

    def check_answer(self, guess):
        guess = guess.lower().strip()
        return self.answer == guess


class Game(object):
    """ Class for each game/round of the game.

    Methods
    -------
    get_score(self): int
        Getter method for getting the total score in the current game.

    calculate_grades(self): Bool
        Prints the congratulatory messages/taunt messages. Returns if player passed or fail.

    end_game(self): None
        Called when the game ends.

    qn_check(self, correct): None
        Called by update to check if the player answer is correct. Increments the score and prints the statements. 

    update(self): None
        Main method of the Game class which is called on every question.
    """
    def __init__(self, total_qns):
        """
        Parameters
        ---------- 
        total_qns: int
            Total number of questions in one round of the game.
        """
        self.score = 0
        self.total_qns = total_qns
        self.qn_nos = random.sample([str(i) for i in range(1, len(QN_ANS) + 1)], total_qns)
        self.ans = None

    def get_score(self):
        return self.score

    def calculate_grades(self):
        """
        Calculates the player's grade and prints the relevant statements to congratulate/insult them.

        Returns:
        --------
        player_pass: Bool
            Represents if player passed or failed.
        """
        delay_print('''Calculating your final grade....
        ....
        ....
        ....\n''')
        total_score=self.score/self.total_qns*100

        player_pass = None
        if total_score>=70:
            delay_print(f"You got {total_score}%! Chief, you dropped your crown\n\n")
            print(r'''.
                  .       |         .    .
            .  *         -*-          *
                 \        |         /   .
.    .            .      /^\     .              .    .
   *    |\   /\    /\  / / \ \  /\    /\   /|    *
 .   .  |  \ \/ /\ \ / /     \ \ / /\ \/ /  | .     .
         \ | _ _\/_ _ \_\_ _ /_/_ _\/_ _ \_/
           \  *  *  *   \ \/ /  *  *  *  /
            ` ~ ~ ~ ~ ~  ~\/~ ~ ~ ~ ~ ~ '
''')
            player_pass = True
        
        elif total_score>=50:
            delay_print(f"You got {total_score}%...")
            delay_print(random.choice(PASS))
            player_pass = True 
        else:
            delay_print(f"You got {total_score}%...")
            delay_print(random.choice(FAIL))
            player_pass = False 
        return player_pass

    def end_game(self):
        """
        Called when the game ends.

        Returns
        -------
        Bool
            Bool returned by calculate_grades which represents if the player passes or fails the game.
        """
        
        print(f"Final score is {self.score} out of {self.total_qns}.")
        input()
        return self.calculate_grades()

    def qn_check(self, correct):
        """
        Called by update to check if the player answer is correct. Increments the score and prints the relevant statements.
        
        Parameters
        ----------
        correct: Bool
            Represents if the player passes or fails the game.
        """

        if correct:
            self.score += 1
            print(random.choice(ENCOURAGEMENTS))
            print(r'''
                     _
                    ( ((
                     \ =\
                 __\_ `-\ 
                (____))(  \------
                (____)) _  
                (____))
                (____))____/----
                ''')

        else:
            print(random.choice(TAUNTS))
            print(r'''   
                   ______
                 (( ____ \---
                 (( _____
                 ((_____ 
                 ((____   ----
                      /  /
                     (_((
                ''')

        print(f"Current Score is {self.score}")
        print("-=" * 20)
        input()

    def update(self):
        """
        Main method of the Game class which is called on every question. Will get inputs.
        """
        if len(self.qn_nos) == 0:
            end_game()
        curr_qn = QN_ANS[self.qn_nos.pop()]
        curr_qn_info = curr_qn.get_question()
        options = curr_qn_info.get("options")

        print(curr_qn_info["question"])
        if options is not None:
            print(MCQ_STRING.format(*options))

        player_input = input("Type your answer:\n")

        self.qn_check(curr_qn.check_answer(player_input))


# ========== Globals ========== 

MCQ_STRING = "1) {} 2) {} \n3) {} 4) {}\n"
qn_ans_path = os.path.join(os.getcwd(), "qn_ans.json")
TAUNTS = ["Haha try again n3rd", "Get r3kt", "Don't worry you TOTALLY got this!", "If Prof Matthieu can do it, I don't see why you couldn't?!", "If Prof Cyrille can do it, I don't see why you couldn't?!", "Dumbass. Read the f***ing textbook.", "Now I shall give you DEATH in return"]
ENCOURAGEMENTS = ["Nice work out there", "I always believed you were able to do it", "You're the best!", "Not bad. You got that one right.", "My analysis shows that you are AWESOME!"]
QN_ANS = {}
HIGH_PASS = []
PASS = ["Pass only but its ok cause its pass/fail.",
        "That feeling when you know that you’re gonna fail this sem but then you checked your grades and you actually PASSED…",
        "Congratulations, you have PASSED your vibe check!",
        "You shall.... not pass!!! Never mind...you PASSED!",
        "That AWESOME feeling when you PASSED your final exam!"
        ]
FAIL = ["YOU HAD ONE JOB! AND YOU FAILED!",
        "YOU HAVE FAILED YOUR MATH EXAM! UNPOSSIBLE.",
        "So you have failed! You’re not a failure!",
        "Bro...You failed! Outstanding!",
        "When you know you failed all your exams but at least it’s over!"]

if os.path.exists(qn_ans_path):
    with open(qn_ans_path) as in_file:
        input_json = json.load(in_file)
        for i, j in input_json.items():
            if j["question_type"] == "dynamic": 
                QN_ANS[i] = Question.from_dynamic(j)
            else:
                QN_ANS[i] = Question.from_static(j)
else:
    print("No json file detected, exitting with error")
    exit(1)


# ========== Main Game Loop ========== 

def main():
    total_qns = 10
    games = [Game(total_qns) for _ in range(3)]
    print(f"Here are your stats (out of {total_qns}):", [game.get_score() for game in games])

    start = time.time()
    _clear_screen()
    health = 3
    curr_round = 1
    bootcamp = True

    print(r'''
 _____ ____  _____ ____  _     _      ____  ____  _____  
/    //  __\/  __// ___\/ \ /|/ \__/|/  _ \/  __\/  __/  
|  __\|  \/||  \  |    \| |_||| |\/||| / \||  \/||  \    
| |   |    /|  /_ \___ || | ||| |  ||| \_/||    /|  /_   
\_/   \_/\_\\____\\____/\_/ \|\_/  \|\____/\_/\_\\____\  
                                                         
    ''')

    delay_print("=======================================================\n")
    
    print(r'''
  ____  _  _      _     _     ____  _____  ____  ____ 
/ ___\/ \/ \__/|/ \ /\/ \   /  _ \/__ __\/  _ \/  __\
|    \| || |\/||| | ||| |   | / \|  / \  | / \||  \/|
\___ || || |  ||| \_/|| |_/\| |-||  | |  | \_/||    /
\____/\_/\_/  \|\____/\____/\_/ \|  \_/  \____/\_/\_\
                                                     
    ''')
    delay_print("=======================================================\n")

    delay_print('''Hello….! Welcome to the Freshmore Simulator—
where we test and predict whether you'll need Bootcamp or not :”)\n\n''')

    username=input("Before we start, we need your name: ")

    delay_print(f'''\nHello {username}, welcome to Freshmore Term 1 Simulator! Today we'll test you on your Maths for a bit...''')

    delay_print('''\n\n. . .
. . .
. . .
Entering Game . . .
. . .
. . .\n\n''')

    print("Rules:\n1) Attempt all questions\n2) Don't cheat (or just don't get caught)\n3) All values are rounded to 2 decimal places, and vectors are represented in (x, y), spacing included.\n4) Click <ENTER> to get the next question")
    input()

    for game in games:
        health -= 1
        print(f"\n\n>WELCOME TO ROUND {curr_round}.\n")
        for game_no in range(total_qns):
            print(f"Question {game_no + 1}")
            game.update()
        print(f"\n>YOU'VE COMPLETED ROUND {curr_round}.\n")
        player_pass = game.end_game()
        input()
        _clear_screen()
        curr_round += 1

        if not player_pass:
            if health > 0:
                 delay_print(f"But it's okay, you have {health} health left, do you want to repeat or just go for Bootcamp now?")
                 repeat = input("\n1) Repeat \n2) Bootcamp\n")
                 while repeat not in ["1", "2"]:
                     print("You're getting on my nerves, be careful I don't send you to bootcamp!")
                     repeat=input("\n1) Repeat \n2) Bootcamp\n")
                 repeat = int(repeat)
                 if repeat == 1:
                     continue
                 if repeat == 2:
                     bootcamp = True
                     break
            else:
                 delay_print("It's okay, you have one last shot...\n at bootcamp</3")
                 bootcamp = True
                 break

    #bootcamp
    if bootcamp==True:
        delay_print("\n\nHello again... welcome to Bootcamp. ")
        delay_print("This is your last chance on passing term 1– all based on an all-or-nothing question... \nPerhaps the trickiest question of them all...")
        bootcamp_response = {"1": "Thanks Prof Matthieu for completing Bootcamp – but you failed.",
                             "2": "Thanks Prof Cyrille for completing Bootcamp – but you failed.",
                             "3": "\n\nMadlad ... you managed to pass via Bootcamp!",
                             "4": "\n\nIt's ok u tried but u still failed"}
        bootcamp_answer=input("\n\nWho is the best CTD prof?\n1)Prof Matthieu <3\n2)Prof Cyrille <3\n3)Both\n4)None of the above\n")
        while bootcamp_answer not in bootcamp_response:
            print("You can run, but you can't hide... Pick one of the options!")
            bootcamp_answer=input("\n\nWho is the best CTD prof?\n1)Prof Matthieu <3\n2)Prof Cyrille <3\n3)Both\n4)None of the above\n")
        delay_print(bootcamp_response[bootcamp_answer])

    #endgame
    delay_print("\n\n...\n....,\n.....\n......\n\n")
    end = time.time()
    time_taken=round(end - start,2)
    delay_print(f"Congratulations! You've just wasted {time_taken}s playing a stupid quiz game :D")
    print(r'''
     _  __   _____  _    ___  _   ____ ___  _ _____
    / |/ /  /__ __\/ \ /|\  \//  /  _ \\  \///  __/
    |   /     / \  | |_|| \  /   | | // \  / |  \  
    |   \     | |  | | || /  \   | |_\\ / /  |  /_ 
    \_|\_\    \_/  \_/ \|/__/\\  \____//_/   \____\
                                               
    ''')


if __name__ == "__main__":
    main()
