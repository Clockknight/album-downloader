import tkinter as tk

label_text = ""


def main():
    root = build_window()
    build_functions(root)
    build_io(root)
    root.mainloop()


def build_window():
    root = tk.Tk()
    root.geometry("1000x800")
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


def build_io(root):
    # column 2
    # row 0
    # output

    # row 1
    input_label = tk.Label(root, text=label_text)
    input_textbox = tk.Entry(root, text="Input here")
    input_button = tk.Button(root, text="ENTER")

    input_label.grid(row=1, column=2)
    input_textbox.grid(row=1, column=2)
    input_button.grid(row=1, column=2)

