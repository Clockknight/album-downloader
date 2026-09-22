import scripts.functions_input as input

import sys
import tkinter as tk
from tkinter import scrolledtext

inter_root = None


def main():
    global inter_root
    inter_root = build_window()

    build_main()
    build_io()

    inter_root.mainloop()


def build_window():
    """
    Builds the frame of the window for the GUI
    """
    global inter_root

    inter_root = tk.Tk()
    inter_root.geometry("1000x800")
    inter_root.title("Clockknight's Album Downloader")

    # content = tk.Frame(inter_root)
    # content.grid(column=4, row=4)

    # text_var = tk.StringVar()
    # text_var.set("Hello, World!")
    # blah = tk.Label(inter_root,
    #                 textvariable=text_var,
    #                 anchor=tk.CENTER,
    #                 bg="lightblue",
    #                 height=3,
    #                 width=30,
    #                 bd=3,
    #                 font=("Arial", 16, "bold"),
    #                 cursor="hand2",
    #                 fg="red",
    #                 padx=15,
    #                 pady=15,
    #                 justify=tk.CENTER,
    #                 relief=tk.RAISED,
    #                 underline=0,
    #                 wraplength=250
    #                 )


    return inter_root


def build_main():
    functions = [
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
    button_frame = tk.Frame(inter_root)

    for func in functions:
        button = tk.Button(button_frame,
                           text=func.__name__,
                           command=func
                           )

        button.grid(column=0)

    button_frame.grid(column=0, row=0)

def build_io():
    io_frame = tk.Frame(inter_root)
    io_frame.grid(row=0, column=1)

    input_frame = tk.Frame(io_frame)
    input_frame.grid(column=1)

    instruction_text = "Please input your album of choice here."
    input_label = tk.Label(input_frame, text=instruction_text)
    input_textbox = tk.Entry(input_frame, state='disabled')
    input_button = tk.Button(input_frame, text="ENTER", command=await_response, state='disabled')

    input_label.grid(row=0)
    input_textbox.grid(row=1)
    input_button.grid(row=2)


    output_frame = tk.Frame(io_frame, borderwidth=2, relief=tk.SUNKEN)
    output_frame.grid(column=1)
    output = tk.scrolledtext.ScrolledText(output_frame)
    output.pack()

    # detail_frame = tk.Frame(inter_root, borderwidth=2, relief=tk.SUNKEN)
    # detail_frame.grid(column=2)




def settings():
    pass

def await_response(new_text):
    global inter_root
    test = inter_root.children['!frame2'].children['!frame2'].children['!frame'].children['!scrolledtext']
    # TODO this
    # var old_text = textbox.text
    # new_text = old_text + new_text
    # textbox.text = new_text
    # TODO how to send function on tkinter button press?
    # maybe two functions?
    # maybe pressing calls something in functions_input?
    print(inter_root)