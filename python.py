import tkinter as tk
import customtkinter as ctk
from tkinter import PhotoImage,messagebox
from time import sleep


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quizpedia")
        self.geometry("1024x768")
        self.bg_image = PhotoImage(file="C:/Users/educa/OneDrive/Pictures/bg3.png")

        def set_background(frame):
            bg_label = tk.Label(frame, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.image = self.bg_image

        self.home_frame = tk.Frame(self)
        self.home_frame.pack(fill='both', expand=True)
        set_background(self.home_frame)

        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to the image
        self.bg_label.image = self.bg_image

        # Quiz frame (hidden by default)
        self.quiz_frame = ctk.CTkFrame(self)
        self.quiz_frame.pack_forget()

        # Leaderboard frame (hidden by default)
        self.leaderboard_frame = ctk.CTkFrame(self)
        self.leaderboard_frame.pack_forget()

        # Home screen button
        self.quiz_button = ctk.CTkButton(self.home_frame, text='Start Quiz', command=self.start_quiz)
        self.quiz_button.pack(pady=20)

        button_font = ctk.CTkFont(family="Helvetica", size=30)

        self.button1 = ctk.CTkButton(self, text="Quiz", width=200, height=100, fg_color="#76ABAE", font=button_font,
                                border_width=2, corner_radius=2, command=self.start_quiz)
        self.button1.place(relx=0.3, rely=0.6, anchor=tk.CENTER)

        self.button2 = ctk.CTkButton(self, text="Factoids", width=200, height=100, fg_color="#76ABAE", font=button_font,
                                border_width=2, corner_radius=2)
        self.button2.place(relx=0.7, rely=0.6, anchor=tk.CENTER)

        self.user_name = ''

        self.initialize_quiz_ui()
    def initialize_quiz_ui(self):
        # Create widgets for the quiz frame
        self.name_label = ctk.CTkLabel(self.quiz_frame, text="Enter your name:")
        self.name_entry = ctk.CTkEntry(self.quiz_frame)
        self.enter_button = ctk.CTkButton(self.quiz_frame, text='Enter', command=self.validate_name)

        self.question_label = ctk.CTkLabel(self.quiz_frame, text="")
        self.options_var = tk.StringVar()
        self.options_buttons = [tk.Radiobutton(self.quiz_frame, text="Option", variable=self.options_var) for _ in
                                range(4)]
        self.submit_button = ctk.CTkButton(self.quiz_frame, text='Submit Answer', command=self.check_answer)

        # Create widgets for the leaderboard frame
        self.score_label = ctk.CTkLabel(self.leaderboard_frame, text="")
        self.home_button = ctk.CTkButton(self.leaderboard_frame, text='Return to Home', command=self.return_to_home)



    def start_quiz(self):
        self.home_frame.pack_forget()
        self.button1.destroy()
        self.button2.destroy()
        self.quiz_frame.pack(fill='both', expand=True)
        self.name_label.pack(pady=20)
        self.name_entry.pack(pady=10)
        self.enter_button.pack(pady=20)

    def validate_name(self):
        user_name = self.name_entry.get()
        if user_name.isalpha():
            self.user_name = user_name
            self.name_label.pack_forget()
            self.name_entry.pack_forget()
            self.enter_button.pack_forget()
            self.display_question()
        else:
            messagebox.showerror("Invalid Name", "Please enter a valid name (letters only).")

    def check_answer(self):
        selected_option = self.options_var.get()
        if selected_option == self.correct_answer:
            self.user_score += 1
        self.questions.pop(0)
        if self.questions:
            self.display_question()
        else:
            self.show_leaderboard()

    def show_leaderboard(self):
        self.quiz_frame.pack_forget()
        self.leaderboard_frame.pack(fill='both', expand=True)
        self.score_label.configure(text=f"{self.user_name}, your score is: {self.user_score}")
        self.score_label.pack(pady=20)
        self.home_button.pack(pady=20)

    def return_to_home(self):
        self.leaderboard_frame.pack_forget()
        self.home_frame.pack(fill='both', expand=True)


if __name__ == "__main__":
    app = QuizApp()
    tk.mainloop()