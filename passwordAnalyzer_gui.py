import tkinter as tk
from tkinter import messagebox
import re
import string
import random as pyrandom

def is_strong_password(password):
    if not (8 <= len(password) <= 64):
        return False, "Password must be between 8 and 64 characters."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number."
    if not re.search(r'[^A-Za-z0-9]', password):
        return False, "Password must contain at least one special character."
    return True, "Password is strong."

class PasswordAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Analyzer")
        self.setup_gui()

    def setup_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)
        tk.Label(frame, text="Enter your password:").grid(row=0, column=0, sticky='w')
        self.pwd_var = tk.StringVar()
        self.entry = tk.Entry(frame, textvariable=self.pwd_var, show='*', width=30)
        self.entry.grid(row=1, column=0, pady=5)
        tk.Button(frame, text="Check Password", command=self.check_password).grid(row=2, column=0, pady=10)
        self.suggested_passwords = [self.generate_strong_password() for _ in range(5)]
        tk.Button(frame, text="Show Suggested Passwords", command=self.show_suggested_passwords).grid(row=2, column=1, padx=10)
        self.result_label = tk.Label(frame, text="", fg="blue")
        self.result_label.grid(row=3, column=0, pady=5, columnspan=2)
        self.suggestion_label = tk.Label(frame, text="", fg="darkred")
        self.suggestion_label.grid(row=4, column=0, pady=5, columnspan=2)
        self.suggested_pw_frame = tk.Frame(self.root)
        self.suggested_pw_frame.pack(padx=10, pady=5)

    def generate_strong_password(self):
        # At least 1 uppercase, 1 lowercase, 1 digit, 1 special, length 12
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
        while True:
            pwd = [
                pyrandom.choice(string.ascii_uppercase),
                pyrandom.choice(string.ascii_lowercase),
                pyrandom.choice(string.digits),
                pyrandom.choice(string.punctuation)
            ]
            pwd += [pyrandom.choice(chars) for _ in range(8)]
            pyrandom.shuffle(pwd)
            pwd_str = ''.join(pwd)
            valid, _ = is_strong_password(pwd_str)
            if valid:
                return pwd_str

    def show_suggested_passwords(self):
        for widget in self.suggested_pw_frame.winfo_children():
            widget.destroy()
        tk.Label(self.suggested_pw_frame, text="Select a suggested strong password:").pack()
        for idx, pw in enumerate(self.suggested_passwords):
            btn = tk.Button(self.suggested_pw_frame, text=pw, font=("Consolas", 10), command=lambda p=pw: self.use_suggested_password(p))
            btn.pack(pady=2)

    def use_suggested_password(self, password):
        self.pwd_var.set(password)
        self.result_label.config(text="Password meets all requirements. The program will close in 15 seconds.", fg="green")
        self.suggestion_label.config(text="")
        for widget in self.suggested_pw_frame.winfo_children():
            widget.destroy()
        self.root.after(15000, self.root.destroy)

    def check_password(self):
        pwd = self.pwd_var.get()
        valid, message = is_strong_password(pwd)
        suggestions = []
        if not (8 <= len(pwd) <= 64):
            suggestions.append("• Password must be between 8 and 64 characters.")
        if not re.search(r'[A-Z]', pwd):
            suggestions.append("• Add at least one uppercase letter (A-Z).")
        if not re.search(r'\d', pwd):
            suggestions.append("• Add at least one digit (0-9).")
        if not re.search(r'[^A-Za-z0-9]', pwd):
            suggestions.append("• Add at least one special character (e.g., !, @, #, $).")
        if valid:
            self.result_label.config(text=message, fg="green")
            self.suggestion_label.config(text="")
        else:
            self.result_label.config(text="Password is not strong.", fg="red")
            self.suggestion_label.config(text="\n".join(suggestions))
            self.pwd_var.set("")  # Clear the entry field

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordAnalyzerGUI(root)
    root.mainloop()
