import customtkinter as ctk
import tkinter as tk
from random import shuffle, randint
from tkinter import PhotoImage
from time import sleep




class QuizApp(tk.Tk):
    def __init__(window):
        
        window = tk.Tk()
        window.geometry("1024x768")
        window.title("Quizmania")

        window.bg_image = PhotoImage(file='C:/Users/educa/OneDrive/Pictures/bg3.png')

        def set_background(frame):
            bg_label = ctk.CTkLabel(frame, image=window.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.image = window.bg_image

        window.home_frame = tk.Frame(window)
        window.home_frame.pack(fill='both', expand=True)
        set_background(window.home_frame)

        # Background label using the image
        window.bg_label = tk.Label(window, image=window.bg_image)
        window.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to the image
        window.bg_label.image = window.bg_image

        # Fun facts frame (hidden by default)
        window.funfacts_frame = ctk.CTkFrame(window)
        window.funfacts_frame.pack_forget()

        # Quiz frame (hidden by default)
        window.quiz_frame = ctk.CTkFrame(window)
        window.quiz_frame.pack_forget()

        # Leaderboard frame (hidden by default)
        window.leaderboard_frame = ctk.CTkFrame(window)
        window.leaderboard_frame.pack_forget()

        button_font = ctk.CTkFont(family="Helvetica", size=30)
        button1 = ctk.CTkButton(window, text="Quiz", width=200, height=100, fg_color="#76ABAE", font=button_font, border_width=2, corner_radius=2)
        button1.place(relx=0.3, rely=0.6, anchor=tk.CENTER)

        button2 = ctk.CTkButton(window, text="Factoids", width=200, height=100,  fg_color="#76ABAE", font=button_font, border_width=2, corner_radius=2)
        button2.place(relx=0.7, rely=0.6, anchor=tk.CENTER)


        window.mainloop()



if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
