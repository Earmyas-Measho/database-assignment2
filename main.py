from tkinter import *

import Controller
import Model
import View

if __name__ == '__main__':
    root = Tk()
    root.geometry('600x450')
    controller = Controller.Controller(Model.Model(), View.View(root))
       
    root.mainloop()
