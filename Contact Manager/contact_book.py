import tkinter as tk
from tkinter import messagebox

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.root.geometry("700x450")
        self.root.minsize(650, 420)
        self.root.configure(bg="#f4f6fb")

        self.contacts = []
        self.selected_index = None

        # -------- GRID CONFIG --------
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)

        # -------- LEFT PANEL --------
        form_frame = tk.Frame(root, bg="#f4f6fb", padx=20, pady=20)
        form_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(form_frame, text="Contact Details",
                 font=("Segoe UI", 18, "bold"),
                 bg="#f4f6fb").pack(pady=10)

        self.name_entry = self.create_field(form_frame, "Name")
        self.phone_entry = self.create_field(form_frame, "Phone")
        self.email_entry = self.create_field(form_frame, "Email")
        self.address_entry = self.create_field(form_frame, "Address")

        tk.Button(form_frame, text="Save Contact",
                  bg="#4f46e5", fg="white",
                  font=("Segoe UI", 11),
                  relief="flat",
                  command=self.save_contact).pack(pady=10, fill="x")

        tk.Button(form_frame, text="Clear Fields",
                  bg="#94a3b8", fg="white",
                  relief="flat",
                  command=self.clear_fields).pack(fill="x")

        # -------- RIGHT PANEL --------
        list_frame = tk.Frame(root, bg="#f4f6fb", padx=20, pady=20)
        list_frame.grid(row=0, column=1, sticky="nsew")

        search_frame = tk.Frame(list_frame, bg="#f4f6fb")
        search_frame.pack(fill="x")

        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 12))
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.search_contact)

        tk.Button(search_frame, text="Search",
                  bg="#22c55e", fg="white",
                  relief="flat",
                  command=self.search_contact).pack(side="left")

        self.contact_list = tk.Listbox(
            list_frame,
            font=("Segoe UI", 12),
            activestyle="none",
            selectbackground="#c7d2fe"
        )
        self.contact_list.pack(fill="both", expand=True, pady=10)
        self.contact_list.bind("<<ListboxSelect>>", self.select_contact)

        action_frame = tk.Frame(list_frame, bg="#f4f6fb")
        action_frame.pack(fill="x")

        tk.Button(action_frame, text="✏ Edit Selected",
                  bg="#eab308", fg="black",
                  relief="flat",
                  command=self.edit_contact).pack(side="left", padx=5, expand=True, fill="x")

        tk.Button(action_frame, text="🗑 Delete Selected",
                  bg="#ef4444", fg="white",
                  relief="flat",
                  command=self.delete_contact).pack(side="left", padx=5, expand=True, fill="x")

        self.refresh_list()

    # -------- UI HELPERS --------
    def create_field(self, parent, label):
        tk.Label(parent, text=label, bg="#f4f6fb",
                 font=("Segoe UI", 11)).pack(anchor="w")
        entry = tk.Entry(parent, font=("Segoe UI", 12))
        entry.pack(fill="x", pady=5)
        return entry

    # -------- CORE LOGIC --------
    def save_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning("Missing Data", "Name and Phone are required")
            return

        if self.selected_index is not None:
            self.contacts[self.selected_index] = {
                "name": name, "phone": phone,
                "email": email, "address": address
            }
        else:
            self.contacts.append({
                "name": name, "phone": phone,
                "email": email, "address": address
            })

        self.selected_index = None
        self.refresh_list()
        self.clear_fields()

    def select_contact(self, event):
        try:
            self.selected_index = self.contact_list.curselection()[0]
        except:
            self.selected_index = None

    def edit_contact(self):
        if self.selected_index is None:
            messagebox.showwarning("Select Contact", "Select a contact first")
            return

        contact = self.contacts[self.selected_index]
        self.fill_fields(contact)

    def delete_contact(self):
        if self.selected_index is None:
            messagebox.showwarning("Select Contact", "Select a contact first")
            return

        del self.contacts[self.selected_index]
        self.selected_index = None
        self.refresh_list()
        self.clear_fields()

    def search_contact(self, event=None):
        query = self.search_entry.get().lower()
        self.contact_list.delete(0, tk.END)

        matches = [
            c for c in self.contacts
            if query in c["name"].lower() or query in c["phone"]
        ]

        if not matches:
            self.contact_list.insert(tk.END, "No contacts found")
            return

        for c in matches:
            self.contact_list.insert(tk.END, f"{c['name']} - {c['phone']}")

    def refresh_list(self):
        self.contact_list.delete(0, tk.END)
        for c in self.contacts:
            self.contact_list.insert(tk.END, f"{c['name']} - {c['phone']}")

    def fill_fields(self, contact):
        self.clear_fields()
        self.name_entry.insert(0, contact["name"])
        self.phone_entry.insert(0, contact["phone"])
        self.email_entry.insert(0, contact["email"])
        self.address_entry.insert(0, contact["address"])

    def clear_fields(self):
        for e in [self.name_entry, self.phone_entry,
                  self.email_entry, self.address_entry]:
            e.delete(0, tk.END)

# -------- RUN --------
root = tk.Tk()
ContactManager(root)
root.mainloop()
