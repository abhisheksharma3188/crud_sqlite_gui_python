import tkinter as tk
import sqlite3

from main_frame import MainFrame
from insert_frame import InsertFrame
from view_frame import ViewFrame
from edit_frame import EditFrame


class App:
    def __init__(self):

        # Connect to SQLite database (or create if not exists)
        self.conn = sqlite3.connect('my_database.db')
        self.cursor = self.conn.cursor()

        # Create users table if not exists
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                surname TEXT NOT NULL,
                                email TEXT NOT NULL,
                                gender TEXT NOT NULL,
                                age TEXT NOT NULL
                            )
                        ''')

        # Commit the transaction and close the connection
        self.conn.commit()
        self.conn.close()

        self.root = tk.Tk()

        self.root.geometry("800x500")
        self.root.state('zoomed')

        self.root.title("Records App")

        # code to create menu below
        self.menu_bar = tk.Menu(self.root)  # this creates menu
        self.menu_bar.add_command(label="Main", command=lambda: self.open_main_frame())  # this adds menu item
        self.menu_bar.add_command(label="Insert", command=lambda: self.open_insert_frame())  # this add menu item
        self.menu_bar.add_command(label="View", command=lambda:self.open_view_frame())  # this adds menu item
        self.root.config(menu=self.menu_bar)  # this adds menu to window
        # code to create menu above

        self.frames_dictionary={}

        self.main_frame_obj = MainFrame(self.root)  # this creates object of Frame1 class
        self.main_frame = self.main_frame_obj.get_frame()
        self.frames_dictionary["main_frame"]=self.main_frame

        self.insert_frame_obj = InsertFrame(self.root)  # this creates object of Frame1 class
        self.insert_frame = self.insert_frame_obj.get_frame()
        self.frames_dictionary["insert_frame"] = self.insert_frame

        self.view_frame_obj = ViewFrame(self.root)  # this creates object of Frame1 class
        self.view_frame = self.view_frame_obj.get_frame()
        self.frames_dictionary["view_frame"] = self.view_frame

        self.edit_frame_obj = EditFrame(self.root)  # this creates object of Frame1 class
        self.edit_frame = self.edit_frame_obj.get_frame()
        self.frames_dictionary["edit_frame"] = self.edit_frame

        self.main_frame_obj.set_frames_dictionary(self.frames_dictionary)
        self.view_frame_obj.set_frames_dictionary(self.frames_dictionary)
        self.insert_frame_obj.set_frames_dictionary(self.frames_dictionary)
        self.edit_frame_obj.set_frames_dictionary(self.frames_dictionary)

        self.main_frame_obj.set_view_frame_object(self.view_frame_obj)
        self.view_frame_obj.set_edit_frame_object(self.edit_frame_obj)

        self.open_main_frame()

        self.root.mainloop()

    def open_main_frame(self):
        self.main_frame.tkraise()

    def open_insert_frame(self):
        self.insert_frame.tkraise()

    def open_view_frame(self):
        self.view_frame.tkraise()
        self.view_frame_obj.print_data()



app = App()
