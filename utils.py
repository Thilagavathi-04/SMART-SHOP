import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_secure_password():
    return input("Password: ") 
