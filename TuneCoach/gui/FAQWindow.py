import tkinter as tk
from TuneCoach.gui.constants import *


class FAQWindow:
    def __init__(self, mainWindow):
        faq_window = tk.Toplevel(mainWindow.master)
        faq_window.geometry()

        message = "Q: How do I use TuneCoach?\n" \
                  "A: Thorough instructions can be found in \"Tutorial\" under the \"Help\" dropdown menu.\n" \
                  "\n" \
                  "Q: Is there any way to change the intonation threshold?\n" \
                  "A: Yes! It is located in the \"Settings\" dropdown menu, then \"Tuner Settings\"\n" \
                  "\n" \
                  "Q: What instruments can be used with TuneCoach?\n" \
                  "A: Any instrument can be used with TuneCoach! Even your voice!\n" \
                  "\n" \
                  "Q: Why does the tuner not work?\n" \
                  "A: Check your microphone. Ensure that it is fully plugged in and is recognized as audio input.\n" \
                  "    Other apps and programs may be using the microphone, blocking access to TuneCoach.\n" \
                  "    Other apps must be closed in this case. If it does not help, restart TuneCoach or your PC.\n" \
                  "    Microphone permissions may also be blocked. To fix this, go into your system settings\n" \
                  "    to allow the microphone to be used with TuneCoach.\n" \
                  "\n" \
                  "Q: Do I need internet to use TuneCoach?\n" \
                  "A: No! Once TuneCoach is downloaded and installed, it can be used at any time!\n" \
                  "\n" \
                  "Q: Why am I not in tune?\n" \
                  "A: Git gud bro\n"

        faq_label = tk.Label(faq_window, text=message, font=("Calibri", 12), justify=tk.LEFT)
        faq_label.config(bg=background_color, fg="white")
        faq_label.pack()
        faq_window.lift(mainWindow.master)
