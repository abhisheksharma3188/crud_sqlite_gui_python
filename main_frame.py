import tkinter as tk
import sqlite3


class MainFrame:
    def __init__(self, root):
        self.frames_dictionary = None
        self.view_frame_obj = None

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

        self.label_frame = tk.LabelFrame(self.inner_frame, text="Welcome", font=("Helvetica", 16))
        self.label_frame.pack(padx=20, pady=20)

        self.insert_button = tk.Button(self.label_frame, text="Insert", height=3, width=15, font=("Helvetica", 16), command=lambda: self.open_insert_frame())
        self.insert_button.grid(row=0, column=0, padx=40, pady=40)

        self.view_button = tk.Button(self.label_frame, text="View", height=3, width=15, font=("Helvetica", 16), command=lambda: self.open_view_frame())
        self.view_button.grid(row=0, column=1, padx=40, pady=40)


    def get_frame(self):
        return self.frame

    def set_frames_dictionary(self, frames_dictionary):
        self.frames_dictionary = frames_dictionary

    def set_view_frame_object(self,view_frame_object):
        self.view_frame_obj=view_frame_object

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def open_insert_frame(self):
        self.frames_dictionary["insert_frame"].tkraise()

    def open_view_frame(self):
        self.frames_dictionary["view_frame"].tkraise()
        self.view_frame_obj.print_data()



