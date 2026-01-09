from governance.sod_rules import SOD_ROLE_CONFLICTS

def detect_sod_violations(users):
    violations = []

    for user in users:
        role = user.get("role")

        for conflict in SOD_ROLE_CONFLICTS:
            if role in conflict:
                # Check if user has another conflicting role historically
                # (For now, single-role system → simulate risk)
                violations.append({
                    "username": user["username"],
                    "role": role,
                    "conflict": conflict,
                    "risk": "HIGH"
                })

    return violations
