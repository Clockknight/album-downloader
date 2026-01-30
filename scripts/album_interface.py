import tkinter
import scripts.user_functions as user_functions


def init():
    window = build_interface()
    window.mainloop()


def build_interface():

    window = tkinter.Tk()
    window.geometry('1000x600')

    funcs = [
        user_functions.cache_input,
        user_functions.search_process,
        user_functions.artist_search,
        user_functions.update,
        user_functions.ignorant_download,
        user_functions.scouting_toggle,
        user_functions.url_input,
        settings,
        exit
    ]

    for thing in funcs:
        button = tkinter.Button(window, text=thing.__name__, command=thing)
        button.pack()

    return window

def settings():
    pass