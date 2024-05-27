from tkinter import *
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

    button1 = Button(button_frame, text="Factoids", font=("Comic Sans MS", 25))
    button1.pack(padx=100, side=LEFT)

    button2 = Button(button_frame, text="Quiz", font=("Comic Sans MS", 25))
    button2.pack(padx=100, side=LEFT)

    button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    window.mainloop()

if __name__ == "__main__":
    main()

