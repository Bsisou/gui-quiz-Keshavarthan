import tkinter as tk
import customtkinter as ctk
from tkinter import PhotoImage, messagebox
from random import shuffle, choice


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
        label = ctk.CTkLabel(tw, text=self.text, justify='left',
                             fg_color="#ffffe0", corner_radius=5,
                             font=ctk.CTkFont(family="Helvetica", size=10),
                             text_color="black")  # Changed font color to black
        label.pack(ipadx=1, ipady=1)

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

        # Difficulty selection frame (hidden by default)
        self.difficulty_frame = ctk.CTkFrame(self)
        self.difficulty_frame.pack_forget()

        # Quiz frame (hidden by default)
        self.quiz_frame = ctk.CTkFrame(self)
        self.quiz_frame.pack_forget()

        # Leaderboard frame (hidden by default)
        self.leaderboard_frame = ctk.CTkFrame(self)
        self.leaderboard_frame.pack_forget()

        # Fun fact frame (hidden by default)
        self.funfact_frame = ctk.CTkFrame(self)
        self.funfact_frame.pack_forget()

        # Fun fact label
        self.funfact_label = ctk.CTkLabel(self.funfact_frame, text="", wraplength=380, width=400, height=400,
                                          corner_radius=5)
        self.funfact_label.pack(padx=10, pady=10)

        # Home screen button to start the quiz
        self.quiz_button = ctk.CTkButton(self.home_frame, text='Start Quiz', command=self.start_quiz)
        self.quiz_button.pack(pady=20)

        button_font = ctk.CTkFont(family="Helvetica", size=30)

        # Buttons for navigating to quiz and factoids
        self.button1 = ctk.CTkButton(self, text="Quiz", width=200, height=100, fg_color="#76ABAE", font=button_font,
                                     border_width=2, corner_radius=2, command=self.start_quiz)
        self.button1.place(relx=0.3, rely=0.6, anchor=tk.CENTER)

        self.button2 = ctk.CTkButton(self, text="Factoids", width=200, height=100, fg_color="#76ABAE", font=button_font,
                                     border_width=2, corner_radius=2, command=self.show_funfact)
        self.button2.place(relx=0.7, rely=0.6, anchor=tk.CENTER)

        self.timer_id = None
        self.user_name = ''
        self.user_score = 0
        self.difficulty = 'easy'

        # List of quiz questions and answers
        self.original_questions = [
            ("What is the smallest unit of life?", ["Cell", "Atom", "Molecule", "Organ"]),
            ("Which insect is known for its role in pollination?", ["Bee", "Ant", "Butterfly", "Beetle"]),
            ("What is the smallest bird in the world?", ["Bee Hummingbird", "Sparrow", "Finch", "Wren"]),
            ("Which fruit is known for its small size and high vitamin C content?",
             ["Strawberry", "Apple", "Banana", "Grape"]),
            ("What is the smallest planet in our solar system?", ["Mercury", "Venus", "Mars", "Earth"]),
            ("Which small mammal is known for its ability to glide?", ["Sugar Glider", "Squirrel", "Mouse", "Bat"]),
            ("What is the smallest bone in the human body?", ["Stapes", "Malleus", "Incus", "Humerus"]),
            ("Which small flower is often associated with love and romance?", ["Rose", "Daisy", "Tulip", "Lily"]),
            ("What is the smallest country in the world by area?", ["Vatican City", "Monaco", "Nauru", "San Marino"]),
            ("Which small marine creature is known for its ability to change color?",
             ["Octopus", "Jellyfish", "Seahorse", "Starfish"]),
            ("What is the smallest unit of a chemical element?", ["Atom", "Molecule", "Compound", "Mixture"]),
            ("Which small bird is known for its beautiful singing?", ["Nightingale", "Crow", "Eagle", "Owl"]),
            ("What is the smallest type of tree?", ["Bonsai", "Oak", "Pine", "Maple"]),
            ("Which small animal is known for its ability to play dead?", ["Opossum", "Rabbit", "Fox", "Deer"]),
            ("What is the smallest continent by land area?", ["Australia", "Europe", "Antarctica", "South America"]),
            ("Which small fruit is known for its high antioxidant content?",
             ["Blueberry", "Apple", "Orange", "Pineapple"]),
            ("What is the smallest unit of time?", ["Second", "Minute", "Hour", "Day"]),
            ("Which small insect is known for its ability to produce silk?", ["Silkworm", "Bee", "Ant", "Butterfly"]),
            ("What is the smallest type of penguin?",
             ["Little Blue Penguin", "Emperor Penguin", "King Penguin", "Adelie Penguin"]),
            ("Which small amphibian is known for its bright colors?",
             ["Poison Dart Frog", "Toad", "Salamander", "Newt"]),
        ]

        # List of harder quiz questions and answers
        self.hard_questions = [
            ("What is the smallest particle of an element that retains its chemical properties?",
             ["Atom", "Proton", "Neutron", "Electron"]),
            ("Which small bird is known for its long migratory journey?",
             ["Arctic Tern", "Sparrow", "Robin", "Swallow"]),
            ("What is the smallest unit of a living organism?", ["Cell", "Tissue", "Organ", "System"]),
            ("Which small mammal is known for its ability to hibernate?", ["Hedgehog", "Rabbit", "Fox", "Deer"]),
            ("What is the smallest unit of digital information?", ["Bit", "Byte", "Kilobyte", "Megabyte"]),
            ("Which small fish is known for its vibrant colors and is popular in aquariums?",
             ["Neon Tetra", "Goldfish", "Betta", "Guppy"]),
            ("What is the smallest unit of a compound?", ["Molecule", "Atom", "Element", "Mixture"]),
            ("Which small bird is known for its ability to hover in mid-air?",
             ["Hummingbird", "Eagle", "Sparrow", "Owl"]),
            ("What is the smallest unit of currency in the United States?", ["Cent", "Dollar", "Nickel", "Dime"]),
            (
            "Which small mammal is known for its ability to dig extensive burrows?", ["Mole", "Rabbit", "Fox", "Deer"]),
        ]

        self.reset_questions()

        # List of fun facts
        self.funfacts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.",
            "A day on Venus is longer than a year on Venus. It takes Venus longer to rotate once on its axis (243 Earth days) than it does to complete one orbit of the Sun (225 Earth days).",
            "Bananas are berries, but strawberries aren't. Botanically, a berry is a fruit produced from the ovary of a single flower with seeds embedded in the flesh.",
            "Octopuses have three hearts. Two pump blood to the gills, while the third pumps it to the rest of the body.",
            "There are more stars in the universe than grains of sand on all the Earth's beaches. The observable universe has an estimated 1,000,000,000,000,000,000,000,000 stars."
        ]

        self.initialize_quiz_ui()

    # Initialize the UI components for the quiz
    def initialize_quiz_ui(self):
        buttonfont2 = ctk.CTkFont(family="Helvetica", size=20)
        question_font = ctk.CTkFont(family="Helvetica", size=24)  # Increased font size for questions
        large_button_font = ctk.CTkFont(family="Helvetica", size=18)  # Font for larger buttons
        # Create widgets for the name entry frame
        self.name_label = ctk.CTkLabel(self.name_frame, text="Enter your name:")
        self.name_entry = ctk.CTkEntry(self.name_frame)
        self.enter_button = ctk.CTkButton(self.name_frame, text='Enter', command=self.validate_name, font=buttonfont2)
        self.name_label.pack(pady=10)
        self.name_entry.pack(pady=10)
        self.enter_button.pack(pady=10)

        # Tooltip for name entry
        ToolTip(self.name_entry, "Enter your full name without any numbers or special characters.")

        # Create widgets for the difficulty selection frame
        self.easy_button = ctk.CTkButton(self.difficulty_frame, text='Easy',
                                         command=lambda: self.set_difficulty('easy'))
        self.hard_button = ctk.CTkButton(self.difficulty_frame, text='Hard',
                                         command=lambda: self.set_difficulty('hard'))
        self.easy_button.pack(pady=20)
        self.hard_button.pack(pady=20)

        # Create widgets for the quiz frame using grid
        self.question_label = ctk.CTkLabel(self.quiz_frame, text="", font=question_font)  # Set font for question label
        self.question_label.grid(row=0, column=0, columnspan=2, pady=20)  # Span across all columns

        self.options_var = tk.IntVar()
        self.options_buttons = [ctk.CTkRadioButton(self.quiz_frame, text="Option", variable=self.options_var, value=i)
                                for i in range(4)]
        self.submit_button = ctk.CTkButton(self.quiz_frame, text='Submit Answer', command=self.check_answer,
                                           font=large_button_font)
        self.submit_button.grid(row=20, column=0, columnspan=4, pady=90)  # Span across all columns

        # Status label for current question and score
        self.status_label = ctk.CTkLabel(self.quiz_frame, text="", text_color="white")  # Set text color to white
        self.status_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.timer_label = ctk.CTkLabel(self.quiz_frame, text="", text_color="white")  # Set text color to white
        self.timer_label.grid(row=0, column=2, columnspan=2, pady=10)

        # Back button to return to the previous screen
        self.back_button = ctk.CTkButton(self.quiz_frame, text="Back", command=self.return_to_home,
                                         font=large_button_font)
        self.back_button.grid(row=29, column=1, columnspan=1, pady=20, sticky="sw")

        # Create widgets for the leaderboard frame
        leaderboard_font = ctk.CTkFont(family="Helvetica", size=24, weight="bold")
        self.results_label = ctk.CTkLabel(self.leaderboard_frame, text="RESULTS", font=leaderboard_font,
                                          fg_color="#0073e6", text_color="white")
        self.results_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)  # Centered at the top

        # Username and Score labels
        self.username_label = ctk.CTkLabel(self.leaderboard_frame, text="USERNAME", font=leaderboard_font,
                                           fg_color="#009688", text_color="white")
        self.username_label.place(relx=0.4, rely=0.5, anchor=tk.CENTER)  # Adjusted position

        self.score_label = ctk.CTkLabel(self.leaderboard_frame, text="SCORE", font=leaderboard_font, fg_color="#009688",
                                        text_color="white")
        self.score_label.place(relx=0.6, rely=0.5, anchor=tk.CENTER)  # Adjusted position

        # Adjusted home button position
        self.home_button = ctk.CTkButton(self.leaderboard_frame, text='HOME', command=self.return_to_home,
                                         fg_color="#e53935", text_color="white")
        self.home_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)  # Centered and lowered position

        # Create widgets for the fun fact frame
        self.funfact_title_label = ctk.CTkLabel(self.funfact_frame, text="FUN FACTS", font=buttonfont2,
                                                fg_color="#0073e6", text_color="white")
        self.funfact_title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.funfact_label = ctk.CTkLabel(self.funfact_frame, text="", wraplength=800, fg_color="#009688",
                                          text_color="white")
        self.funfact_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.funfact_back_button = ctk.CTkButton(self.funfact_frame, text="HOME", command=self.return_to_home,
                                                 fg_color="#e53935", text_color="white")
        self.funfact_back_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def reset_questions(self):
        if self.difficulty == 'easy':
            self.questions = self.original_questions.copy()
        else:
            self.questions = self.hard_questions.copy()
        shuffle(self.questions)
        self.questions = self.questions[:10]  # Select only the first 10 questions

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
            elif len(user_name) < 3:
                messagebox.showerror("Invalid Name", "Please enter a name with at least 3 characters.")
                return
            elif len(user_name) > 15:
                messagebox.showerror("Invalid Name", "Please enter a name with no more than 15 characters.")
                return
            else:
                self.user_name = user_name
                self.name_frame.pack_forget()
                self.difficulty_frame.pack(fill='both', expand=True)
                break

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.difficulty_frame.pack_forget()
        self.quiz_frame.pack(fill='both', expand=True)
        self.reset_questions()
        self.display_question()

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
        self.question_label.grid(row=1, column=0, columnspan=4, pady=20)  # Adjust the row value

        grid_positions = [(5, 1), (5, 3), (6, 1), (6, 3)]  # Adjust the row and column values for more horizontal gap
        for i, option in enumerate(options):
            self.options_buttons[i].configure(text=option)
            self.options_buttons[i].grid(row=grid_positions[i][0], column=grid_positions[i][1], pady=10, padx=40,
                                         sticky="nsew")  # Increased horizontal padding

        self.options_var.set(-1)
        self.quiz_frame.columnconfigure(0, weight=1)
        self.quiz_frame.columnconfigure(1, weight=1)
        self.quiz_frame.columnconfigure(2, weight=1)
        self.quiz_frame.columnconfigure(3, weight=1)
        self.quiz_frame.columnconfigure(4, weight=1)  # Added extra column for spacing
        self.submit_button.configure(state='normal')

        # Update the status label position
        self.status_label.grid(row=0, column=0, pady=10, padx=20, sticky="nw")

        if self.difficulty == 'hard':
            self.start_timer()
            self.status_label.configure(
                text=f"Question {((len(self.hard_questions) - len(self.questions)) % 10) + 1} of {min(len(self.hard_questions), 10)}")
        else:
            self.status_label.configure(
                text=f"Question {((len(self.original_questions) - len(self.questions)) % 10) + 1} of {min(len(self.original_questions), 10)} | Score: {str(self.user_score)}")

    def start_timer(self):
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)  # Cancel any existing timer
        self.time_left = 10  # 10 seconds for hard mode
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.configure(text=f"Time left: {self.time_left} seconds")
            self.time_left -= 1
            self.timer_id = self.after(1000, self.update_timer)  # Save the timer ID
        else:
            self.submit_button.configure(state='disabled')  # Disable the submit button
            self.process_next()

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
        self.username_label.configure(text=f"USERNAME: {self.user_name}")
        self.score_label.configure(text=f"SCORE: {self.user_score}")

    def show_funfact(self):
        self.home_frame.pack_forget()
        self.name_frame.pack_forget()
        self.button1.place_forget()
        self.button2.place_forget()
        self.funfact_back_button.pack_forget()
        self.funfact_frame.pack(fill='both', expand=True)
        random_fact = choice(self.funfacts)
        # Update the fun fact
        self.funfact_label.configure(text=random_fact)

    def return_to_home(self):
        self.user_name = ''
        self.user_score = 0
        self.reset_questions()
        self.current_question = 0
        self.correct_answer = ''
        self.leaderboard_frame.pack_forget()
        self.quiz_frame.pack_forget()  # Ensure the quiz frame is hidden
        self.funfact_frame.pack_forget()  # Ensure the fun fact frame is hidden
        self.home_frame.pack(fill='both', expand=True)
        self.button1.place(relx=0.3, rely=0.6, anchor=tk.CENTER)
        self.button2.place(relx=0.7, rely=0.6, anchor=tk.CENTER)
        self.name_frame.pack(fill='both', expand=True)
        self.name_entry.delete(0, 'end')


if __name__ == "__main__":
    app = QuizApp()
    tk.mainloop()