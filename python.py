import customtkinter as ctk
import tkinter as tk
from random import shuffle, randint
from PIL import Image, ImageTk
from time import sleep




class QuizApp(tk.Tk):
    def __init__(window):

        window = tk.Tk()
        window.geometry("1024x768")
        window.title("Quizmania")

        pil_image = Image.open('C:/Users/educa/OneDrive/Pictures/bg3.png')  # Replace with your image path
        window.bg_image = ImageTk.PhotoImage(pil_image)

        # Background label using the image
        window.bg_label = tk.Label(window, image=window.bg_image)
        window.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference to the image
        window.bg_label.image = window.bg_image

        window.home_frame = tk.Frame(window)
        window.home_frame.pack(fill='both', expand=True)


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
    app = QuizApp()
    app.mainloop()
