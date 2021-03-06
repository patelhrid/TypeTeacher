"""TypeTeacher Main File"""
from tkinter import *
import csv
from typing import Optional
from PIL import Image, ImageTk
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

    # Initialize the application window
    def __init__(self):
        self.window = Tk()
        self.window.title('TypeTeacher')
        self.window.geometry("800x800+320+10")
        self.tests = read_data('data.csv')
        start_button = Button(self.window, text='START', font=("Proxima Nova Bold", 20), command=self.start_day)
        start_button.place(x=345, y=300)
        self.confirm_window = None
        self.medium_allowed = False
        self.hard_allowed = False
        self.streak = 0
        self.current_level = 'Easy'
        self.input = StringVar()
        self.current_test = ''
        img = ImageTk.PhotoImage(Image.open("Untitled-1.png").resize((570, 200)))
        panel = Label(self.window, image=img)
        panel.pack()
        self.day_night = 'day'
        self.window.mainloop()

    # Start the application window in day mode
    def start_day(self) -> None:
        """Start the program"""
        self.clear()
        self.add_home()
        label = Label(self.window, text='Pick a difficulty level.', font=("Proxima Nova Bold", 20))
        label.place(x=300, y=200)
        easy = Button(self.window, text='Easy', font=("Proxima Nova Regular", 20), command=self.easy)
        easy.place(x=250, y=300)
        if not self.medium_allowed:
            medium = Button(self.window, text='Medium', font=("Proxima Nova Regular", 20), command=self.medium, fg='grey')
        else:
            medium = Button(self.window, text='Medium', font=("Proxima Nova Regular", 20), command=self.medium)
        medium.place(x=345, y=300)
        if not self.hard_allowed:
            hard = Button(self.window, text='Hard', font=("Proxima Nova Regular", 20), command=self.hard, fg='grey')
        else:
            hard = Button(self.window, text='Hard', font=("Proxima Nova Regular", 20), command=self.hard)
        hard.place(x=470, y=300)
        day = Button(self.window, text='Day Mode', font=("Proxima Nova Regular", 12), command=self.day)
        day.place(x=700, y=10)
        night = Button(self.window, text='Night Mode', font=("Proxima Nova Regular", 12), command=self.night)
        night.place(x=696, y=40)

    # Start the application window in night mode
    def start_night(self) -> None:
        """Start the program"""
        self.clear()
        self.add_home()
        label = Label(self.window, text='Pick a difficulty level.', font=("Proxima Nova Bold", 20), fg='white')
        label.place(x=300, y=200)
        label.config(bg='#323232')
        easy = Button(self.window, text='Easy', font=("Proxima Nova Regular", 20), command=self.easy)
        easy.place(x=250, y=300)
        easy.config(bg='#323232')
        if not self.medium_allowed:
            medium = Button(self.window, text='Medium', font=("Proxima Nova Regular", 20), command=self.medium,
                            bg='grey', fg='grey')
        else:
            medium = Button(self.window, text='Medium', font=("Proxima Nova Regular", 20), command=self.medium, bg='grey')
        medium.place(x=345, y=300)
        if not self.hard_allowed:
            hard = Button(self.window, text='Hard', font=("Proxima Nova Regular", 20), command=self.hard, fg='grey')
            hard.config(bg='#323232')
        else:
            hard = Button(self.window, text='Hard', font=("Proxima Nova Regular", 20), command=self.hard)
            hard.config(bg='#323232')
        hard.place(x=470, y=300)
        day = Button(self.window, text='Day Mode', font=("Proxima Nova Regular", 12), command=self.day)
        day.place(x=700, y=10)
        day.config(bg='#323232')
        night = Button(self.window, text='Night Mode', font=("Proxima Nova Regular", 12), command=self.night)
        night.place(x=696, y=40)
        night.config(bg='#323232')

    # Set the window in night mode
    def night(self) -> None:
        self.window['background'] = '#323232'
        self.day_night = 'night'
        self.clear()
        self.start_night()

    # Set the window in day mode
    def day(self) -> None:
        self.window['background'] = '#EBEBEB'
        self.day_night = 'day'
        self.clear()
        self.start_day()

    # Set the difficulty to easy and begin a test
    def easy(self) -> None:
        """Easy difficulty"""
        self.current_level = 'Easy'
        self.begin_test()

    # Begin a typing test
    def test(self) -> None:
        """Begin a test based on self.current_level"""
        self.clear()
        self.add_home()
        picked_test = self.pick_test()
        self.current_test = picked_test
        self.display_test(picked_test)
        # type_window = Entry(self.window, textvariable=self.input, highlightthickness=2)
        # type_window.configure(highlightbackground="red", highlightcolor="red", width=50)
        type_window = Entry(self.window, textvariable=self.input, width=50)
        type_window.place(x=170, y=470)
        submit = Button(self.window, text='SUBMIT', font=("Proxima Nova Bold", 20), command=self.submit)
        submit.place(x=340, y=500)
        if self.day_night == 'night':
            submit.config(bg='#323232', fg='#EBEBEB')

    # Display the test on the window
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
            test = Label(self.window, text=to_place, font=("Proxima Nova Regular", 16))
            test.place(x=10, y=50 + (multiplier * 25))
            if self.day_night == 'night':
                test.config(bg='#323232', fg='#EBEBEB')
            multiplier += 1

    # Submit the typed text and evaluate
    def submit(self) -> None:
        """Submit the entered text and evaluate the accuracy"""
        self.clear()
        self.add_home()
        answer = self.input.get()
        total = len(self.current_test)
        correct = 0
        mistakes = {'skipped': 0, 'extra': 0, 'punctuation': 0, 'incorrect': 0}

        if len(answer) >= len(self.current_test):
            length = len(self.current_test)
        else:
            length = len(answer)

        i = 0
        while i != length:
            if self.current_test[i] == answer[i]:
                correct += 1
                i += 1
            elif i < length - 1 and self.current_test[i] == answer[i + 1]:
                if answer[i] in ' ,.!;\"\'()':
                    mistakes['punctuation'] += 1
                else:
                    mistakes['extra'] += 1
                answer = answer[:i] + answer[i + 1:]
                if length == len(answer) + 1:
                    length -= 1
                if i > length:
                    i = length
                else:
                    i += 1
            elif i < length - 1 and self.current_test[i + 1] == answer[i]:
                if self.current_test[i] in ' ,.!;\"\'()':
                    mistakes['punctuation'] += 1
                else:
                    mistakes['extra'] += 1
                mistakes['skipped'] += 1
                answer = answer[:i] + self.current_test[i] + answer[i + 1:]
                if length == len(answer) - 1:
                    length += 1
                i += 1
            else:
                mistakes['incorrect'] += 1
                i += 1

        self.input = StringVar()
        accuracy = correct / total * 100
        label1 = Label(self.window, text='Accuracy: ' + str(round(accuracy, 1)) + '%',
                       font=("Proxima Nova Bold", 24), fg='red')
        label1.place(x=300, y=100)
        if self.day_night == 'night':
            label1.config(bg='#323232', fg='pink')

        if round(accuracy) > 90:
            self.streak += 1
            if self.streak < 3:
                label3 = Label(self.window, text='Current streak: ' + str(self.streak) + '!',
                               font=("Proxima Nova Bold", 24), fg='red')
                label3.place(x=290, y=200)
                button = Button(self.window, text='Next Test', font=("Proxima Nova Bold", 20), command=self.begin_test)
                button.place(x=335, y=300)
                label2 = Label(self.window, text='Get a streak of 3 to proceed to the next level.',
                               font=("Proxima Nova Bold", 16))
                label2.place(x=220, y=500)

                mistake = Label(self.window, text='Mistakes', font=("Proxima Nova Bold", 20), fg='red')
                mistake.place(x=345, y=500)
                skipped = Label(self.window, text='Skipped Character: ' + str(mistakes['skipped']),
                                font=("Proxima Nova Regular", 14))
                skipped.place(x=320, y=570)
                extra = Label(self.window, text='Extra Character: ' + str(mistakes['extra']),
                              font=("Proxima Nova Regular", 14))
                extra.place(x=335, y=550)
                punctuation = Label(self.window, text='Punctuation: ' + str(mistakes['punctuation']),
                                    font=("Proxima Nova Regular", 14))
                punctuation.place(x=345, y=590)
                incorrect = Label(self.window, text='Incorrect Character: ' + str(mistakes['incorrect']),
                                  font=("Proxima Nova Regular", 14))
                incorrect.place(x=320, y=530)
                if self.day_night == 'night':
                    label3.config(bg='#323232', fg='#EBEBEB')
                    button.config(bg='#323232', fg='#EBEBEB')
                    label2.config(bg='#323232', fg='#EBEBEB')
                    mistake.config(bg='#323232', fg='#EBEBEB')
                    skipped.config(bg='#323232', fg='#EBEBEB')
                    extra.config(bg='#323232', fg='#EBEBEB')
                    punctuation.config(bg='#323232', fg='#EBEBEB')
                    incorrect.config(bg='#323232', fg='#EBEBEB')
            else:
                label3 = Label(self.window, text='Easy: Completed!', font=("Proxima Nova Bold", 24), fg='red')
                label3.place(x=310, y=200)
                button = Button(self.window, text='Go Home', font=("Proxima Nova Bold", 20), command=self.go_home)
                button.place(x=350, y=300)
                if self.day_night == 'night':
                    label3.config(bg='#323232', fg='#EBEBEB')
                    button.config(bg='#323232', fg='#EBEBEB')
                if not self.medium_allowed:
                    self.medium_allowed = True
                elif not self.hard_allowed:
                    self.hard_allowed = True

        else:
            self.streak = 0
            label4 = Label(self.window, text='Current streak: ' + str(self.streak) + '!',
                           font=("Proxima Nova Bold", 24), fg='red')
            label4.place(x=290, y=200)
            button = Button(self.window, text='Try Again', font=("Proxima Nova Bold", 20), command=self.begin_test)
            button.place(x=320, y=300)
            label2 = Label(self.window, text='Get a streak of 3 to proceed to the next level.',
                           font=("Proxima Nova Bold", 16))
            label2.place(x=220, y=400)

            mistake = Label(self.window, text='Mistakes', font=("Proxima Nova Bold", 20), fg='red')
            mistake.place(x=345, y=500)
            skipped = Label(self.window, text='Skipped Character: ' + str(mistakes['skipped']),
                            font=("Proxima Nova Regular", 14))
            skipped.place(x=320, y=570)
            extra = Label(self.window, text='Extra Character: ' + str(mistakes['extra']),
                          font=("Proxima Nova Regular", 14))
            extra.place(x=335, y=550)
            punctuation = Label(self.window, text='Punctuation: ' + str(mistakes['punctuation']),
                                font=("Proxima Nova Regular", 14))
            punctuation.place(x=345, y=590)
            incorrect = Label(self.window, text='Incorrect Character: ' + str(mistakes['incorrect']),
                              font=("Proxima Nova Regular", 14))
            incorrect.place(x=320, y=530)
            if self.day_night == 'night':
                label4.config(bg='#323232', fg='#EBEBEB')
                button.config(bg='#323232', fg='#EBEBEB')
                label2.config(bg='#323232', fg='#EBEBEB')
                mistake.config(bg='#323232', fg='pink')
                skipped.config(bg='#323232', fg='#EBEBEB')
                extra.config(bg='#323232', fg='#EBEBEB')
                punctuation.config(bg='#323232', fg='#EBEBEB')
                incorrect.config(bg='#323232', fg='#EBEBEB')

    # Pick a random test of the set difficulty
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

    # Start a test
    def begin_test(self) -> None:
        """Begin test page"""
        self.clear()
        self.add_home()
        label = Label(self.window, text='Press begin when you are ready. Press submit once you\'re done.',
                      font=("Proxima Nova Regular", 20))
        label.place(x=120, y=100)
        label2 = Label(self.window, text='The test will begin immediately.', font=("Proxima Nova Bold", 20))
        label2.place(x=247, y=140)
        begin = Button(self.window, text='BEGIN', font=("Proxima Nova Bold", 20), command=self.test)
        begin.place(x=350, y=200)
        if self.day_night == 'night':
            label.config(bg='#323232', fg='#EBEBEB')
            label2.config(bg='#323232', fg='#EBEBEB')
            begin.config(bg='#323232', fg='#EBEBEB')

    # Set the difficulty to medium and begin a test
    def medium(self) -> None:
        """Medium difficulty"""
        if self.medium_allowed:
            self.current_level = 'Medium'
            self.begin_test()
        else:
            temp = Tk()
            temp.title('Not so fast!')
            temp.geometry("400x100+500+300")
            label = Label(temp, text='This difficulty is locked!', font=("Proxima Nova Bold", 18))
            label.place(x=100, y=10)
            label2 = Label(temp, text='Complete lower difficulties to continue.', font=("Proxima Nova Regular", 14))
            label2.place(x=70, y=50)
            if self.day_night == 'night':
                temp.config(bg='#323232')
                label.config(bg='#323232', fg='#EBEBEB')
                label2.config(bg='#323232', fg='#EBEBEB')

    # Set the difficulty to hard and begin a test
    def hard(self) -> None:
        """Hard difficulty"""
        if self.hard_allowed:
            self.current_level = 'Hard'
            self.begin_test()
        else:
            temp = Tk()
            temp.title('Not so fast!')
            temp.geometry("400x100+500+300")
            label = Label(temp, text='This difficulty is locked!', font=("Proxima Nova Bold", 18))
            label.place(x=100, y=10)
            label2 = Label(temp, text='Complete lower difficulties to continue.', font=("Proxima Nova Regular", 14))
            label2.place(x=70, y=50)
            if self.day_night == 'night':
                temp.config(bg='#323232')
                label.config(bg='#323232', fg='#EBEBEB')
                label2.config(bg='#323232', fg='#EBEBEB')

    # Clear the application window
    def clear(self) -> None:
        """Clear all widgets"""
        for widgets in self.window.winfo_children():
            widgets.destroy()

    # Add the home button
    def add_home(self) -> None:
        """Add a home button in the top left"""
        if self.day_night == 'day':
            button = Button(self.window, text='Home', font=("Proxima Nova Bold", 14), command=self.confirm,
                            fg='blue', bg='red')
        else:
            button = Button(self.window, text='Home', font=("Proxima Nova Bold", 14), command=self.confirm,
                            fg='#EBEBEB', bg='#323232')
        button.place(x=10, y=10)

    # Confirm that the user wants to go home
    def confirm(self) -> None:
        """Confirm whether the user wants to go home"""
        self.confirm_window = Tk()
        if self.day_night == 'night':
            self.confirm_window['background'] = '#323232'
        self.confirm_window.title('Go home?')
        self.confirm_window.geometry("400x100+500+300")
        label = Label(self.confirm_window, text='Are you sure you want to return home?')
        label.place(x=77, y=0)
        label2 = Label(self.confirm_window, text='Progress at this difficulty level will be lost.',
                       fg='red', font=("Proxima Nova Bold", 14))
        label2.place(x=57, y=25)
        yes_button = Button(self.confirm_window, text='Yes', font=("Proxima Nova Bold", 14), command=self.go_home)
        yes_button.place(x=135, y=50)
        no_button = Button(self.confirm_window, text='No', font=("Proxima Nova Bold", 14), command=self.cancel_go_home)
        no_button.place(x=205, y=50)
        if self.day_night == 'night':
            label.config(bg='#323232', fg='#EBEBEB')
            label2.config(bg='#323232', fg='#EBEBEB')
            yes_button.config(bg='#323232')
            no_button.config(bg='#323232')
        self.confirm_window.mainloop()

    # Close the confirmation window to go home
    def cancel_go_home(self) -> None:
        """Close the go home confirmation window."""
        self.confirm_window.destroy()
        self.confirm_window = None

    # Go to the home page
    def go_home(self) -> None:
        """Return to the home GUI"""
        if self.confirm_window is not None:
            self.confirm_window.destroy()
        self.input = StringVar()
        self.current_test = ''
        self.streak = 0
        self.clear()
        if self.day_night == 'day':
            self.start_day()
        else:
            self.start_night()


# Read the tests and load them into a dictionary
def read_data(file_name: str) -> dict:
    """Read the tests in <file_name> and return a dictionary mapping of the difficulty of
    the test to the test and its length"""
    with open(file_name) as file:
        reader = csv.reader(file)
        mapping = {}
        for row in reader:
            mapping[row[1]] = row[0]
    return mapping


# Open an application window upon running this file
if __name__ == '__main__':
    app = App()
