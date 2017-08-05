import json, functools, argparse, os, string
from random import shuffle


class Quiz:
    _items = []

    #Builtins
    def __len__(self):
        return self.length()

    def __hash__(self):
        return functools.reduce(
            (lambda x, y: (x + y) % 30000),
            [self.get_question_hash(ind)
             for ind in range(len(self._items) - 1)])

    def __dict__(self):
        outputDict = {"type": "Quiz"}
        for i in range(self.length()):
            outputDict[i] = self._items[i]
        return outputDict

    #Get/Set
    def length(self):
        return len(self._items)

    def questions(self):
        return [question for question, __, __ in self._items]

    def answer_key(self):
        return [answer for __, __, answer in self._items]

    def add_question(self, question, answer, choices):
        if not isinstance(question, str) or not isinstance(answer, str):
            return False
        #Check if all answer choices are strings
        if not (functools.reduce((lambda x, y: x and y),
                                 map((lambda x: isinstance(x, str))))):
            return False
        if answer >= len(choices):
            return False
        self._items.append((question, answer, choices))
        return True

    def delete_question(self, index):
        if index > len(self._items) - 1 or index < 0 or len(self._items) == 0:
            return False
        self._items.__delitem__(index)
        return True

    def modify_question(self, index, question = "", answer = "", choices = []):
        if question != "":
            self._items[index][0] = question
        if answer != "":
            self._items[index][1] = answer
        if choices != []:
            self._items[index][2] = choices

    def get_question(self, index):
        return self._items[index]

    def get_prompt(self, index):
        return self._items[index][0]

    def get_answer(self, index):
        return self._items[index][1]

    def get_choices(self, index):
        return self._items[index][2]

    def get_question_hash(self, index):
        prompt = self._items[index][0]
        answer = self._items[index][1]
        choices = self._items[index][2]
        return (hash(prompt) + hash(answer) +
                functools.reduce(lambda x,y: x+y, map(hash, choices)))

    def grade(quiz, answers):
        return float(sum(map(
            (lambda qs, ans: qs[1] == ans),
            zip(quiz, answers)))) / float(len(quiz))

    #Utility
    def clear(self):
        self._items = []

    def shuffle(self):
        self._items = shuffle(self._items)

    def copy(self):
        outputQuiz = Quiz()
        outputQuiz._items = [item for item in self._items]
        return outputQuiz

    def json_serialize(self, quiz):
        return json.dump(dict(quiz))

    def json_import(self, json_str):
        jsn = json.load(json_str)
        if (jsn["type"].lower() == "quiz"):
            raise RuntimeError("Input type is not a quiz could not parse the"
                                + "input.")
        else:
            for question in jsn.values():
                if question.lower() != "quiz":
                    self.add_question(question[0], question[1], question[2])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", default="make", type=str, help="take, make, mod")
    parser.add_argument("file", default="", type=str, help="file to import quiz"
                                                            + "from")
    args = parser.parse_args()

    def query(text, choices =  [], xfm = str):
        not_confirmed = True
        choice_valid = True
        inp = ""
        while (not_confirmed and choice_valid):
            print(text)
            if len(choices) > 0 :
                inp = input("Choices: ".join(["\n".join(choices), "---------"]))
            else:
                inp = input("----------")
            print ("You entered: " + inp)
            confirm_inp = input("Are you satisfied with the current input"
                                    + "(Y/N)?")
            not_confirmed = not (confirm_inp.lower()[0] == "y")
            ret = xfm(inp)
            choice_valid = True if len(choices) == 0 else ret in choices
            if not choice_valid:
                print("Invalid option")
        return ret

    yes_resp_func = lambda x : (x.lower()[0] == "y")

    def write_string_to_file(s):
        try:
            if query("Do you want to output to a file (Y/N)",[], yes_resp_func):
                not_saved = True
                while not_saved:
                    filepath = query("Location to save file:",[],str)
                    if os.path.exists(filepath):
                        if query("Overwrite file? (Y/N)", [], yes_resp_func):
                            with open(filepath, "wt") as f:
                                f.write(s)
                            not_saved = False
                        else:
                            with open(filepath, "wt") as f:
                                f.write(s)
                            not_saved = False
                return True
            else:
                return False
        except IOError:
            print("IO Error writing to file")
            return False

    def get_choices():
        choices = []
        num_ans = query("How many possible responses?",[], int)
        while num_ans <= 0:
            print("Must have more than one choice")
            num_ans = query("How many possible responses?",[], int)
        for i in range(num_ans - 1):
            resp = query("Enter the text for this choice")
            choices.push(resp)
        return choices

    def create_question(quiz):
        question = query("Please enter a question for the quiz")
        print("The choices are")
        choices = get_choices()
        for choice in choices:
            print(choice)
        correct = query("Which choice is the correct choice?",
                        range[len(choices)], int)
        if quiz.add_question(question, choices, correct):
            print("Question added")
        else:
            print("Question not added")
        return quiz

    def display_question(quiz, index, disp_ans = False):
        print(str(index) + ". " + quiz.get_prompt(index))
        for i, choice in enumerate(quiz.get_choices(index)):
            print("\t" + string.ascii_lowercase[i] + ". " + str(choice))
        if disp_ans:
            print("Answer: " + quiz.get_answer(index))

    def modify_question(quiz, index):
        option = "m"
        cont = True
        # m -> default, p -> prompt, c -> choices, a -> answer
        while cont and option in ["m", "p", "c", "a", "q"]:
            display_question(quiz, index, True)
            option = query("Choose option: " +
                            "\np: Change the prompt" +
                            "\nc: Change the choices" +
                            "\na: Change the answer" +
                            "\nq: Stop modification",
                            ["p","c","a","q"])
            if option == "p":
                quiz.modify_question(index, question=query("New question:"))
            elif option == "c":
                quiz.modify_question(index, choices=get_choices())
            elif option == "a":
                quiz.modify_question(index,
                            answer=query("Which choice is the correct choice?",
                                    range(len(quiz.get_choices(index))), int))
            elif option == "q":
                cont = False

    quiz = Quiz()

    #Prepare Quiz
    if (args.file != ""):
        with open(args.file, "r") as inp_file:
            jsn = inp_file.read()
        quiz.json_import(jsn)
        print("Quiz loaded from file")


    if (args.mode == "make"):
        if len(quiz) > 0:
            args.mode = "mod"
            print("Cannot create a new quiz when one is loaded, switching to " +
                  "modification mode")
        else:
            print("Creating a new quiz")
            more_questions = True
            while (more_questions):
                create_question(quiz)
                more_questions = query("Are there more questions? (Y/N)",[],
                                    yes_resp_func)
            #Output
            write_string_to_file(quiz.json_serialize())

    #Modify quiz
    if (args.mode == "mod"):
        current_question = 0
        while current_question >= 0:
            display_question(quiz, current_question, True)
            option = query("Choose option:"+
                           "\nn: Next question" +
                           "\np: Previous question" +
                           "\nd: Delete question"  +
                           "\na: Add new question" +
                           "\nm: Modify question" +
                           "\nq: Quit", ["n", "p", "d", "a", "m", "q"])
            if option == "n":
                if (current_question <= len(quiz)):
                    current_question += 1
                else:
                    print("No more questions remain in the quiz.")
            elif option == "p":
                if (current_question >= 0):
                    current_question -= 1
                else:
                    print("Cannot move backwards any further")
            elif option == "d":
                quiz.delete_question(current_question)
                print("Question deleted")
                current_question -= 1 if current_question > 0 else 0
            elif option == "a":
                create_question(quiz)
                current_question += 1
            elif option == "m":
                modify_question(quiz, current_question)
            elif option == "q":
                current_question = -1
        write_string_to_file(quiz.json_serialize())



    #Run quiz
    if args.mode == "take":
        if query("Shuffle quiz? (Y/N)", [], yes_resp_func):
            quiz.shuffle()
        quiz_answers = [-1] * len(quiz)
        current_question = 0
        while current_question >= 0:
            display_question(quiz, current_question)
            print("Your answer is: " +
                "Unselected" if quiz_answers[current_question] == -1 else
            quiz.get_choices(current_question)[quiz_answers[current_question]])
            option = query("Choose option:" +
                        "\na: Answer question" +
                       "\nn: Next question" +
                       "\np: Previous question" +
                       "\nq: Finish quiz", ["a", "n", "p", "q"])
            if option == "a":
                quiz_answers[current_question] = query("Answer choice: ",
                                range(len(quiz.get_choices(current_question))),
                                 int)
                if current_question >= len(quiz):
                    print("at the end of the quiz")
                    if query("Would you like to grade your quiz? (Y/N)",
                        xfm=yes_resp_func):
                        break
                else:
                    current_question += 1
            elif option == "n":
                if current_question >= len(quiz):
                    print("At end of quiz")
                    if query("Would you like to grade your quiz? (Y/N)",
                            xfm=yes_resp_func):
                        break
                else:
                    current_question += 1
            elif option == "p":
                if current_question <= 0:
                    print("At the beginning of the quiz")
                    if query("Would you like to grade your quiz? (Y/N)",
                            xfm=yes_resp_func):
                        break
                else:
                    current_question -= 1
            elif option == "q":
                break
        grade = quiz.grade(quiz_answers) * 100
        print("Score is " + str(grade))
        output_dict = dict(quiz_answers)
        output_dict["score"] = grade
        write_string_to_file(json.dump(output_dict))











