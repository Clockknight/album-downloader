import tkinter
import sys
import scripts.functions_input as input



def init():
    window = build_interface()
    window.mainloop()


def build_interface():

    window = tkinter.Tk()
    window.geometry('1000x600')

    funcs = [
        input.cache_input,
        input.album_search,
        input.artist_search,
        input.update,
        input.ignorant_download,
        input.scouting_toggle,
        input.url_input,
        settings,
        sys.exit
    ]

    for thing in funcs:
        button = tkinter.Button(window, text=thing.__name__, command=thing)
        button.pack()

    return window

def settings():
    pass