import json
from datetime import datetime, timedelta
from auth.mfa import verify_otp
from audit.audit_log import log_event

LOCK_THRESHOLD = 3
LOCK_DURATION_MINUTES = 5

def authenticate(username, password, otp):
    with open("data/users.json") as f:
        users = json.load(f)

    now = datetime.now()

    for user in users:
        if user["username"] != username:
            continue

        # Account disabled
        if not user.get("active", True):
            return None

        # Account locked
        if user.get("lock_until"):
            lock_until = datetime.fromisoformat(user["lock_until"])
            if now < lock_until:
                return {
                    "locked": True,
                    "lock_until": lock_until.isoformat()
                }

            else:
                # Lock expired
                user["lock_until"] = None
                user["failed_mfa_attempts"] = 0

        # Password check
        if user["password"] != password:
            return None

        # MFA check
        if not verify_otp(user["mfa_secret"], otp):
            user["failed_mfa_attempts"] += 1

            log_event(
                actor=username,
                action="MFA_FAILED",
                target=username,
                details=f"Failed MFA attempt {user['failed_mfa_attempts']}"
            )

            if user["failed_mfa_attempts"] >= LOCK_THRESHOLD:
                user["lock_until"] = (
                    now + timedelta(minutes=LOCK_DURATION_MINUTES)
                ).isoformat()

                log_event(
                    actor=username,
                    action="ACCOUNT_LOCKED",
                    target=username,
                    details="Too many failed MFA attempts"
                )

            with open("data/users.json", "w") as f:
                json.dump(users, f, indent=2)

            return None

        # MFA success → reset counters
        user["failed_mfa_attempts"] = 0
        user["lock_until"] = None

        with open("data/users.json", "w") as f:
            json.dump(users, f, indent=2)

        log_event(
            actor=username,
            action="LOGIN_SUCCESS",
            target=username,
            details="Successful login with MFA"
        )

        return user

    return {"locked": False}

