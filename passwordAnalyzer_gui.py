import tkinter as tk
from tkinter import messagebox
import re
import string
import random as pyrandom

# Function to check if a password meets strength requirements
def is_strong_password(password):
    # Password length must be between 8 and 64 characters
    if not (8 <= len(password) <= 64):
        return False, "Password must be between 8 and 64 characters."
    # Password must contain at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    # Password must contain at least one digit
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number."
    # Password must contain at least one special character (non-alphanumeric)
    if not re.search(r'[^A-Za-z0-9]', password):
        return False, "Password must contain at least one special character."
    # If all checks passed, password is strong
    return True, "Password is strong."

# GUI application class for password analysis
class PasswordAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Analyzer")
        self.setup_gui()

    # Setup the GUI widgets and layout
    def setup_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        # Label prompting user to enter password
        tk.Label(frame, text="Enter your password:").grid(row=0, column=0, sticky='w')

        # Entry widget for password input, masked with '*'
        self.pwd_var = tk.StringVar()
        self.entry = tk.Entry(frame, textvariable=self.pwd_var, show='*', width=30)
        self.entry.grid(row=1, column=0, pady=5)

        # Button to check entered password strength
        tk.Button(frame, text="Check Password", command=self.check_password).grid(row=2, column=0, pady=10)

        # Generate 5 suggested strong passwords ahead of time
        self.suggested_passwords = [self.generate_strong_password() for _ in range(5)]

        # Button to show suggested strong passwords
        tk.Button(frame, text="Show Suggested Passwords", command=self.show_suggested_passwords).grid(row=2, column=1, padx=10)

        # Label to display password strength result message
        self.result_label = tk.Label(frame, text="", fg="blue")
        self.result_label.grid(row=3, column=0, pady=5, columnspan=2)

        # Label to display suggestions for improving password strength
        self.suggestion_label = tk.Label(frame, text="", fg="darkred")
        self.suggestion_label.grid(row=4, column=0, pady=5, columnspan=2)

        # Frame to hold suggested password buttons dynamically
        self.suggested_pw_frame = tk.Frame(self.root)
        self.suggested_pw_frame.pack(padx=10, pady=5)

    # Generate a strong password with required character types and length
    def generate_strong_password(self):
        # Allowed characters: uppercase, lowercase, digits, special chars
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
        while True:
            # Ensure password has at least one uppercase, one lowercase, one digit, one special char
            pwd = [
                pyrandom.choice(string.ascii_uppercase),
                pyrandom.choice(string.ascii_lowercase),
                pyrandom.choice(string.digits),
                pyrandom.choice(string.punctuation)
            ]
            # Add 8 more random characters from the full allowed set (total length 12)
            pwd += [pyrandom.choice(chars) for _ in range(8)]
            # Shuffle to randomize character order
            pyrandom.shuffle(pwd)
            pwd_str = ''.join(pwd)
            # Validate password using the is_strong_password function
            valid, _ = is_strong_password(pwd_str)
            if valid:
                return pwd_str

    # Display buttons with suggested strong passwords
    def show_suggested_passwords(self):
        # Clear any existing widgets in the suggestion frame
        for widget in self.suggested_pw_frame.winfo_children():
            widget.destroy()
        # Add label above suggested passwords
        tk.Label(self.suggested_pw_frame, text="Select a suggested strong password:").pack()
        # Create a button for each suggested password
        for idx, pw in enumerate(self.suggested_passwords):
            btn = tk.Button(self.suggested_pw_frame, text=pw, font=("Consolas", 10),
                            command=lambda p=pw: self.use_suggested_password(p))
            btn.pack(pady=2)

    # Use the selected suggested password: set entry and close app after 15 seconds
    def use_suggested_password(self, password):
        self.pwd_var.set(password)  # Insert password into entry widget
        self.result_label.config(text="Password meets all requirements. The program will close in 15 seconds.", fg="green")
        self.suggestion_label.config(text="")
        # Remove suggested password buttons after selection
        for widget in self.suggested_pw_frame.winfo_children():
            widget.destroy()
        # Close the app after 15 seconds
        self.root.after(15000, self.root.destroy)

    # Check the password entered by the user for strength and display suggestions
    def check_password(self):
        pwd = self.pwd_var.get()
        valid, message = is_strong_password(pwd)
        suggestions = []

        # Collect suggestions if criteria are not met
        if not (8 <= len(pwd) <= 64):
            suggestions.append("• Password must be between 8 and 64 characters.")
        if not re.search(r'[A-Z]', pwd):
            suggestions.append("• Add at least one uppercase letter (A-Z).")
        if not re.search(r'\d', pwd):
            suggestions.append("• Add at least one digit (0-9).")
        if not re.search(r'[^A-Za-z0-9]', pwd):
            suggestions.append("• Add at least one special character (e.g., !, @, #, $).")

        # If valid, display success message; else show suggestions and clear entry
        if valid:
            self.result_label.config(text=message, fg="green")
            self.suggestion_label.config(text="")
        else:
            self.result_label.config(text="Password is not strong.", fg="red")
            self.suggestion_label.config(text="\n".join(suggestions))
            self.pwd_var.set("")  # Clear the entry field

# Run the GUI application if this script is executed directly
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordAnalyzerGUI(root)
    root.mainloop()
