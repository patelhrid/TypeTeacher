"""TypeTeacher Main File"""
from tkinter import *
import csv
from typing import Optional
import random


class App:
    """Class for the TypeTeacher app"""
    window: Tk
    tests: dict
    # background: str
    confirm_window: Optional[Tk]
    medium_allowed: bool
    hard_allowed: bool
    streak: int
    current_level: str
    input: StringVar
    current_test: str

    def __init__(self):
        self.window = Tk()
        # self.window['background'] = '#323232'
        # self.background = '#323232'
        self.window.title('TypeTeacher')
        self.window.geometry("800x800+320+10")
        self.tests = read_data('data.csv')
        start_button = Button(self.window, text='START', font=("Arial Bold", 20), command=self.start)
        start_button.place(x=345, y=300)
        self.confirm_window = None
        self.medium_allowed = False
        self.hard_allowed = False
        self.streak = 0
        self.current_level = 'Easy'
        self.input = StringVar()
        self.current_test = ''
        self.window.mainloop()

    def start(self) -> None:
        """Start the program"""
        self.clear()
        self.add_home()
        label = Label(self.window, text='Pick a difficulty level.', font=("Arial Bold", 20))
        label.place(x=300, y=200)
        easy = Button(self.window, text='Easy', font=("Arial", 20), command=self.easy)
        easy.place(x=250, y=300)
        if not self.medium_allowed:
            medium = Button(self.window, text='Medium', font=("Arial", 20), command=self.medium, fg='grey')
        else:
            medium = Button(self.window, text='Medium', font=("Arial", 20), command=self.medium)
        medium.place(x=345, y=300)
        if not self.hard_allowed:
            hard = Button(self.window, text='Hard', font=("Arial", 20), command=self.hard, fg='grey')
        else:
            hard = Button(self.window, text='Hard', font=("Arial", 20), command=self.hard)
        hard.place(x=470, y=300)

    def easy(self) -> None:
        """Easy difficulty"""
        self.current_level = 'Easy'
        self.begin_test()

    def test(self) -> None:
        """Begin a test based on self.current_level"""
        self.clear()
        self.add_home()
        picked_test = self.pick_test()
        self.current_test = picked_test
        self.display_test(picked_test)
        type_window = Entry(self.window, textvariable=self.input, highlightthickness=2)
        type_window.configure(highlightbackground="red", highlightcolor="red", width=50)
        type_window.place(x=170, y=470)
        submit = Button(self.window, text='SUBMIT', font=("Arial Bold", 20), command=self.submit)
        submit.place(x=340, y=500)

    def display_test(self, picked_test: str) -> None:
        """Display <picked_test> on multiple lines."""
        multiplier = 0
        remaining = picked_test
        while remaining != '':
            count = 0
            to_place = ''
            while count < 100:
                if remaining != '':
                    if 90 < count < 100 and remaining[0] == ' ':
                        to_place += remaining[0]
                        remaining = remaining[1:]
                        count = 100
                    else:
                        to_place += remaining[0]
                        remaining = remaining[1:]
                        count += 1
                else:
                    count = 100
            test = Label(self.window, text=to_place, font=("Arial", 16))
            test.place(x=10, y=50 + (multiplier * 25))
            multiplier += 1

    def submit(self) -> None:
        """Submit the entered text and evaluate the accuracy"""
        self.clear()
        self.add_home()
        answer = self.input.get()
        total = len(self.current_test)
        correct = 0
        if len(answer) == len(self.current_test) or len(answer) > len(self.current_test):
            for i in range(len(self.current_test)):
                if self.current_test[i] == answer[i]:
                    correct += 1
        elif len(answer) < len(self.current_test):
            for i in range(len(answer)):
                if self.current_test[i] == answer[i]:
                    correct += 1
        self.input = StringVar()
        accuracy = correct / total * 100
        label1 = Label(self.window, text='Accuracy: ' + str(round(accuracy, 2)) + '%',
                       font=("Arial Bold", 24), fg='red')
        label1.place(x=300, y=100)
        if round(accuracy) > 90:
            self.streak += 1
            if self.streak < 3:
                label3 = Label(self.window, text='Current streak: ' + str(self.streak) + '!',
                               font=("Arial Bold", 24), fg='red')
                label3.place(x=290, y=200)
                button = Button(self.window, text='Next Test', font=("Arial Bold", 20), command=self.begin_test)
                button.place(x=335, y=300)
                label2 = Label(self.window, text='Get a streak of 3 to proceed to the next level.',
                               font=("Arial Bold", 16))
                label2.place(x=235, y=500)
            else:
                label3 = Label(self.window, text='Easy: Completed!', font=("Arial Bold", 24), fg='red')
                label3.place(x=310, y=200)
                button = Button(self.window, text='Go Home', font=("Arial Bold", 20), command=self.go_home)
                button.place(x=350, y=300)
                if not self.medium_allowed:
                    self.medium_allowed = True
                elif not self.hard_allowed:
                    self.hard_allowed = True
        else:
            self.streak = 0
            label4 = Label(self.window, text='Current streak: ' + str(self.streak) + '!',
                           font=("Arial Bold", 24), fg='red')
            label4.place(x=290, y=200)
            button = Button(self.window, text='Try Again', font=("Arial Bold", 20), command=self.begin_test)
            button.place(x=320, y=300)
            label2 = Label(self.window, text='Get a streak of 3 to proceed to the next level.',
                           font=("Arial Bold", 16))
            label2.place(x=235, y=500)

    def pick_test(self) -> str:
        """Pick a test based on self.current_level"""
        if self.current_level == 'Easy':
            random_choice = random.choice(list(self.tests.keys()))
            while float(random_choice) > 2.0:
                random_choice = random.choice(list(self.tests.keys()))
            return self.tests[random_choice]
        elif self.current_level == 'Medium':
            random_choice = random.choice(list(self.tests.keys()))
            while float(random_choice) > 3.5 or float(random_choice) < 2.0:
                random_choice = random.choice(list(self.tests.keys()))
            return self.tests[random_choice]
        elif self.current_level == 'Hard':
            random_choice = random.choice(list(self.tests.keys()))
            while float(random_choice) < 3.5:
                random_choice = random.choice(list(self.tests.keys()))
            return self.tests[random_choice]

    def begin_test(self) -> None:
        """Begin test page"""
        self.clear()
        self.add_home()
        label = Label(self.window, text='Press begin when you are ready. Press submit once you\'re done.',
                      font=("Arial", 20))
        label.place(x=120, y=100)
        label2 = Label(self.window, text='The test will begin immediately.', font=("Arial Bold", 20))
        label2.place(x=247, y=140)
        begin = Button(self.window, text='BEGIN', font=("Arial Bold", 20), command=self.test)
        begin.place(x=350, y=200)

    def medium(self) -> None:
        """Medium difficulty"""
        if self.medium_allowed:
            self.current_level = 'Medium'
            self.begin_test()
        else:
            temp = Tk()
            temp.title('Not so fast!')
            temp.geometry("400x100+500+300")
            label = Label(temp, text='This difficulty is locked!', font=("Arial Bold", 18))
            label.place(x=94, y=10)
            label2 = Label(temp, text='Complete lower difficulties to continue.', font=("Arial", 14))
            label2.place(x=80, y=50)

    def hard(self) -> None:
        """Hard difficulty"""
        if self.hard_allowed:
            self.current_level = 'Hard'
            self.begin_test()
        else:
            temp = Tk()
            temp.title('Not so fast!')
            temp.geometry("400x100+500+300")
            label = Label(temp, text='This difficulty is locked!', font=("Arial Bold", 18))
            label.place(x=94, y=10)
            label2 = Label(temp, text='Complete lower difficulties to continue.', font=("Arial", 14))
            label2.place(x=80, y=50)

    def clear(self) -> None:
        """Clear all widgets"""
        for widgets in self.window.winfo_children():
            widgets.destroy()

    def add_home(self) -> None:
        """Add a home button in the top left"""
        button = Button(self.window, text='Home', font=("Arial Bold", 14), command=self.confirm)
        button.place(x=10, y=10)

    def confirm(self) -> None:
        """Confirm whether the user wants to go home"""
        self.confirm_window = Tk()
        self.confirm_window.title('Go home?')
        self.confirm_window.geometry("400x100+500+300")
        label = Label(self.confirm_window, text='Are you sure you want to return home?')
        label.place(x=77, y=0)
        label2 = Label(self.confirm_window, text='Progress at this difficulty level will be lost.',
                       fg='red', font=("Arial Bold", 14))
        label2.place(x=57, y=25)
        yes_button = Button(self.confirm_window, text='Yes', font=("Arial Bold", 14), command=self.go_home)
        yes_button.place(x=135, y=50)
        no_button = Button(self.confirm_window, text='No', font=("Arial Bold", 14), command=self.cancel_go_home)
        no_button.place(x=205, y=50)
        self.confirm_window.mainloop()

    def cancel_go_home(self) -> None:
        """Close the go home confirmation window."""
        self.confirm_window.destroy()
        self.confirm_window = None

    def go_home(self) -> None:
        """Return to the home GUI"""
        self.confirm_window.destroy()
        self.input = StringVar()
        self.current_test = ''
        self.streak = 0
        self.clear()
        start_button = Button(self.window, text='START', font=("Arial Bold", 20), command=self.start)
        start_button.place(x=345, y=300)


def read_data(file_name: str) -> dict:
    """Read the tests in <file_name> and return a dictionary mapping of the difficulty of
    the test to the test and its length"""
    with open(file_name) as file:
        reader = csv.reader(file)
        mapping = {}
        for row in reader:
            mapping[row[1]] = row[0]
    return mapping


if __name__ == '__main__':
    app = App()
