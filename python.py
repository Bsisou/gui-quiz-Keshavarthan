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

    button_frame = Frame(window, bg="#222831")
    button_frame.pack(pady=20)

    button1 = ctk.CTkButton(button_frame, text="Button 1")
    button1.pack(side="left", padx=10, pady=10)

    button2 = ctk.CTkButton(button_frame, text="Button 2")
    button2.pack(side="right", padx=10, pady=10)

    button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    window.mainloop()


def quiz_page():
    window = Tk()
    window.geometry("1024x768")


if __name__ == "__main__":
    main()
