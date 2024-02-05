import tkinter as tk
import sqlite3
from tkinter import messagebox

class ViewFrame:
    def __init__(self,root):
        self.frames_dictionary = None
        self.conn = None
        self.cursor = None
        self.columns = None
        self.users = None
        self.result_as_dict = None

        self.edit_frame_obj = None

        self.frame = tk.Frame(root)
        self.frame.place(x=0, y=0, relwidth=1,relheight=1)  # this adds frame to window at x=0 and y=0 and then make it acquire full height and width

        self.canvas = tk.Canvas(self.frame)
        self.scrollbar_y = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.inner_frame = tk.Frame(self.canvas,)

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw", width=self.canvas.winfo_screenwidth())
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.frame.bind("<Configure>", self.on_canvas_configure)

        self.page_label = tk.Label(self.inner_frame, text="Data", font=("Helvetica", 16))
        self.page_label.pack(pady=(20, 0))

        self.headings_frame = tk.Frame(self.inner_frame)
        self.headings_frame.pack(pady=(20, 0))

        self.name_heading_label = tk.Label(self.headings_frame, text="Id", width=6, bd=2, relief="solid", font=("Helvetica", 16), padx=5, pady=5)
        self.name_heading_label.grid(row=0, column=0)

        self.name_heading_label = tk.Label(self.headings_frame, text="Name", width=20, bd=2, relief="solid", font=("Helvetica", 16), padx=5, pady=5)
        self.name_heading_label.grid(row=0, column=1)

        self.surname_heading_label = tk.Label(self.headings_frame, text="Surname", width=20, bd=2, relief="solid", font=("Helvetica", 16), padx=5, pady=5)
        self.surname_heading_label.grid(row=0, column=2)

        self.email_heading_label = tk.Label(self.headings_frame, text="Email", width=20, bd=2, relief="solid", font=("Helvetica", 16), padx=5, pady=5)
        self.email_heading_label.grid(row=0, column=3)

        self.gender_heading_label = tk.Label(self.headings_frame, text="Gender", width=12, bd=2, relief="solid", font=("Helvetica", 16), padx=5, pady=5)
        self.gender_heading_label.grid(row=0, column=4)

        self.age_heading_label = tk.Label(self.headings_frame, text="Age", width=6, bd=2, relief="solid", font=("Helvetica", 16), padx=5, pady=5)
        self.age_heading_label.grid(row=0, column=5)

        self.edit_heading_label = tk.Label(self.headings_frame, text="Edit", width=6, bd=2, relief="solid", font=("Helvetica", 16), padx=5, pady=5)
        self.edit_heading_label.grid(row=0, column=6)

        self.delete_heading_label = tk.Label(self.headings_frame, text="Delete", width=7, bd=2, relief="solid", font=("Helvetica", 16), padx=5, pady=5)
        self.delete_heading_label.grid(row=0, column=7)

        self.data_frame = tk.Frame(self.inner_frame, bg="white")
        self.data_frame.pack(pady=(0, 0))

    def get_frame(self):
        return self.frame

    def set_frames_dictionary(self, frames_dictionary):
        self.frames_dictionary=frames_dictionary

    def open_main_frame(self):
        self.frames_dictionary["main_frame"].tkraise()

    def on_canvas_configure(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_edit_button_click(self, user_id):
        #print(f"You clicked edit button for id = {user_id}")
        self.edit_frame_obj.set_id_variable(user_id)
        self.edit_frame_obj.fetch_id_data()
        self.frames_dictionary["edit_frame"].tkraise()

    def on_delete_button_click(self,user_id):
        #print(f"You clicked delete button for id = {user_id}")

        result = messagebox.askquestion("Delete", f"Do you want to delete id = {user_id}?", icon='question')
        if result == 'yes':
            #print("User clicked 'Yes'")
            self.conn = sqlite3.connect('my_database.db')
            self.cursor = self.conn.cursor()

            self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))

            # Commit the transaction and close the connection
            self.conn.commit()
            self.conn.close()
            messagebox.showinfo("Success", "Data Deleted Successfully.")
            self.print_data()

    def print_data(self):
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        self.conn = sqlite3.connect('my_database.db')
        self.cursor = self.conn.cursor()

        # Retrieve all users
        self.cursor.execute('SELECT * FROM users')
        self.users = self.cursor.fetchall()

        self.columns = [desc[0] for desc in self.cursor.description]
        self.result_as_dict = [dict(zip(self.columns, row)) for row in self.users]

        # Display the users
        for index, user in enumerate(self.result_as_dict):
            id = user['id']
            name = user['name']
            surname = user['surname']
            email = user['email']
            gender = user['gender']
            age = user['age']

            tk.Label(self.data_frame, text=id, width=6, wraplength=60, bd=2, relief="solid", bg="white",
                     font=("Helvetica", 16), padx=5, pady=5, anchor="n").grid(row=index, column=0, sticky="nsew")

            tk.Label(self.data_frame, text=name, width=20, wraplength=235, bd=2, relief="solid", bg="white",
                     font=("Helvetica", 16), padx=5, pady=5, anchor="n").grid(row=index, column=1, sticky="nsew")

            tk.Label(self.data_frame, text=surname, width=20, wraplength=235, bd=2, relief="solid", bg="white",
                     font=("Helvetica", 16), padx=5, pady=5, anchor="n").grid(row=index, column=2, sticky="nsew")

            tk.Label(self.data_frame, text=email, width=20, wraplength=235, bd=2, relief="solid", bg="white",
                     font=("Helvetica", 16), padx=5, pady=5, anchor="n").grid(row=index, column=3, sticky="nsew")

            tk.Label(self.data_frame, text=gender, width=12, wraplength=140, bd=2, relief="solid", bg="white",
                     font=("Helvetica", 16), padx=5, pady=5, anchor="n").grid(row=index, column=4, sticky="nsew")

            tk.Label(self.data_frame, text=age, width=6, wraplength=60, bd=2, relief="solid", bg="white",
                     font=("Helvetica", 16), padx=5, pady=5, anchor="n").grid(row=index, column=5, sticky="nsew")

            tk.Button(self.data_frame, text="Edit", width=6, wraplength=80, bd=2, relief="solid",
                      font=("Helvetica", 16), padx=3, pady=5, fg="blue",
                      command=lambda uid=id: self.on_edit_button_click(uid)).grid(row=index, column=6, sticky="nsew")

            tk.Button(self.data_frame, text="Delete", width=7, wraplength=80, bd=2, relief="solid",
                      font=("Helvetica", 16), padx=3, pady=5, fg="blue",
                      command=lambda uid=id: self.on_delete_button_click(uid)).grid(row=index, column=7, sticky="nsew")

        # Close the connection
        self.conn.close()

    def set_edit_frame_object(self, edit_frame_obj):
        self.edit_frame_obj = edit_frame_obj

