import json
import tkinter as tk
from governance.sod_engine import detect_sod_violations
from datetime import datetime
from governance.entitlements import HIGH_RISK_ENTITLEMENTS

DATA_FILE = "data/users.json"

# Simple access review rules
HIGH_PRIV_ROLES = ["CEO", "CFO", "CISO"]
DEV_ROLES = ["Developer1", "Developer2", "Developer3"]

def load_users():
    with open(DATA_FILE) as f:
        return json.load(f)

def open_ciso_dashboard(user):
    window = tk.Tk()
    window.title("CISO – Access Review Dashboard")
    window.geometry("700x450")

    tk.Label(
        window,
        text="CISO – Identity Access Review (Read-Only)",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    users = load_users()

    listbox = tk.Listbox(window, width=90)
    listbox.pack(pady=10)

    for u in users:
        status = "DISABLED" if not u.get("active", True) else "ACTIVE"
        listbox.insert(
            tk.END,
            f"{u['username']} | {u['role']} | {status}"
        )

    review_output = tk.Text(window, height=8)
    review_output.pack(pady=10)

    def run_access_review():

        review_output.delete("1.0", tk.END)
        now = datetime.now()
        findings = False

        for u in users:
            print("Reviewing user:", u["username"])
            if not u.get("active", True):
                continue

            username = u.get("username")
            role = u.get("role")

            # 1️⃣ High-risk entitlements
            for ent in u.get("entitlements", []):
                if ent in HIGH_RISK_ENTITLEMENTS:
                    review_output.insert(
                        tk.END,
                        f"[ENTITLEMENT RISK]\n"
                        f"User: {username}\n"
                        f"Role: {role}\n"
                        f"Entitlement: {ent}\n"
                        f"Risk: HIGH\n\n"
                    )
                    findings = True

            # 2️⃣ Expired JIT access
            for jit in u.get("jit_entitlements", []):
                expiry = datetime.fromisoformat(jit["expires_at"])
                if now > expiry:
                    formatted_time = expiry.strftime("%d %b %Y, %I:%M %p")
                    review_output.insert(
                        tk.END,
                        f"[JIT ACCESS EXPIRED]\n"
                        f"User: {username}\n"
                        f"Role: {role}\n"
                        f"Entitlement: {jit['entitlement']}\n"
                        f"Expired At: {formatted_time}\n\n"
                    )
                    findings = True

            # 3️⃣ Existing role-based risk checks
            if role in HIGH_PRIV_ROLES and "dev" in username.lower():
                review_output.insert(
                    tk.END,
                    f"[ROLE VIOLATION]\n"
                    f"User: {username}\n"
                    f"Role: {role}\n"
                    f"Risk: Developer assigned high-privilege role\n\n"
                )
                findings = True

        if not findings:
            review_output.insert(
                tk.END,
                "No entitlement, JIT, role, or SoD violations detected.\n"
            )

    def run_sod_review():
        review_output.delete("1.0", tk.END)

        violations = detect_sod_violations(users)

        if not violations:
            review_output.insert(tk.END, "No SoD violations detected.\n")
            return

        for v in violations:
            review_output.insert(
                tk.END,
                f"[SoD VIOLATION] User: {v['username']} | "
                f"Role: {v['role']} | "
                f"Conflict Policy: {v['conflict']} | "
                f"Risk: {v['risk']}\n"
            )

    tk.Button(
        window,
        text="Run SoD Violation Review",
        command=run_sod_review
    ).pack(pady=5)

    tk.Button(
        window,
        text="Run Access Review",
        command=run_access_review
    ).pack(pady=5)

    window.mainloop()
