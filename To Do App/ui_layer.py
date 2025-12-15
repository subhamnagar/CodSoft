import tkinter as tk
from tkinter import messagebox
from task_controller import TaskController
from data_store import load_tasks, save_tasks

class TodoUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python To-Do Manager")
        self.root.geometry("500x420")     # shorter window on open
        self.root.minsize(450, 380)
        self.root.configure(bg="#f4f6fb")

        self.controller = TaskController()
        self.controller.tasks = load_tasks()

        # ---------- GRID CONFIG ----------
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        # ---------- HEADER ----------
        tk.Label(
            root,
            text="My To-Do List",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f6fb",
            fg="#333"
        ).grid(row=0, column=0, pady=(15, 8))

        # ---------- INPUT ----------
        input_frame = tk.Frame(root, bg="#f4f6fb")
        input_frame.grid(row=1, column=0, sticky="ew", padx=20)
        input_frame.columnconfigure(0, weight=1)

        self.task_input = tk.Entry(input_frame, font=("Segoe UI", 14))
        self.task_input.grid(row=0, column=0, sticky="ew", ipady=6, padx=(0, 10))
        self.task_input.bind("<Return>", lambda e: self.add_task())  # ENTER key

        tk.Button(
            input_frame,
            text="+",
            font=("Segoe UI", 16, "bold"),
            bg="#4f46e5",
            fg="white",
            width=4,
            relief="flat",
            command=self.add_task
        ).grid(row=0, column=1)

        # ---------- TASK LIST ----------
        list_frame = tk.Frame(root, bg="#f4f6fb")
        list_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=12)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.task_list = tk.Listbox(
            list_frame,
            font=("Segoe UI", 13),
            activestyle="none",
            selectbackground="#c7d2fe"
        )
        self.task_list.grid(row=0, column=0, sticky="nsew")
        self.task_list.bind("<Button-1>", self.toggle_on_click)

        scrollbar = tk.Scrollbar(list_frame, command=self.task_list.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.task_list.config(yscrollcommand=scrollbar.set)

        # ---------- ACTION BUTTONS ----------
        action_frame = tk.Frame(root, bg="#f4f6fb")
        action_frame.grid(row=3, column=0, pady=(5, 15))

        tk.Button(
            action_frame,
            text="🧹 Clear Completed",
            font=("Segoe UI", 11),
            bg="#22c55e",
            fg="white",
            relief="flat",
            padx=14,
            pady=6,
            command=self.clear_completed
        ).grid(row=0, column=0, padx=6)

        tk.Button(
            action_frame,
            text="🗑 Delete Selected",
            font=("Segoe UI", 11),
            bg="#ef4444",
            fg="white",
            relief="flat",
            padx=14,
            pady=6,
            command=self.delete_task
        ).grid(row=0, column=1, padx=6)

        self.refresh()

    # ---------- FUNCTIONS ----------
    def refresh(self):
        self.task_list.delete(0, tk.END)
        for task in self.controller.tasks:
            icon = "☑" if task["completed"] else "☐"
            self.task_list.insert(tk.END, f"{icon}  {task['title']}")
        save_tasks(self.controller.tasks)

    def add_task(self):
        title = self.task_input.get().strip()
        if title:
            self.controller.add_task(title)
            self.task_input.delete(0, tk.END)
            self.refresh()

    def toggle_on_click(self, event):
        index = self.task_list.nearest(event.y)
        if index >= 0:
            self.controller.toggle_status(index)
            self.refresh()

    def delete_task(self):
        try:
            index = self.task_list.curselection()[0]
            self.controller.delete_task(index)
            self.refresh()
        except IndexError:
            messagebox.showwarning("Select Task", "Please select a task")

    def clear_completed(self):
        self.controller.tasks = [
            task for task in self.controller.tasks if not task["completed"]
        ]
        self.refresh()
