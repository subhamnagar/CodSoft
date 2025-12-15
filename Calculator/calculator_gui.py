import tkinter as tk
from tkinter import messagebox

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Calculator")
root.geometry("360x520")
root.minsize(320, 480)
root.configure(bg="#1f1f1f")

# Responsive grid
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

expression = ""

# ---------------- FUNCTIONS ----------------
def update_display(value):
    display_var.set(value)

def press(key):
    global expression

    if key in "+-*/":
        if expression and expression[-1] in "+-*/":
            expression = expression[:-1] + key
        else:
            expression += key
    else:
        expression += key

    update_display(expression)

def clear():
    global expression
    expression = ""
    update_display("")

def calculate():
    global expression
    try:
        result = str(eval(expression))
        update_display(result)
        expression = result
    except:
        messagebox.showerror("Error", "Invalid Expression")
        expression = ""
        update_display("")

# ---------------- DISPLAY ----------------
display_var = tk.StringVar()

display = tk.Entry(
    root,
    textvariable=display_var,
    font=("Segoe UI", 26),
    bg="#bdbdbd",
    fg="black",
    bd=0,
    justify="right"
)
display.grid(row=0, column=0, sticky="ew", padx=20, pady=20, ipady=15)

# ---------------- BUTTON FRAME ----------------
btn_frame = tk.Frame(root, bg="#1f1f1f")
btn_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

# Grid responsiveness
for i in range(4):
    btn_frame.columnconfigure(i, weight=1)
for i in range(4):
    btn_frame.rowconfigure(i, weight=1)

# ---------------- BUTTON CREATOR ----------------
def create_btn(text, row, col, color, command, colspan=1):
    btn = tk.Button(
        btn_frame,
        text=text,
        font=("Segoe UI", 18, "bold"),
        bg=color,
        fg="white",
        relief="flat",
        command=command
    )
    btn.grid(row=row, column=col, columnspan=colspan,
             sticky="nsew", padx=8, pady=8)

# ---------------- NUMBERS ----------------
buttons = [
    ("7",0,0), ("8",0,1), ("9",0,2),
    ("4",1,0), ("5",1,1), ("6",1,2),
    ("1",2,0), ("2",2,1), ("3",2,2),
    ("0",3,0), (".",3,1)
]

for txt, r, c in buttons:
    create_btn(txt, r, c, "#3b3b3b", lambda t=txt: press(t))

# ---------------- OPERATORS ----------------
create_btn("/", 0, 3, "#f59e0b", lambda: press("/"))
create_btn("*", 1, 3, "#f59e0b", lambda: press("*"))
create_btn("-", 2, 3, "#f59e0b", lambda: press("-"))
create_btn("+", 3, 3, "#f59e0b", lambda: press("+"))

# ---------------- EQUAL ----------------
create_btn("=", 3, 2, "#10b981", calculate)

# ---------------- CLEAR ----------------
clear_btn = tk.Button(
    root,
    text="C",
    font=("Segoe UI", 18, "bold"),
    bg="#ef4444",
    fg="white",
    relief="flat",
    command=clear
)
clear_btn.grid(row=2, column=0, sticky="ew", padx=20, pady=20, ipady=10)

# ---------------- RUN ----------------
root.mainloop()
