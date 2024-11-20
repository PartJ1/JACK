import tkinter as tk
from datetime import date
import os
import numpy as np
from PIL import Image, ImageTk
from tkinter import ttk
import admin_gui
import cv2
import matplotlib.pyplot as plt
from tkinter import messagebox
import class_gui
import MachineLearning as ml
from tkcalendar import DateEntry
import stats_gui


class AdminMenu(tk.Frame):
    def __init__(self, root, con):
        super().__init__(root)

        noteb = ttk.Notebook(self)
        noteb.grid(row=0, column=0)

        create_account_frame = admin_gui.create_account(self, con)
        change_password_frame = admin_gui.change_password(self, con)
        delete_account_frame = admin_gui.delete_account(self, con)

        noteb.add(create_account_frame, text="Create Account")
        noteb.add(change_password_frame, text="Change Password")
        noteb.add(delete_account_frame, text="Delete Account")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class ClassManagement(tk.Frame):
    def __init__(self, root, con, username):
        super().__init__(root)

        noteb = ttk.Notebook(self)
        noteb.grid(row=0, column=0)

        create_class_frame = class_gui.AddClass(self, con, username)
        delete_class_frame = class_gui.DeleteClass(self, con)

        noteb.add(create_class_frame, text="Create Class")
        noteb.add(delete_class_frame, text="Delete Class")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class Statistics(tk.Frame):
    def __init__(self, root, con):
        super().__init__(root, width=5000)

        noteb = ttk.Notebook(self, width=700, height=700)
        noteb.grid(row=0, column=0)

        class_stat_gui = stats_gui.Classes(con, self)
        student_gui = stats_gui.Students(con, self)

        noteb.add(class_stat_gui, text="Class")
        noteb.add(student_gui, text="Students")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class AttendanceMenu(tk.Frame):
    def __init__(self, root, conn):
        super().__init__(root)
        self.grid()

        self.con = conn
        self.loaded = False

        self.class_options = ["Pick a Class"] + ([i[0] for i in conn.get_all_classes()])
        self.selected_class = tk.StringVar()
        self.selected_class.set(self.class_options[0])

        self.webcam_options = ["Pick a webcam"]
        webcams = self.list_connected_webcams()
        self.webcam_options.extend(webcams)

        self.selected_webcam = tk.StringVar()
        self.selected_webcam.set(self.webcam_options[0])

        self.class_widget = ttk.OptionMenu(self, self.selected_class, *self.class_options)
        webcam_widget = ttk.OptionMenu(self, self.selected_webcam, *self.webcam_options)

        refresh_class_list = tk.Button(self, text="Refresh", command=self.refresh_classes)
        load_class_list = tk.Button(self, text="Load", command=self.load_class)


        self.table = ttk.Treeview(self, columns=["name", "present"], show="headings")
        self.table.heading("name", text="Name")
        self.table.heading("present", text="Present")

        present_btn = tk.Button(self, text="toggle attendance of selected", command=self.toggle_attendance)
        self.start_btn = tk.Button(self, text="Start Detecting", command=self.check_fields)
        save_btn = tk.Button(self, text="Save Attendance", command=self.save_attendance)

        self.class_widget.grid(row=0, column=0)
        load_class_list.grid(row=0, column=1)
        refresh_class_list.grid(row=0, column=2)
        webcam_widget.grid(row=1, column=0)
        self.table.grid(row=2, column=0)
        present_btn.grid(row=3, column=0)
        self.start_btn.grid(row=4, column=0)
        save_btn.grid(row=5, column=0)

        # self.table.insert(parent="", index=0, values=('John Smith', 1))
        # self.table.insert(parent="", index=0, values=('John Tuff', 0))

    def save_attendance(self):
        def date_entry_command():
            self.date_entry = DateEntry(self)
            self.date_entry.grid(row=7, column=0)
            self.cust_date = True

        def save_students():
            if self.cust_date is True:
                current_date = "-".join(str(self.date_entry.get_date()).split("-")[::-1])

            else:
                current_date = date.today().strftime("%d-%m-%Y")

            current_class = self.selected_class.get()
            class_id = self.con.get_id_from_class_name(current_class)

            for item in self.table.get_children():
                values = self.table.item(item, 'values')
                student_id = self.con.get_student_id_from_class_and_name(class_id, values[0])
                self.con.add_attendance(student_id, class_id, current_date, int(values[1]))

            messagebox.showinfo(message="Data has been saved.")

        if self.loaded is False:
            messagebox.showerror(message="Please load the class with the button next to the pick class menu.")
        else:
            # add some diologue
            self.cust_date = False

            date_button = tk.Button(self, text="Enter custom date\n(do not click if you want to use the currentdate of your system)", command=date_entry_command)

            go_btn = tk.Button(self, text="Save", command=save_students)

            # Use grid to place the Radiobuttons
            date_button.grid(row=6, column=0)
            go_btn.grid(row=8, column=0)

    def check_fields(self):
        if self.selected_webcam.get() == self.webcam_options[0]:
            messagebox.showerror(message="Please select a webcam")
            pass
        elif self.selected_class.get() == self.class_options[0]:
            messagebox.showerror(message="Please select a class")
            pass
        elif self.loaded is False:
            messagebox.showerror(message="Please load the class with the button next to the pick class menu.")
            pass 
        else:
            self.start_btn.config(state="disabled")
            self.take_images()

    def load_class(self):
        class_name = self.selected_class.get()
        unpro_students = self.con.get_students_from_class(class_name)
        student_ids = [i[1] for i in unpro_students]
        self.loaded = True

        for item in self.table.get_children():
            self.table.delete(item)

        for i in unpro_students:
            self.table.insert(parent="", index=0, values=(i[0], 0))

    def refresh_classes(self):
        self.class_options = ["Pick a Class"] + ([i[0] for i in self.con.get_all_classes()])
        self.selected_class.set(self.class_options[0])
        self.class_widget.destroy()
        self.class_widget = ttk.OptionMenu(self, self.selected_class, *self.class_options)
        self.class_widget.grid(row=0, column=0)

    def toggle_attendance(self):
        for i in self.table.selection():
            current_values = self.table.item(i, 'values')
            if int(current_values[1]) == 1:
                self.table.item(i, values=(current_values[0], 0))
            else:
                self.table.item(i, values=(current_values[0], 1))

    @staticmethod
    def list_connected_webcams():
        webcam_indices = []
        index = 0
        while True:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                webcam_indices.append(str(index))  # Append index as a string for display purposes
                cap.release()  # Release the video capture object
            else:
                break
            index += 1
        return webcam_indices

    def take_images(self):
        def update_present(name_to_find, new_value):
            for item in self.table.get_children():
                values = self.table.item(item, "values")
                if values[0] == name_to_find:
                    self.table.set(item, "present", new_value)

        def start_video():
            if self.video_running:
                return  # Prevent multiple instances of video feed

            self.video_running = True

            self.cap = cv2.VideoCapture(int(self.selected_webcam.get()))
            self.count = 0
            self.images = np.zeros((10, 200, 200, 3))
            self.model = ml.UseModel(os.path.join("data", str(self.con.get_id_from_class_name(self.selected_class.get())), "base.keras"))

            def update_video():
                ret, frame = self.cap.read()
                if ret:
                    start_point = (225, 100)  # Top-left corner
                    end_point = (500, 400)    # Bottom-right corner
                    color = (0, 255, 0)       # Green color in BGR
                    thickness = 2             # Thickness of the rectangle
                    cv2.rectangle(frame, start_point, end_point, color, thickness)

                    # Convert the frame to a format suitable for Tkinter
                    image = (cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    img = ImageTk.PhotoImage(Image.fromarray(image))

                    self.images[self.count] = cv2.resize(image[100:400, 225:500], (200, 200)) / 255.

                    if self.count == 9:
                        result = self.model.process_image(self.images)
                        print(result)
                        if result["confidence"] >= 0.6:
                            # find name based on relitive id and class id
                            class_id = self.con.get_id_from_class_name(self.selected_class.get())
                            student_name = self.con.get_name_from_relitive_id_and_class(result["result"], class_id)
                            update_present(student_name, 1)
                        self.count = -1

                    self.count += 1

                    video_widget['image'] = img
                    video_widget.image = img  # To prevent garbage collection

                if self.video_running:
                    self.after(10, update_video)  # Refresh rate (in milliseconds)

            update_video()

        def stop_video():
            self.video_running = False
            if self.cap:
                self.cap.release()
            video_widget['image'] = ''  # Clear the video widget

        def on_closing():
            self.start_btn.config(state="normal")
            stop_video()
            root.destroy()

        root = tk.Toplevel()

        self.video_frame = tk.Frame(root)
        video_widget = tk.Label(self.video_frame)
        self.video_frame.grid(column=1, row=0)
        video_widget.grid(column=0, row=1)

        start_btn = tk.Button(root, text="Start Video", command=start_video)
        start_btn.grid(column=0, row=1)

        stop_btn = tk.Button(root, text="Stop Video", command=stop_video)
        stop_btn.grid(column=1, row=1)

        root.protocol("WM_DELETE_WINDOW", on_closing)

        self.video_running = False
        start_video()

