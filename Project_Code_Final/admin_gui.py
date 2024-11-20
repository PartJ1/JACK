import tkinter as tk
from tkinter import messagebox

class create_account(tk.Frame):
    def __init__(self, root, conn):
        super().__init__(root)

        self.con = conn
        first_name = tk.StringVar()
        second_name = tk.StringVar()
        email = tk.StringVar()
        password_entry = tk.StringVar()
        reenterpassword = tk.StringVar()
        selected_value = tk.StringVar()
        self.state = True

        def on_click():
            print(selected_value.get())
            if first.get() == "":
                messagebox.showerror(message="Please enter first name.")
            elif l_name.get() == "":
                messagebox.showerror(message="Please enter second name.")
            elif email.get() == "":
                messagebox.showerror(message="Please enter your email.")
            elif password.get() == "":
                messagebox.showerror(message="Please enter a password.")
            elif repass.get() == "":
                messagebox.showerror(message="Please re-enter your password.")
            elif selected_value.get() == "":
                messagebox.showerror(message="Please select a account type.")
            elif password.get() != repass.get():
                messagebox.showerror(message="Your entered passwords dont match.")
            else:
                count = 0
                if len(l_name.get()) < 4:
                    username = l_name.get() + first.get()[0] + str(count)
                else:
                    username = l_name.get()[:4] + first.get()[0] + str(count)

                while self.con.check_user_exists(username):
                    count += 1
                    if len(l_name.get()) < 4:
                        username = l_name.get() + first.get()[0] + str(count)
                    else:
                        username = l_name.get()[:4] + first.get()[0] + str(count)

                self.con.create_user(first.get(), l_name.get(), username, email.get(), password.get(), selected_value.get())
                messagebox.showinfo(message=f"Created Account, Username: {username}")

        def toggle_show(pasw):
            if self.state is True:
                pasw[0].config(show="")
                pasw[1].config(show="")
            else:
                pasw[0].config(show="*")
                pasw[1].config(show="*")
            self.state = not(self.state)

        tk.Label(self, text="First Name").grid(column=1, row=0, pady=10)
        first = tk.Entry(self, textvariable=first_name)
        first.grid(column=1, row=1)
        first.focus()

        tk.Label(self, text="Last Name").grid(column=1, row=2, pady=10)
        l_name = tk.Entry(self,  textvariable=second_name)
        l_name.grid(column=1, row=3)

        tk.Label(self, text="email").grid(column=1, row=7, pady=10)
        l_name = tk.Entry(self,  textvariable=email)
        l_name.grid(column=1, row=8)

        tk.Label(self, text="Password").grid(column=1, row=9, pady=10)
        password = tk.Entry(self,  textvariable=password_entry, show="*")
        password.grid(column=1, row=10)

        tk.Label(self, text="Re Enter Password").grid(column=1, row=11, pady=10)
        repass = tk.Entry(self,  textvariable=reenterpassword, show="*")
        repass.grid(column=1, row=12)
        tk.Button(self, text="Show", command=lambda: toggle_show([password, repass])).grid(column=2, row=12)


        radiobutton1 = tk.Radiobutton(self, text="Admin", variable=selected_value, value="1")
        radiobutton2 = tk.Radiobutton(self, text="Standard", variable=selected_value, value="0")

        # Use grid to place the Radiobuttons
        radiobutton1.grid(column=1, row=13)
        radiobutton2.grid(column=1, row=14)

        tk.Button(self, pady=10, padx=10, text="Go", command=on_click).grid(pady=10, column=1, row=15)

class delete_account(tk.Frame):
    def __init__(self, root, conn):
        super().__init__(root)
        self.con = conn

        username_entry_1 = tk.Entry(self)
        username_entry_2 = tk.Entry(self)

        def delete_acnt():
            if username_entry_1.get() == username_entry_2.get():
                if self.con.check_user_exists(username_entry_1.get()) is True:
                    self.con.delete_user(username_entry_1.get())
                    messagebox.showinfo(message="User successfully deleted")
                    username_entry_1.delete(0, tk.END)
                    username_entry_2.delete(0, tk.END)
                else:
                    messagebox.showerror(message="User does not exist")

            else:
                messagebox.showerror(message="Usernames entered are not the same.")

        del_btn = tk.Button(self, text="Delete", command=delete_acnt)

        tk.Label(self, text="Enter Username: ").grid(row=0, column=0)
        username_entry_1.grid(row=0, column=1)
        tk.Label(self, text="Re-Enter Username: ").grid(row=1, column=0)
        username_entry_2.grid(row=1, column=1)
        del_btn.grid(row=2, column=1)


class change_password(tk.Frame):
    def __init__(self, root, conn):
        super().__init__(root)
        self.con = conn

        username_entry_1 = tk.Entry(self)
        username_entry_2 = tk.Entry(self)

        password_entry_1 = tk.Entry(self)
        password_entry_2 = tk.Entry(self)

        def change_acnt():
            if username_entry_1.get() == username_entry_2.get() or password_entry_1.get() == password_entry_2.get():
                if self.con.check_user_exists(username_entry_1.get()) is True:
                    self.con.delete_user(username_entry_1.get())
                    messagebox.showinfo(message="User successfully deleted")
                    username_entry_1.delete(0, tk.END)
                    username_entry_2.delete(0, tk.END)
                else:
                    messagebox.showerror(message="User does not exist")
            else:
                messagebox.showerror(message="Usernames entered are not the same.")

        change_btn = tk.Button(self, text="Edit Password", command=change_acnt)

        tk.Label(self, text="Enter Username: ").grid(row=0, column=0)
        username_entry_1.grid(row=0, column=1)
        tk.Label(self, text="Re-Enter Username: ").grid(row=1, column=0)
        username_entry_2.grid(row=1, column=1)
        tk.Label(self, text="Enter New Password: ").grid(row=0, column=0)
        password_entry_1.grid(row=0, column=1)
        tk.Label(self, text="Re-Enter New Password: ").grid(row=1, column=0)
        password_entry_2.grid(row=1, column=1)
        change_btn.grid(row=2, column=1)


if __name__ == "__main__":
    root = tk.Tk()
    delete_account(root, "phi").pack()
    root.mainloop()
