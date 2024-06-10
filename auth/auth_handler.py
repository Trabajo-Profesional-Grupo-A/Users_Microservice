import jwt
import bcrypt 

SECRET_KEY = "my_secret_key"

def generate_token(email: str) -> str:
    """
    Generate a JWT token for a user with the specified email.
    """
    if not SECRET_KEY:
        raise ValueError("JWT secret key is not configured")
    
    # Payload containing user email
    payload = {"email": email}

    # Generate token with specified payload and secret key
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> str:
    """
    Decode a JWT token, returns the email of the user.
    """
    if not SECRET_KEY:
        raise ValueError("JWT secret key is not configured")
    
    # Decode token with secret key
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

def hash_password(password: str) -> str:
    """
    Hash a password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(password: str, hashed_password: str) -> bool:
    """
    Check if a password is correct.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))