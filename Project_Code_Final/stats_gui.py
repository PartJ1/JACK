import tkinter as tk
from tkinter import ttk
import stats_backend as stats
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Students(tk.Frame):
    def __init__(self, con, root):
        super().__init__(root)
        self.con = con
        self.setup_scroll()

        self.class_options = ["Pick a Class"] + ([i[0] for i in self.con.get_all_classes()])
        self.selected_class = tk.StringVar()
        self.selected_class.set(self.class_options[0])

        self.class_widget = ttk.OptionMenu(self, self.selected_class, *self.class_options)

        refresh_class_list = tk.Button(self, text="Refresh", command=self.refresh_classes)
        load_class_list = tk.Button(self, text="Load Class", command=self.load_class)

        self.class_widget.grid(row=0, column=0)
        load_class_list.grid(row=0, column=1)
        refresh_class_list.grid(row=0, column=2)

        self.loaded_student = False
        self.loaded_class = False

    def load_class(self):
        if self.selected_class.get() == "Pick a Class":
            tk.messagebox.showerror(message="Please load a class first")
            return False

        self.loaded_class = True

        class_name = self.selected_class.get()
        self.class_id = self.con.get_id_from_class_name(class_name)
        self.unpro_students = self.con.get_students_from_class(class_name)
        self.student_options = ["Pick a Student"] + [str(i[1]) + " | " + str(i[0]) for i in self.unpro_students]
        print(self.unpro_students)
        self.selected_student = tk.StringVar()
        self.selected_student.set(self.student_options[0])

        self.student_widget = ttk.OptionMenu(self, self.selected_student, *self.student_options)

        load_student_list = tk.Button(self, text="Load student", command=self.load_student)

        self.student_widget.grid(row=1, column=0, sticky="n")
        load_student_list.grid(row=1, column=1, sticky="n")

    def load_student(self):
        if self.selected_class.get() == "Pick a Student":
            tk.messagebox.showerror(message="Please load a student first")
            return False

        self.loaded_student = True
        student_id = int(self.selected_student.get().split(" | ")[0])

        self.canvas1 = FigureCanvasTkAgg(stats.student_pie_chart(student_id, self.con), master=self.inner_frame)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=1, column=0)

        self.canvas2 = FigureCanvasTkAgg(stats.student_attendance_over_time(self.class_id, student_id, self.con), master=self.inner_frame)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().grid(row=2, column=0)

        self.canvas3 = FigureCanvasTkAgg(stats.percentage_attendance_for_day_week(student_id, self.con), master=self.inner_frame)
        self.canvas3.draw()
        self.canvas3.get_tk_widget().grid(row=3, column=0)

    def refresh_classes(self):
        self.class_options = ["Pick a Class"] + ([i[0] for i in self.con.get_all_classes()])
        self.selected_class.set(self.class_options[0])
        self.class_widget.destroy()
        self.class_widget = ttk.OptionMenu(self, self.selected_class, *self.class_options)
        self.class_widget.grid(row=0, column=0)

        if self.loaded_student is True:
            self.canvas1.get_tk_widget().grid_forget()
            self.canvas2.get_tk_widget().grid_forget()
            self.canvas3.get_tk_widget().grid_forget()

    def setup_scroll(self):
        # Create a frame for the canvas and scrollbar
        scroll_frame = ttk.Frame(self)
        scroll_frame.grid(row=2, column=0, sticky='nsew')

        # Create a canvas
        self.canvas = tk.Canvas(scroll_frame, width=560, height=600)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(scroll_frame, orient='vertical', command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Configure canvas scrolling
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        # Bind the canvas to scroll when resized
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Optional: Add mouse scroll functionality
        self.inner_frame.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")



class Classes(tk.Frame):
    def __init__(self, con, root):
        super().__init__(root)
        self.con = con
        self.setup_scroll()

        self.class_options = ["Pick a Class"] + ([i[0] for i in self.con.get_all_classes()])
        self.selected_class = tk.StringVar()
        self.selected_class.set(self.class_options[0])

        self.class_widget = ttk.OptionMenu(self, self.selected_class, *self.class_options)

        refresh_class_list = tk.Button(self, text="Refresh", command=self.refresh_classes)
        load_class_list = tk.Button(self, text="Load", command=self.load_class)

        self.class_widget.grid(row=0, column=0)
        load_class_list.grid(row=0, column=1)
        refresh_class_list.grid(row=0, column=2)

        # canvas = FigureCanvasTkAgg(stats.all_students_bar(class_id, con), master=self)
        # canvas.draw()
        # canvas.get_tk_widget().grid

        self.loaded_class = False

    def refresh_classes(self):
        self.class_options = ["Pick a Class"] + ([i[0] for i in self.con.get_all_classes()])
        self.selected_class.set(self.class_options[0])
        self.class_widget.destroy()
        self.class_widget = ttk.OptionMenu(self, self.selected_class, *self.class_options)
        self.class_widget.grid(row=0, column=0)

        if self.loaded_class is True:
            self.canvas1.get_tk_widget().grid_forget()
            self.canvas2.get_tk_widget().grid_forget()
            self.canvas3.get_tk_widget().grid_forget()

        else:
            tk.messagebox.showerror(message="Please load a class first")

    def setup_scroll(self):
        # Create a frame for the canvas and scrollbar
        scroll_frame = ttk.Frame(self)
        scroll_frame.grid(row=1, column=0, sticky='nsew')

        # Create a canvas
        self.canvas = tk.Canvas(scroll_frame, width=560, height=600)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(scroll_frame, orient='vertical', command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Configure canvas scrolling
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        # Bind the canvas to scroll when resized
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Optional: Add mouse scroll functionality
        self.inner_frame.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def load_class(self):
        if self.selected_class.get() == "Pick a Class":
            tk.messagebox.showerror(message="Please load a class first")
            return False

        self.loaded_class = True

        class_name = self.selected_class.get()
        class_id = self.con.get_id_from_class_name(class_name)
        unpro_students = self.con.get_students_from_class(class_name)
        student_ids = [i[1] for i in unpro_students]

        # Plot all_students_bar in the scrollable frame
        canvas1 = FigureCanvasTkAgg(stats.all_students_bar(class_id, self.con), master=self.inner_frame)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=1, column=0)

        # Plot time_against_attendance in the scrollable frame
        canvas2 = FigureCanvasTkAgg(stats.time_against_attendance(class_id, self.con), master=self.inner_frame)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=2, column=0)

        canvas3 = FigureCanvasTkAgg(stats.attendance_against_week(class_id, self.con), master=self.inner_frame)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=3, column=0)

