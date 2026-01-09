import json
import tkinter as tk
from tkinter import messagebox
from audit.audit_log import log_event

DATA_FILE = "data/users.json"
ALLOWED_ROLES = [
    "CEO",
    "CFO",
    "CISO",
    "Branch Manager",
    "HR",
    "Developer1",
    "Developer2",
    "Developer3",
    "IAM Engineer",
    "SOC Analyst",
    "GRC Analyst"
]

def load_users():
    with open(DATA_FILE) as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def open_ceo_dashboard(user):
    window = tk.Tk()
    window.title("CEO – Identity Governance Dashboard")
    window.geometry("600x400")

    tk.Label(window, text="CEO Identity Management Panel",
             font=("Arial", 14, "bold")).pack(pady=10)

    users = load_users()

    listbox = tk.Listbox(window, width=50)
    listbox.pack(pady=10)

    for u in users:
        status = "DISABLED" if not u.get("active", True) else "ACTIVE"
        listbox.insert(tk.END, f"{u['username']} | {u['role']} | {status}")

    def reset_password():
        index = listbox.curselection()
        if not index:
            messagebox.showerror("Error", "Select a user")
            return

        old_password = users[index[0]]["password"]
        users[index[0]]["password"] = "reset@123"
        save_users(users)

        log_event(
            actor="CEO",
            action="RESET_PASSWORD",
            target=users[index[0]]["username"],
            details=f"{old_password} -> reset@123"
        )

        messagebox.showinfo("Success", "Password reset to reset@123")

    role_var = tk.StringVar(window)
    role_var.set(ALLOWED_ROLES[0])

    def change_role():
        index = listbox.curselection()
        if not index:
            messagebox.showerror("Error", "Select a user")
            return

        selected_user = users[index[0]]
        old_role = selected_user["role"]
        new_role = role_var.get()

        if old_role == new_role:
            messagebox.showinfo("Info", "User already has this role")
            return

        selected_user["role"] = new_role
        save_users(users)

        log_event(
            actor="CEO",
            action="CHANGE_ROLE",
            target=selected_user["username"],
            details=f"{old_role} -> {new_role}"
        )

        listbox.delete(index)
        listbox.insert(index, f"{selected_user['username']} | {new_role}")

        messagebox.showinfo(
            "Success",
            f"Role changed from {old_role} to {new_role}"
        )

    tk.Button(
        window,
        text="Change Role",
        command=change_role
    ).pack(pady=10)

    def disable_account():
        index = listbox.curselection()
        if not index:
            messagebox.showerror("Error", "Select a user")
            return

        user = users[index[0]]

        if not user.get("active", True):
            messagebox.showinfo("Info", "Account already disabled")
            return

        user["active"] = False
        save_users(users)

        log_event(
            actor="CEO",
            action="DISABLE_ACCOUNT",
            target=user["username"],
            details="Account disabled"
        )

        listbox.delete(index)
        listbox.insert(index, f"{user['username']} | {user['role']} | DISABLED")

        messagebox.showinfo("Success", "Account disabled")

    def enable_account():
        index = listbox.curselection()
        if not index:
            messagebox.showerror("Error", "Select a user")
            return

        user = users[index[0]]

        if user.get("active", True):
            messagebox.showinfo("Info", "Account already active")
            return

        user["active"] = True
        save_users(users)

        log_event(
            actor="CEO",
            action="ENABLE_ACCOUNT",
            target=user["username"],
            details="Account enabled"
        )

        listbox.delete(index)
        listbox.insert(index, f"{user['username']} | {user['role']}")

        messagebox.showinfo("Success", "Account enabled")

    tk.Button(window, text="Disable Account", command=disable_account).pack(pady=5)
    tk.Button(window, text="Enable Account", command=enable_account).pack(pady=5)

    tk.Label(window, text="Change Role To:").pack(pady=5)

    role_menu = tk.OptionMenu(window, role_var, *ALLOWED_ROLES)
    role_menu.pack()

    tk.Button(window, text="Reset Password",
              command=reset_password).pack(pady=5)

    window.mainloop()
