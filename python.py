import tkinter as tk
import customtkinter as ctk
from tkinter import PhotoImage, messagebox
from random import shuffle

# Class to create tooltips for widgets, must be put before the main quiz class.
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()

# Main application class for the quiz
class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quizpedia")
        self.geometry("1024x768")
        self.bg_image = PhotoImage(file="C:/Users/educa/OneDrive/Pictures/bg3.png")
        self.name_bg_image = PhotoImage(file="C:/Users/educa/OneDrive/Pictures/usernamebg.png")

        # Function to set background image for a frame
        def set_background(frame):
            bg_label = tk.Label(frame, image=self.bg_image)
            bg_label.pack(fill='both', expand=True)
            bg_label.image = self.bg_image

        # Function to set background image for the name entry frame
        def set_name_background(frame):
            bg_label = tk.Label(frame, image=self.name_bg_image)
            bg_label.pack(fill='both', expand=True)
            bg_label.image = self.name_bg_image

        # Home frame setup
        self.home_frame = tk.Frame(self)
        set_background(self.home_frame)

        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.image = self.bg_image
        self.home_frame.pack(fill='both', expand=True)

        # Name entry frame (shown by default)
        self.name_frame = ctk.CTkFrame(self)
        self.name_frame.pack(fill='both', expand=True)
        set_name_background(self.name_frame)

        # Quiz frame (hidden by default)
        self.quiz_frame = ctk.CTkFrame(self)
        self.quiz_frame.pack_forget()

        # Leaderboard frame (hidden by default)
        self.leaderboard_frame = ctk.CTkFrame(self)
        self.leaderboard_frame.pack_forget()

        # Home screen button to start the quiz
        self.quiz_button = ctk.CTkButton(self.home_frame, text='Start Quiz', command=self.start_quiz)
        self.quiz_button.pack(pady=20)

        button_font = ctk.CTkFont(family="Helvetica", size=30)

        # Buttons for navigating to quiz and factoids
        self.button1 = ctk.CTkButton(self, text="Quiz", width=200, height=100, fg_color="#76ABAE", font=button_font,
                                     border_width=2, corner_radius=2, command=self.start_quiz)
        self.button1.place(relx=0.3, rely=0.6, anchor=tk.CENTER)

        self.button2 = ctk.CTkButton(self, text="Factoids", width=200, height=100, fg_color="#76ABAE", font=button_font,
                                     border_width=2, corner_radius=2)
        self.button2.place(relx=0.7, rely=0.6, anchor=tk.CENTER)

        self.user_name = ''
        self.user_score = 0

        # List of quiz questions and answers
        self.questions = [
            ("What is the capital of France?", ["Paris", "London", "Berlin", "Rome"]),
            ("Which planet is known as the Red Planet?", ["Mars", "Jupiter", "Saturn", "Venus"]),
            ("What is the largest mammal in the world?", ["Blue whale", "Elephant", "Giraffe", "Hippopotamus"]),
            ("What is the meal eaten during morning called", ["Breakfast", "Lunch", "Dinner", "Brunch"]),
            ("What is the capital of Japan?", ["Tokyo", "Kyoto", "Osaka", "Hiroshima"]),
            ("What is the tallest mountain in the world?", ["Mount Everest", "K2", "Kangchenjunga", "Lhotse"]),
            ("What is the largest ocean in the world?", ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"]),
            ("What is the smallest planet in our solar system?", ["Mercury", "Venus", "Mars", "Earth"]),
            ("What is the largest country in the world by area?", ["Russia", "Canada", "China", "United States"]),
            ("What is the longest river in the world?", ["Nile", "Amazon", "Yangtze", "Mississippi"]),
        ]
        self.current_question = 0
        self.correct_answer = ''

        self.initialize_quiz_ui()

    # Initialize the UI components for the quiz
    def initialize_quiz_ui(self):
        buttonfont2 = ctk.CTkFont(family="Helvetica", size=20)
        # Create widgets for the name entry frame
        self.name_label = ctk.CTkLabel(self.name_frame, text="Enter your name:")
        self.name_entry = ctk.CTkEntry(self.name_frame)
        self.enter_button = ctk.CTkButton(self.name_frame, text='Enter', command=self.validate_name, font=buttonfont2)
        self.name_label.pack(pady=10)
        self.name_entry.pack(pady=10)
        self.enter_button.pack(pady=10)

        # Tooltip for name entry
        ToolTip(self.name_entry, "Enter your full name without any numbers or special characters.")

        # Create widgets for the quiz frame using grid
        self.question_label = ctk.CTkLabel(self.quiz_frame, text="")
        self.question_label.grid(row=0, column=0, columnspan=2, pady=20)  # Span across all columns

        self.options_var = tk.IntVar()
        self.options_buttons = [ctk.CTkRadioButton(self.quiz_frame, text="Option", variable=self.options_var, value=i) for i in range(4)]
        # Positioning will be handled in display_question
        self.submit_button = ctk.CTkButton(self.quiz_frame, text='Submit Answer', command=self.check_answer)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=20)  # Span across all columns

        # Status label for current question and score
        self.status_label = ctk.CTkLabel(self.quiz_frame, text="")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Back button to return to the previous screen
        self.back_button = ctk.CTkButton(self.quiz_frame, text="Back", command=self.return_to_home)
        self.back_button.grid(row=5, column=0, pady=10)

        # Create widgets for the leaderboard frame
        self.score_label = ctk.CTkLabel(self.leaderboard_frame, text="")
        self.home_button = ctk.CTkButton(self.leaderboard_frame, text='Return to Home', command=self.return_to_home)
        self.score_label.pack(pady=20)
        self.home_button.pack(pady=20)

    def start_quiz(self):
        self.home_frame.pack_forget()
        self.button1.place_forget()
        self.button2.place_forget()
        self.name_entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.enter_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def validate_name(self):
        while True:
            user_name = self.name_entry.get()
            if not user_name.isalpha():
                messagebox.showerror("Invalid Name", "Please enter a valid name (letters only).")
                return
            elif len(user_name) > 20:
                messagebox.showerror("Invalid Name", "Please enter a name with no more than 20 characters.")
                return
            else:
                self.user_name = user_name
                self.name_frame.pack_forget()
                self.quiz_frame.pack(fill='both', expand=True)
                self.display_question()
                break

    def process_next(self):
        if self.questions:
            self.questions.pop(0)
        if self.questions:
            self.display_question()
        else:
            self.show_leaderboard()
            self.submit_button.configure(state='normal')

    def display_question(self):
        if not self.questions:
            self.show_leaderboard()
            return

        self.current_question, options = self.questions[0]
        correct_answer_text = options[0]
        shuffle(options)
        self.correct_answer = options.index(correct_answer_text)
        self.question_label.configure(text=self.current_question)
        self.question_label.grid(row=0, column=0, columnspan=4, pady=20)

        grid_positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        for i, option in enumerate(options):
            self.options_buttons[i].configure(text=option)
            self.options_buttons[i].grid(row=grid_positions[i][0], column=grid_positions[i][1], pady=10, padx=20, sticky="nsew")

        self.options_var.set(-1)
        self.quiz_frame.columnconfigure(0, weight=1)
        self.quiz_frame.columnconfigure(1, weight=1)
        self.quiz_frame.columnconfigure(2, weight=1)
        self.quiz_frame.columnconfigure(3, weight=1)
        self.submit_button.configure(state='normal')
        self.submit_button.grid(row=3, column=1, columnspan=2, pady=20)
        self.status_label.configure(text=f"Question {len(self.questions) - len(self.questions) + 1} of {len(self.questions)} | Score: {str(self.user_score)}")

    def check_answer(self):
        selected_option = self.options_var.get()
        if selected_option == -1:
            messagebox.showerror("No Selection", "Please select an option before submitting.")
            return
        self.submit_button.configure(state='disabled')
        if selected_option == self.correct_answer:
            self.user_score += 1
        self.after(200, self.process_next)

    def show_leaderboard(self):
        self.quiz_frame.pack_forget()
        self.leaderboard_frame.pack(fill='both', expand=True)
        self.score_label.configure(text=f"{self.user_name}, your score is: {self.user_score}")

    def return_to_home(self):
        self.user_name = ''
        self.user_score = 0
        self.questions = [
            ("What is the capital of France?", ["Paris", "London", "Berlin", "Rome"]),
            ("Which planet is known as the Red Planet?", ["Mars", "Jupiter", "Saturn", "Venus"]),
            ("What is the largest mammal in the world?", ["Blue whale", "Elephant", "Giraffe", "Hippopotamus"]),
            ("What is the meal eaten during morning called", ["Breakfast", "Lunch", "Dinner", "Brunch"]),
            ("What is the capital of Japan?", ["Tokyo", "Kyoto", "Osaka", "Hiroshima"]),
            ("What is the tallest mountain in the world?", ["Mount Everest", "K2", "Kangchenjunga", "Lhotse"]),
            ("What is the largest ocean in the world?", ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"]),
            ("What is the smallest planet in our solar system?", ["Mercury", "Venus", "Mars", "Earth"]),
            ("What is the largest country in the world by area?", ["Russia", "Canada", "China", "United States"]),
            ("What is the longest river in the world?", ["Nile", "Amazon", "Yangtze", "Mississippi"]),
        ]
        self.current_question = 0
        self.correct_answer = ''
        self.leaderboard_frame.pack_forget()
        self.home_frame.pack(fill='both', expand=True)
        self.button1.place(relx=0.3, rely=0.6, anchor=tk.CENTER)
        self.button2.place(relx=0.7, rely=0.6, anchor=tk.CENTER)
        self.name_frame.pack(fill='both', expand=True)
        self.name_entry.delete(0, 'end')

if __name__ == "__main__":
    app = QuizApp()
    tk.mainloop()