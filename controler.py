# Programme du logiciel de contrôle du MBot.

# Ajout des bibliothèques au programme
import tkinter as tk
from tkinter import ttk
import serial as serial

global communication

def testt(event, text):
    print(text)

def mainWindow():
    print("Démarrage...")

    window = tk.Tk()
    window.title("Contrôleur MBot")
    window.geometry('1000x500+50+50')
    window.resizable(False, False)
    window.iconbitmap('./assets/icon.ico')
    window.configure(bg="white")

    test = ttk.Button(window, text="TEST")
    test.pack()

    window.bind('<KeyPress-Up>', lambda eff: testt(eff, "OK"))
    window.bind('<KeyRelease-Up>', lambda eff: testt(eff, "NO"), add='+')

    window.mainloop()

if __name__ == "__main__":
    # communication = serial.Serial(port= "COM18", baudrate=115200, timeout=.1)
    mainWindow()