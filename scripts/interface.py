import scripts.functions_input as input

import sys
import tkinter as tk
from tkinter import scrolledtext



def main():
    root = build_window()

    build_main(root)
    build_io(root)

    root.mainloop()


def build_window():
    root = tk.Tk()
    root.geometry("1000x800")
    content = tk.Frame(root)
    root.title("Clockknight's Album Downloader")

    text_var = tk.StringVar()
    text_var.set("Hello, World!")

    blah = tk.Label(root,
                    textvariable=text_var,
                    anchor=tk.CENTER,
                    bg="lightblue",
                    height=3,
                    width=30,
                    bd=3,
                    font=("Arial", 16, "bold"),
                    cursor="hand2",
                    fg="red",
                    padx=15,
                    pady=15,
                    justify=tk.CENTER,
                    relief=tk.RAISED,
                    underline=0,
                    wraplength=250
                    )

    return root


def build_main(root):
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
    button_frame = tk.Frame(root)

    for func in functions:
        button = tk.Button(button_frame,
                           text=func.__name__,
                           command=func
                           )

        button.grid(column=0)

    button_frame.grid(column=0, row=0)

def submit_text():
    print("yeh")


def build_io(root:tk.Tk):
    io_frame = tk.Frame(root)
    io_frame.grid(column=1, row=0)

    input_frame = tk.Frame(io_frame)
    input_frame.grid(column=1)

    instruction_text = "Please input your album of choice here."
    input_label = tk.Label(input_frame, text=instruction_text)
    input_textbox = tk.Entry(input_frame)
    input_button = tk.Button(input_frame, text="ENTER", command=submit_text)

    INPUT_COLUMN = 2
    input_label.grid(row=0, column=INPUT_COLUMN)
    input_textbox.grid(row=1, column=INPUT_COLUMN)
    input_button.grid(row=2, column=INPUT_COLUMN)


    output_frame = tk.Frame(io_frame, borderwidth=2, relief=tk.SUNKEN)
    output_frame.grid(column=1)

    output = tk.scrolledtext.ScrolledText(output_frame)
    output.grid()

    detail_frame = tk.Frame(root, borderwidth=2, relief=tk.SUNKEN)
    detail_frame.grid(column=2)

def settings():
    pass