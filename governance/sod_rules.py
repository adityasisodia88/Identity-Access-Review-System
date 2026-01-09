# Separation of Duties (SoD) conflict definitions

SOD_ROLE_CONFLICTS = [
    ("HR", "Finance Analyst"),
    ("HR", "Accounts Manager"),
    ("Developer1", "IAM Engineer"),
    ("Developer2", "IAM Engineer"),
    ("Developer3", "IAM Engineer"),
    ("CFO", "GRC Analyst"),
]

# Optional: permission-based conflicts (future-ready)
SOD_PERMISSION_CONFLICTS = [
    ("payroll_modify", "audit_read"),
    ("iam_admin", "repo_write"),
]
