import tkinter as tk
from tkinter import messagebox
from auth.login import authenticate
from gui.ceo_dashboard import open_ceo_dashboard
from gui.ciso_dashboard import open_ciso_dashboard
from datetime import datetime

def login():
    username = username_entry.get()
    password = password_entry.get()
    otp = otp_entry.get()

    result = authenticate(username, password, otp)

    # Case 1: Account locked
    if isinstance(result, dict) and result.get("locked"):
        lock_until_raw = result["lock_until"]
        lock_until_dt = datetime.fromisoformat(lock_until_raw)
        formatted_time = lock_until_dt.strftime("%d %b %Y, %I:%M %p")
        messagebox.showerror(
            "Account Locked",
            f"Your account is locked until:\n{formatted_time}"

        )
        return

    # Case 2: Login failed (wrong creds / OTP)
    if not result or result.get("locked") is False and "role" not in result:
        messagebox.showerror(
            "Login Failed",
            "Invalid credentials or OTP"
        )
        return

    # Case 3: Login success
    user = result
    role = user.get("role")

    if role == "CEO":
        root.destroy()
        open_ceo_dashboard(user)

    elif role == "CISO":
        root.destroy()
        open_ciso_dashboard(user)

    else:
        messagebox.showinfo(
            "Login Success",
            f"Logged in as {role}. No admin dashboard assigned."
        )


root = tk.Tk()
root.title("IAM Secure Login")
root.geometry("300x250")

tk.Label(root, text="Username").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Label(root, text="OTP").pack()
otp_entry = tk.Entry(root)
otp_entry.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()
