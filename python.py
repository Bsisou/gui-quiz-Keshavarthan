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


        button_font = ctk.CTkFont(family="Helvetica", size=30)
        button1 = ctk.CTkButton(self, text="Quiz", width=200, height=100, fg_color="#76ABAE", font=button_font,
                                border_width=2, corner_radius=2, command=self.start_quiz)
        button1.place(relx=0.3, rely=0.6, anchor=tk.CENTER)

        button2 = ctk.CTkButton(self, text="Factoids", width=200, height=100, fg_color="#76ABAE", font=button_font,
                                border_width=2, corner_radius=2)
        button2.place(relx=0.7, rely=0.6, anchor=tk.CENTER)

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



if __name__ == "__main__":
    app = QuizApp()
    tk.mainloop()