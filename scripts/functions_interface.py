import tkinter
import sys



def init():
    window = build_interface()
    window.mainloop()


def build_interface():

    window = tkinter.Tk()
    window.geometry('1000x600')


    for thing in funcs:
        button = tkinter.Button(window, text=thing.__name__, command=thing)
        button.pack()

    return window
