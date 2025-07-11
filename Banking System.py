from tkinter import *
from tkinter import messagebox, simpledialog

class BankSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("🏦 Bank Management System")
        self.master.geometry("600x500")
        self.master.configure(bg="#F9F9F9")

        self.users = {}

        # 🏷️ Title Label
        self.title_label = Label(master, text="🏦 Welcome to MyBank", font=("Segoe UI", 18, "bold"), bg="#F9F9F9", fg="#333")
        self.title_label.pack(pady=10)

        # Frame: Create Account
        self.create_account_frame = Frame(master, bg="#FFFFFF", bd=2, relief=RIDGE)
        self.create_account_frame.pack(pady=10, padx=20)

        Label(self.create_account_frame, text="Create Account", font=("Segoe UI", 14, "bold"), bg="#FFFFFF").grid(row=0, columnspan=2, pady=10)

        self._add_label_entry(self.create_account_frame, "Name:", 1)
        self._add_label_entry(self.create_account_frame, "Age:", 2)
        self._add_label_entry(self.create_account_frame, "Salary:", 3)
        self._add_label_entry(self.create_account_frame, "PIN:", 4, show="*")

        self.create_account_button = Button(self.create_account_frame, text="➕ Create Account", command=self.create_account,
                                            font=("Segoe UI", 11), bg="#4CAF50", fg="white", width=20)
        self.create_account_button.grid(row=5, column=1, pady=10)

        # Frame: Login
        self.login_frame = Frame(master, bg="#FFFFFF", bd=2, relief=RIDGE)
        self.login_frame.pack(pady=10, padx=20)

        Label(self.login_frame, text="Login", font=("Segoe UI", 14, "bold"), bg="#FFFFFF").grid(row=0, columnspan=2, pady=10)

        self.login_name_entry = self._add_label_entry(self.login_frame, "Name:", 1)
        self.login_pin_entry = self._add_label_entry(self.login_frame, "PIN:", 2, show="*")

        self.login_button = Button(self.login_frame, text="🔐 Login", command=self.login,
                                   font=("Segoe UI", 11), bg="#2196F3", fg="white", width=20)
        self.login_button.grid(row=3, column=1, pady=10)

        # Bind Enter key to login
        self.master.bind('<Return>', self.login)

        # Frame: User Details
        self.user_details_frame = Frame(master, bg="#F0FFF0")

        self.name_label2 = Label(self.user_details_frame, font=("Segoe UI", 12, "bold"), bg="#F0FFF0")
        self.age_label2 = Label(self.user_details_frame, font=("Segoe UI", 12, "bold"), bg="#F0FFF0")
        self.salary_label2 = Label(self.user_details_frame, font=("Segoe UI", 12, "bold"), bg="#F0FFF0")
        self.current_balance_label = Label(self.user_details_frame, font=("Segoe UI", 12, "bold"), bg="#F0FFF0")

        self.name_label2.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        self.age_label2.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        self.salary_label2.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        self.current_balance_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)

        # Action Buttons
        self.deposit_button = Button(self.user_details_frame, text="💰 Deposit", command=self.deposit,
                                     bg="yellow", width=15)
        self.withdraw_button = Button(self.user_details_frame, text="💸 Withdraw", command=self.withdraw,
                                      bg="orange", width=15)
        self.view_transaction_button = Button(self.user_details_frame, text="📜 View Transactions", command=self.view_transaction_log,
                                              bg="#8BC34A", fg="white", width=20)
        self.logout_button = Button(self.user_details_frame, text="🚪 Logout", command=self.logout,
                                    bg="#f44336", fg="white", width=15)

        self.deposit_button.grid(row=4, column=0, pady=10)
        self.withdraw_button.grid(row=4, column=1, pady=10)
        self.view_transaction_button.grid(row=5, column=0, columnspan=2, pady=5)
        self.logout_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Internal state
        self.current_user_data = {}
        self.current_pin = ""

    def _add_label_entry(self, frame, text, row, show=None):
        label = Label(frame, text=text, font=("Segoe UI", 11), bg="#FFFFFF")
        label.grid(row=row, column=0, padx=10, pady=5, sticky=W)
        entry = Entry(frame, font=("Segoe UI", 11), show=show)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    def create_account(self):
        name = self.create_account_frame.grid_slaves(row=1, column=1)[0].get()
        age = self.create_account_frame.grid_slaves(row=2, column=1)[0].get()
        salary = self.create_account_frame.grid_slaves(row=3, column=1)[0].get()
        pin = self.create_account_frame.grid_slaves(row=4, column=1)[0].get()

        if not all([name, age, salary, pin]):
            messagebox.showerror("Error", "All fields are required!")
            return
        if not age.isdigit() or not salary.isdigit():
            messagebox.showerror("Error", "Age and Salary must be numbers!")
            return
        if not pin.isdigit() or len(pin) != 4:
            messagebox.showerror("Error", "PIN must be a 4-digit number!")
            return
        if pin in self.users:
            messagebox.showerror("Error", "User with this PIN already exists!")
            return

        self.users[pin] = {
            'name': name, 'age': age, 'salary': salary,
            'pin': pin, 'balance': 0, 'transaction_log': []
        }
        messagebox.showinfo("Success", "Account created successfully!")

        # Clear entries
        for row in range(1, 5):
            self.create_account_frame.grid_slaves(row=row, column=1)[0].delete(0, END)

    def login(self, event=None):
        name = self.login_name_entry.get()
        pin = self.login_pin_entry.get()

        if pin in self.users and self.users[pin]['name'] == name:
            self.current_user_data = self.users[pin]
            self.current_pin = pin
            self._update_user_details()
            self.create_account_frame.pack_forget()
            self.login_frame.pack_forget()
            self.user_details_frame.pack(pady=20)
        else:
            messagebox.showerror("Error", "Invalid name or PIN!")

    def _update_user_details(self):
        user = self.current_user_data
        self.name_label2.config(text=f"👤 Name: {user['name']}")
        self.age_label2.config(text=f"🎂 Age: {user['age']}")
        self.salary_label2.config(text=f"💼 Salary: {user['salary']}")
        self.current_balance_label.config(text=f"💲 Balance: ₹{user['balance']}")

    def deposit(self):
        amount = simpledialog.askstring("Deposit", "Enter amount:")
        if not amount or not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Error", "Invalid amount.")
            return
        amount = int(amount)
        self.current_user_data['balance'] += amount
        self.current_user_data['transaction_log'].append(f"Deposit: +₹{amount}")
        self._update_user_details()

    def withdraw(self):
        amount = simpledialog.askstring("Withdraw", "Enter amount:")
        if not amount or not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Error", "Invalid amount.")
            return
        amount = int(amount)
        if amount > self.current_user_data['balance']:
            messagebox.showerror("Error", "Insufficient balance.")
            return
        self.current_user_data['balance'] -= amount
        self.current_user_data['transaction_log'].append(f"Withdraw: -₹{amount}")
        self._update_user_details()

    def view_transaction_log(self):
        win = Toplevel(self.master)
        win.title("📜 Transaction Log")
        win.geometry("400x300")
        log_list = Listbox(win, font=("Segoe UI", 11))
        log_list.pack(padx=10, pady=10, fill=BOTH, expand=True)
        for txn in self.current_user_data['transaction_log']:
            log_list.insert(END, txn)

    def logout(self):
        self.current_user_data = {}
        self.current_pin = ""
        self.login_pin_entry.delete(0, END)
        self.user_details_frame.pack_forget()
        self.create_account_frame.pack(pady=10)
        self.login_frame.pack(pady=10)

def main():
    root = Tk()
    BankSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
