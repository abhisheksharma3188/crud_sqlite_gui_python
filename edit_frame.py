import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class EditFrame:
    def __init__(self,root):
        self.frames_dictionary = None
        self.id_var = None
        self.conn = None
        self.cursor = None
        self.users = None

        self.frame = tk.Frame(root)
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)  # this adds frame to window at x=0 and y=0 and then make it acquire full height and width

        self.canvas = tk.Canvas(self.frame)
        self.scrollbar_y = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.inner_frame = tk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw", width=self.canvas.winfo_screenwidth())
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.frame.bind("<Configure>", self.on_canvas_configure)

        self.label_frame = tk.LabelFrame(self.inner_frame, text="Edit Data", font=("Helvetica", 16))
        self.label_frame.pack(padx=20, pady=20)

        self.id_label = tk.Label(self.label_frame, font=("Helvetica", 16), anchor='w')
        self.id_label.grid(row=0, column=0, padx=40, pady=(10, 0), sticky="news")

        self.name_label = tk.Label(self.label_frame, text="Enter Name :", font=("Helvetica", 16), anchor='w')
        self.name_label.grid(row=1, column=0, padx=40, pady=(10,0), sticky="news")

        self.name_entry_var=tk.StringVar()
        self.name_entry = tk.Entry(self.label_frame, font=("Helvetica", 16), textvariable=self.name_entry_var)
        self.name_entry.grid(row=2, column=0, padx=40, pady=(5,10), sticky="news")

        self.surname_label = tk.Label(self.label_frame, text="Enter Surname :", font=("Helvetica", 16), anchor='w')
        self.surname_label.grid(row=3, column=0, padx=40, pady=(10, 0), sticky="news")

        self.surname_entry_var = tk.StringVar()
        self.surname_entry = tk.Entry(self.label_frame, font=("Helvetica", 16), textvariable=self.surname_entry_var)
        self.surname_entry.grid(row=4, column=0, padx=40, pady=(5, 10), sticky="news")

        self.email_label = tk.Label(self.label_frame, text="Your Email :", font=("Helvetica", 16), anchor='w')
        self.email_label.grid(row=5, column=0, padx=40, pady=(10, 0), sticky="news")

        self.email_entry_var = tk.StringVar()
        self.email_entry = tk.Entry(self.label_frame, font=("Helvetica", 16),textvariable=self.email_entry_var)
        self.email_entry.grid(row=6, column=0, padx=40, pady=(5, 10), sticky="news")

        self.gender_label = tk.Label(self.label_frame, text="Your Gender :", font=("Helvetica", 16), anchor='w')
        self.gender_label.grid(row=7, column=0, padx=40, pady=(10, 0), sticky="news")

        self.gender_combobox_items = ["Male", "Female", "Transgender"]
        self.gender_combobox = ttk.Combobox(self.label_frame, font=("Helvetica", 16), values=self.gender_combobox_items, state='readonly')
        self.gender_combobox.grid(row=8, column=0, padx=40, pady=(5, 10), sticky="news")

        self.age_label = tk.Label(self.label_frame, text="Your Age :", font=("Helvetica", 16), anchor='w')
        self.age_label.grid(row=9, column=0, padx=40, pady=(10, 0), sticky="news")

        self.age_combobox_items=[]
        for x in range(1,111):
            self.age_combobox_items.append(str(x))
        self.age_combobox = ttk.Combobox(self.label_frame, font=("Helvetica", 16), values=self.age_combobox_items, state='readonly')
        self.age_combobox.grid(row=10, column=0, padx=40, pady=(5, 10), sticky="news")

        self.submit_button = tk.Button(self.label_frame, text="Submit", font=("Helvetica", 16), command=self.submit_form)
        self.submit_button.grid(row=11, column=0, padx=40, pady=(10, 10), sticky="news")

        self.clear_button = tk.Button(self.label_frame, text="Clear", font=("Helvetica", 16), command=self.clear_form)
        self.clear_button.grid(row=12, column=0, padx=40, pady=(10, 10), sticky="news")

    def get_frame(self):
        return self.frame

    def set_frames_dictionary(self, frames_dictionary):
        self.frames_dictionary = frames_dictionary

    def on_canvas_configure(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def clear_form(self):
        self.name_entry_var.set("")
        self.surname_entry_var.set("")
        self.email_entry_var.set("")
        self.gender_combobox.set("")
        self.age_combobox.set("")

    def set_id_variable(self, id_variable):
        self.id_var = id_variable
        self.id_label.config(text=f"Id : {self.id_var}")

    def fetch_id_data(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect('my_database.db')
        self.cursor = self.conn.cursor()

        # Retrieve all users
        self.cursor.execute(f'SELECT * FROM users WHERE id = {self.id_var}')
        self.users = self.cursor.fetchone()

        #print(self.users)

        self.name_entry_var.set(self.users[1])
        self.surname_entry_var.set(self.users[2])
        self.email_entry_var.set(self.users[3])
        self.gender_combobox.set(self.users[4])
        self.age_combobox.set(self.users[5])

        # Close the connection
        self.conn.close()

    def submit_form(self):
        id = self.id_var
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()
        gender = self.gender_combobox.get()
        age = self.age_combobox.get()

        if not name or name.isspace():
            messagebox.showinfo("Error", "Name cannot be empty.")
            return
        if not surname or surname.isspace():
            messagebox.showinfo("Error", "Surame cannot be empty.")
            return
        if not email or email.isspace():
            messagebox.showinfo("Error", "Email cannot be empty.")
            return
        if not gender or gender.isspace():
            messagebox.showinfo("Error", "Gender cannot be empty.")
            return
        if not age or age.isspace():
            messagebox.showinfo("Error", "Age cannot be empty.")
            return

        # Connect to SQLite database
        self.conn = sqlite3.connect('my_database.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('UPDATE users SET name = ?, surname = ?, email = ?, gender = ?, age = ? WHERE id = ?',
                            (name, surname, email, gender, age, id))

        # Commit the transaction and close the connection
        self.conn.commit()
        self.conn.close()

        messagebox.showinfo("Success", "Data Updated Succesfully.")




