from tkinter import *
import customtkinter as ctk
import random


def main():
    window = Tk()
    window.geometry("1024x768")
    window.title("Quizmania")
    window.configure(bg="#222831")

    label = Label(window, text="WELCOME TO", font=("Arial", 30), bg="#31363F", fg="#EEEEEE")
    label.pack(pady=20)

    label = Label(window, text="QUIZPEDIA", font=("Arial", 40))
    label.pack(pady=20)

    button_frame = ctk.CTkFrame(window, fg_color="transparent")
    button_frame.place(relx=0.5, rely=0.5, anchor="center")

    button_font = ctk.CTkFont(family="Helvetica", size=30)
    button1 = ctk.CTkButton(button_frame, text="Quiz", width=200, height=100, fg_color="#76ABAE", font=button_font)
    button1.grid(row=0, column=0, padx=75)

    button2 = ctk.CTkButton(button_frame, text="Factoids", width=200, height=100,  fg_color="#76ABAE", font=button_font)
    button2.grid(row=0, column=1, padx=75)

    window.mainloop()


def quiz_page():
    window = Tk()
    window.geometry("1024x768")


if __name__ == "__main__":
    main()
