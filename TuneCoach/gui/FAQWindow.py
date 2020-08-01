import tkinter as tk
import tkinter.ttk as ttk
from TuneCoach.gui.constants import *


class FAQWindow:
    def __init__(self, mainWindow):
        faq_window = tk.Toplevel(mainWindow.master)
        faq_window.title("FAQ")
        faq_window.geometry()
        faq_window.minsize(width = 610, height = 380)
        faq_window.config(background="#f4f4f4")

        question_answer_list = [
            ('How do I use TuneCoach?', 'Detailed instructions can be found in "Tutorial" under the "Help" dropdown menu.\n'),
            ('Is there any way to change the intonation threshold?', 'Yes! It is located in the "Settings" dropdown menu, under "Tuner Settings".\n'),
            ('What instruments can I use with TuneCoach?', 'Any instrument can be used with TuneCoach! Even your voice!\n'),
            ('Why does the tuner not work?', 'Check your microphone. Ensure that it is fully plugged in and is recognized as audio input.\n' \
                                             'Other apps and programs may be using the microphone, blocking access to TuneCoach.\n' \
                                             'Other apps must be closed in this case. If it does not help, try restarting TuneCoach or your PC.\n'
                                             'Microphone permissions may be blocked. Check system settings to allow the microphone to be used with TuneCoach.\n'),
            ('Do I need internet to use TuneCoach?', 'No! Once TuneCoach is downloaded and installed, it can be used at any time!\n'),
            ('Why am I not in tune?', 'Git gud bro\n')
        ]

        faq_question_label_style = ttk.Style()
        faq_question_label_style.configure("FaqQuestionLabel.TLabel", foreground="white", background="grey", font=("Ubuntu 16"), width=70, anchor=tk.W)
        faq_answer_label_style = ttk.Style()
        faq_answer_label_style.configure("FaqAnswerLabel.TLabel", width=100, anchor=tk.W)
        for question, answer in question_answer_list:
            question_label = ttk.Label(faq_window, text= "Q: " + question, style="FaqQuestionLabel.TLabel")
            question_label.pack()
            answer_label = ttk.Label(faq_window, text="\nA: " + answer, style="FaqAnswerLabel.TLabel")
            answer_label.pack()

        faq_window.lift(mainWindow.master)
