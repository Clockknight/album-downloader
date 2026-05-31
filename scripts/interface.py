import tkinter as tk
from tkinter import scrolledtext



def main():
    root = build_window()
    build_functions(root)
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

    build_functions(root)

    return root


def build_functions(root):
    functions = []

    for func in functions:
        button = tk.Button(root,
                           text=func.text,
                           command=func
                           )

        button.grid(column=0)

def submit_text():
    print("yeh")


def build_io(root:tk.Tk):
    io_frame = tk.Frame(root)
    io_frame.pack(side=tk.TOP)

    input_frame = tk.Frame(io_frame)
    input_frame.pack(side=tk.LEFT)

    instruction_text = "Please input your album of choice here."
    input_label = tk.Label(input_frame, text=instruction_text)
    input_textbox = tk.Entry(input_frame)
    input_button = tk.Button(input_frame, text="ENTER", command=submit_text)

    input_label.grid(row=0)
    input_textbox.grid(row=1)
    input_button.grid(row=2)


    output_frame = tk.Frame(io_frame, borderwidth=2, relief=tk.SUNKEN)
    output_frame.pack(side=tk.RIGHT)

    output = tk.scrolledtext.ScrolledText(output_frame)
    output.pack()

    detail_frame = tk.Frame(root, borderwidth=2, relief=tk.SUNKEN)
    detail_frame.pack(side=tk.BOTTOM)


