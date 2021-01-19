from tkinter import *


class WindowManager:

    # Open window asking user whether they would like a line graph or scatter plot
    def __init__(self):
        self.root = Tk()
        self.user_choice = None
        self.label = Label(
            text="Enter 1 for Tornado vs Sunspot scatter plot\nor 2 for Tornado and Sunspot vs Time line graph")
        self.label.grid(column=0, row=0)
        self.button = Button(text="Enter", command=self.get_user_choice)
        self.button.grid(column=0, row=2)
        self.entry = Entry()
        self.entry.grid(column=0, row=1)
        self.root.mainloop()

    # Get user's input and close window
    def get_user_choice(self):
        self.user_choice = int(self.entry.get())
        self.root.destroy()
