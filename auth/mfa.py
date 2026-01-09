import pyotp

def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)
