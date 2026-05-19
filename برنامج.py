import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime
class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("500x500")
        self.root.configure(bg="#2c3e50")
        
        # Initialize saved passwords
        self.saved_passwords = []
        self.load_passwords()
        
        # Title
        title_label = tk.Label(root, text="Password Generator", font=("Arial", 20, "bold"), 
                              bg="#2c3e50", fg="#3498db")
        title_label.pack(pady=20)
        
        # Configuration frame
        config_frame = tk.Frame(root, bg="#34495e", padx=10, pady=10)
        config_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(config_frame, text="Password Configuration", font=("Arial", 12, "bold"), 
                bg="#34495e", fg="#3498db").pack(anchor="w", pady=(0, 10))
        
        # Total length
        length_frame = tk.Frame(config_frame, bg="#34495e")
        length_frame.pack(fill="x", pady=5)
        tk.Label(length_frame, text="Total Length:", bg="#34495e", fg="white").pack(side="left")
        self.total_var = tk.IntVar(value=12)
        total_spin = ttk.Spinbox(length_frame, from_=4, to=50, textvariable=self.total_var, width=10)
        total_spin.pack(side="left", padx=10)
        total_spin.bind("<KeyRelease>", self.update_character_types)
        
        # Character types
        self.letters_var = tk.BooleanVar(value=True)
        letters_check = ttk.Checkbutton(config_frame, text="Include Letters", 
                                       variable=self.letters_var, command=self.update_character_types)
        letters_check.pack(anchor="w", pady=2)
        
        self.numbers_var = tk.BooleanVar(value=True)
        numbers_check = ttk.Checkbutton(config_frame, text="Include Numbers", 
                                       variable=self.numbers_var, command=self.update_character_types)
        numbers_check.pack(anchor="w", pady=2)
        
        self.symbols_var = tk.BooleanVar(value=True)
        symbols_check = ttk.Checkbutton(config_frame, text="Include Symbols", 
                                       variable=self.symbols_var, command=self.update_character_types)
        symbols_check.pack(anchor="w", pady=2)
        
        # Character counts frame
        self.counts_frame = tk.Frame(root, bg="#34495e", padx=10, pady=10)
        self.counts_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(self.counts_frame, text="Character Counts", font=("Arial", 12, "bold"), 
                bg="#34495e", fg="#3498db").pack(anchor="w", pady=(0, 10))
        
        # Letters count
        letters_count_frame = tk.Frame(self.counts_frame, bg="#34495e")
        letters_count_frame.pack(fill="x", pady=5)
        tk.Label(letters_count_frame, text="Letters:", bg="#34495e", fg="white").pack(side="left")
        self.letters_count_var = tk.IntVar(value=6)
        self.letters_spin = ttk.Spinbox(letters_count_frame, from_=0, to=50, 
                                       textvariable=self.letters_count_var, width=10, state="normal")
        self.letters_spin.pack(side="left", padx=10)
        
        # Numbers count
        numbers_count_frame = tk.Frame(self.counts_frame, bg="#34495e")
        numbers_count_frame.pack(fill="x", pady=5)
        tk.Label(numbers_count_frame, text="Numbers:", bg="#34495e", fg="white").pack(side="left")
        self.numbers_count_var = tk.IntVar(value=3)
        self.numbers_spin = ttk.Spinbox(numbers_count_frame, from_=0, to=50, 
                                       textvariable=self.numbers_count_var, width=10, state="normal")
        self.numbers_spin.pack(side="left", padx=10)
        
        # Symbols count
        symbols_count_frame = tk.Frame(self.counts_frame, bg="#34495e")
        symbols_count_frame.pack(fill="x", pady=5)
        tk.Label(symbols_count_frame, text="Symbols:", bg="#34495e", fg="white").pack(side="left")
        self.symbols_count_var = tk.IntVar(value=3)
        self.symbols_spin = ttk.Spinbox(symbols_count_frame, from_=0, to=50, 
                                       textvariable=self.symbols_count_var, width=10, state="normal")
        self.symbols_spin.pack(side="left", padx=10)
        
        # Password display frame
        password_frame = tk.Frame(root, bg="#2c3e50")
        password_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(password_frame, text="Generated Password:", bg="#2c3e50", fg="white").pack(anchor="w")
        
        password_display_frame = tk.Frame(password_frame, bg="#2c3e50")
        password_display_frame.pack(fill="x", pady=5)
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(password_display_frame, textvariable=self.password_var, 
                                  font=("Arial", 12), state="readonly")
        password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        copy_btn = ttk.Button(password_display_frame, text="Copy", command=self.copy_to_clipboard)
        copy_btn.pack(side="right")
        
        # Buttons frame
        buttons_frame = tk.Frame(root, bg="#2c3e50")
        buttons_frame.pack(pady=10)
        
        generate_btn = ttk.Button(buttons_frame, text="Generate Password", command=self.generate_password)
        generate_btn.pack(side="left", padx=5)
        
        save_btn = ttk.Button(buttons_frame, text="Save Password", command=self.save_password)
        save_btn.pack(side="left", padx=5)
        
        # Saved passwords frame
        saved_frame = tk.Frame(root, bg="#34495e", padx=10, pady=10)
        saved_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(saved_frame, text="Saved Passwords", font=("Arial", 12, "bold"), 
                bg="#34495e", fg="#3498db").pack(anchor="w", pady=(0, 10))
        
        # Create treeview for saved passwords
        columns = ("Website", "Username", "Password", "Date")
        self.passwords_tree = ttk.Treeview(saved_frame, columns=columns, show="headings", height=6)
        
        # Define headings
        self.passwords_tree.heading("Website", text="Website/Service")
        self.passwords_tree.heading("Username", text="Username")
        self.passwords_tree.heading("Password", text="Password")
        self.passwords_tree.heading("Date", text="Created Date")
        
        # Define columns
        self.passwords_tree.column("Website", width=120)
        self.passwords_tree.column("Username", width=100)
        self.passwords_tree.column("Password", width=120)
        self.passwords_tree.column("Date", width=100)
        
        self.passwords_tree.pack(fill="both", expand=True)
        
        # Buttons for saved passwords
        saved_buttons_frame = tk.Frame(saved_frame, bg="#34495e")
        saved_buttons_frame.pack(pady=5)
        
        ttk.Button(saved_buttons_frame, text="Copy Selected", 
                  command=self.copy_selected_password).pack(side="left", padx=5)
        ttk.Button(saved_buttons_frame, text="Delete Selected", 
                  command=self.delete_selected_password).pack(side="left", padx=5)
        ttk.Button(saved_buttons_frame, text="Refresh List", 
                  command=self.refresh_passwords_list).pack(side="left", padx=5)
        
        # Bind double-click event
        self.passwords_tree.bind("<Double-1>", self.on_password_double_click)
        
        # Set initial state
        self.update_character_types()
        self.refresh_passwords_list()    
    def load_passwords(self):
        """Load saved passwords from JSON file"""
        try:
            if os.path.exists("saved_passwords.json"):
                with open("saved_passwords.json", "r") as f:
                    self.saved_passwords = json.load(f)
            else:
                self.saved_passwords = []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load saved passwords: {str(e)}")
            self.saved_passwords = []    
    def save_passwords_to_file(self):
        """Save passwords to JSON file"""
        try:
            with open("saved_passwords.json", "w") as f:
                json.dump(self.saved_passwords, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save passwords: {str(e)}")   
    def refresh_passwords_list(self):
        """Refresh the treeview with current saved passwords"""
        # Clear existing items
        for item in self.passwords_tree.get_children():
            self.passwords_tree.delete(item)
        
        # Add passwords to treeview
        for pw in self.saved_passwords:
            self.passwords_tree.insert("", "end", values=(
                pw.get("website", ""),
                pw.get("username", ""),
                "•" * 12,  # Show dots instead of actual password
                pw.get("date", "")
            ))    
    def save_password(self):
        """Save the current password with website and username information"""
        password = self.password_var.get()
        if not password:
            messagebox.showwarning("Warning", "No password to save! Generate a password first.")
            return
        
        # Create dialog for website and username
        dialog = tk.Toplevel(self.root)
        dialog.title("Save Password")
        dialog.geometry("300x150")
        dialog.configure(bg="#2c3e50")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Website/Service:", bg="#2c3e50", fg="white").pack(pady=(10, 0))
        website_entry = ttk.Entry(dialog, width=30)
        website_entry.pack(pady=5)
        website_entry.focus()
        
        tk.Label(dialog, text="Username (optional):", bg="#2c3e50", fg="white").pack(pady=(5, 0))
        username_entry = ttk.Entry(dialog, width=30)
        username_entry.pack(pady=5)
        
        def save_and_close():
            website = website_entry.get().strip()
            if not website:
                messagebox.showwarning("Warning", "Please enter a website/service name.")
                return
            
            username = username_entry.get().strip()
            
            # Save password info
            password_info = {
                "website": website,
                "username": username,
                "password": password,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "config": {
                    "total_length": self.total_var.get(),
                    "letters": self.letters_var.get(),
                    "numbers": self.numbers_var.get(),
                    "symbols": self.symbols_var.get(),
                    "letters_count": self.letters_count_var.get(),
                    "numbers_count": self.numbers_count_var.get(),
                    "symbols_count": self.symbols_count_var.get()
                }
            }
            
            self.saved_passwords.append(password_info)
            self.save_passwords_to_file()
            self.refresh_passwords_list()
            
            messagebox.showinfo("Success", f"Password for {website} saved successfully!")
            dialog.destroy()
        
        buttons_frame = tk.Frame(dialog, bg="#2c3e50")
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Save", command=save_and_close).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=5)    
    def copy_selected_password(self):
        """Copy the selected password to clipboard"""
        selection = self.passwords_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password to copy.")
            return
        
        item = selection[0]
        index = self.passwords_tree.index(item)
        
        if 0 <= index < len(self.saved_passwords):
            password = self.saved_passwords[index]["password"]
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Copied", "Password has been copied to clipboard!")    
    def delete_selected_password(self):
        """Delete the selected password"""
        selection = self.passwords_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password to delete.")
            return
        
        item = selection[0]
        index = self.passwords_tree.index(item)
        website = self.saved_passwords[index]["website"]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the password for {website}?"):
            self.saved_passwords.pop(index)
            self.save_passwords_to_file()
            self.refresh_passwords_list()
            messagebox.showinfo("Success", "Password deleted successfully!")
    def on_password_double_click(self, event):
        """Handle double-click on password item"""
        item = self.passwords_tree.identify('item', event.x, event.y)
        if item:
            self.copy_selected_password()    
    def update_character_types(self, event=None):
        total = self.total_var.get()
        
        # Enable/disable spin boxes based on checkboxes
        state_letters = "normal" if self.letters_var.get() else "disabled"
        state_numbers = "normal" if self.numbers_var.get() else "disabled"
        state_symbols = "normal" if self.symbols_var.get() else "disabled"
        
        self.letters_spin.config(state=state_letters)
        self.numbers_spin.config(state=state_numbers)
        self.symbols_spin.config(state=state_symbols)
        
        # Calculate how many character types are selected
        enabled_types = sum([
            self.letters_var.get(),
            self.numbers_var.get(),
            self.symbols_var.get()
        ])
        
        if enabled_types == 0:
            messagebox.showwarning("Warning", "At least one character type must be selected!")
            self.letters_var.set(True)
            return
        
        # Distribute total among enabled types
        if enabled_types == 3:
            # Default distribution
            letters = max(1, total // 2)
            numbers = max(1, (total - letters) // 2)
            symbols = max(0, total - letters - numbers)
            
            self.letters_count_var.set(letters)
            self.numbers_count_var.set(numbers)
            self.symbols_count_var.set(symbols)
        elif enabled_types == 2:
            # Distribute between the two enabled types
            first_half = total // 2
            second_half = total - first_half
            
            if self.letters_var.get() and self.numbers_var.get():
                self.letters_count_var.set(first_half)
                self.numbers_count_var.set(second_half)
                self.symbols_count_var.set(0)
            elif self.letters_var.get() and self.symbols_var.get():
                self.letters_count_var.set(first_half)
                self.symbols_count_var.set(second_half)
                self.numbers_count_var.set(0)
            else:  # numbers and symbols
                self.numbers_count_var.set(first_half)
                self.symbols_count_var.set(second_half)
                self.letters_count_var.set(0)
        else:  # Only one type selected
            if self.letters_var.get():
                self.letters_count_var.set(total)
                self.numbers_count_var.set(0)
                self.symbols_count_var.set(0)
            elif self.numbers_var.get():
                self.numbers_count_var.set(total)
                self.letters_count_var.set(0)
                self.symbols_count_var.set(0)
            else:  # symbols
                self.symbols_count_var.set(total)
                self.letters_count_var.set(0)
                self.numbers_count_var.set(0)    
    def validate_inputs(self):
        total = self.total_var.get()
        letters = self.letters_count_var.get() if self.letters_var.get() else 0
        numbers = self.numbers_count_var.get() if self.numbers_var.get() else 0
        symbols = self.symbols_count_var.get() if self.symbols_var.get() else 0        
        if letters + numbers + symbols != total:
            messagebox.showerror("Input Error", 
                               f"The sum of characters ({letters + numbers + symbols}) "
                               f"does not match the total length ({total}).")
            return False        
        if total < 4:
            messagebox.showerror("Input Error", "Password length should be at least 4 characters.")
            return False            
        return True    
    def generate_password(self):
        if not self.validate_inputs():
            return            
        letters_count = self.letters_count_var.get() if self.letters_var.get() else 0
        numbers_count = self.numbers_count_var.get() if self.numbers_var.get() else 0
        symbols_count = self.symbols_count_var.get() if self.symbols_var.get() else 0        
        # Define character sets
        letters = string.ascii_letters
        numbers = string.digits
        symbols = string.punctuation        
        # Generate password components
        password_chars = []        
        if letters_count > 0:
            password_chars.extend(random.choices(letters, k=letters_count))
        if numbers_count > 0:
            password_chars.extend(random.choices(numbers, k=numbers_count))
        if symbols_count > 0:
            password_chars.extend(random.choices(symbols, k=symbols_count))        
        # Shuffle to mix characters
        random.shuffle(password_chars)        
        # Create the final password
        password = "".join(password_chars)
        self.password_var.set(password)    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Copied", "Password has been copied to clipboard!")
        else:
            messagebox.showerror("Copy Error", "No password to copy!")
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

















































