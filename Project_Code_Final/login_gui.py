import tkinter as tk
import database_controller as con
from tkinter import messagebox

class login(tk.Frame):
    def __init__(self, root, con):
        super().__init__(root)

        user_entry = tk.StringVar()
        password_entry = tk.StringVar()
        self.state = True

        def on_click(user_entry, password_entry):
            user_exists = con.check_user_exists(user_entry.get())
            if user_exists:
                if con.login_user(user_entry.get(), password_entry.get()):
                    root.start_program(con.get_permission(user_entry.get()), user_entry.get())
                    self.destroy()
                    root.unbind("<Return>")

                else:
                    password_entry.delete(0, tk.END)
                    password_entry.focus()
                    messagebox.showerror(message="Incorrect password try again")

            else:
                user_entry.delete(0, tk.END)
                user_entry.focus()
                messagebox.showerror(message="Username does not exist try again")

        def toggle_show(pasw, show):
            if self.state is True:
                pasw.config(show="")
                show.config(text="Hide")
            else:
                pasw.config(show="*")
                show.config(text="Show")
            self.state = not(self.state)

        tk.Label(self, text="Username").grid(column=0, row=0, pady=10)
        first = tk.Entry(self, textvariable=user_entry)
        first.grid(column=0, row=1)
        first.focus()
        tk.Label(self, text="Password").grid(column=0, row=2, pady=10)
        password = tk.Entry(self,  textvariable=password_entry, show="*")
        password.grid(column=0, row=3)
        show = tk.Button(self, text="Show", command=lambda: toggle_show(password, show))
        show.grid(column=1, row=3)
        tk.Button(self, pady=10, padx=10, text="Go", command=lambda: on_click(first, password)).grid(pady=10, column=0, row=4)

        root.bind("<Return>", lambda _: on_click(first, password))


        self.grid_columnconfigure(0, weight=1)
