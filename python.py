import customtkinter as ctk
import tkinter as tk
from random import shuffle, randint
from tkinter import PhotoImage
from time import sleep



def main():
    window = tk.Tk()
    window.geometry("1024x768")
    window.title("Quizmania")
    bg_image = PhotoImage(file="C:/Users/educa/OneDrive/Pictures/bg3.png")

    bg_label = tk.Label(window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)


    button_font = ctk.CTkFont(family="Helvetica", size=30)
    button1 = ctk.CTkButton(window, text="Quiz", width=200, height=100, fg_color="#76ABAE", font=button_font, border_width=2, corner_radius=2)
    button1.place(relx=0.3, rely=0.6, anchor=tk.CENTER)

    button2 = ctk.CTkButton(window, text="Factoids", width=200, height=100,  fg_color="#76ABAE", font=button_font, border_width=2, corner_radius=2)
    button2.place(relx=0.7, rely=0.6, anchor=tk.CENTER)


    window.mainloop()


def quiz_page():
    window = tk.Tk()
    window.geometry("1024x768")



if __name__ == "__main__":
    main()
