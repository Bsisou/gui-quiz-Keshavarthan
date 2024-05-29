from tkinter import *
import customtkinter as ctk
from tkinter import PhotoImage
import random




def main():
    window = Tk()
    window.geometry("1024x768")
    window.title("Quizmania")
    bg_image = PhotoImage(file="C:\\Users\\educa\\OneDrive\\Pictures\\Screen 1@1x (3).png")

    bg_label = Label(window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)


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
