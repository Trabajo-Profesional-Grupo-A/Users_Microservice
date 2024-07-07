import jwt
import bcrypt 

SECRET_KEY = "my_secret_key"

def generate_token(email: str, user_type: str) -> str:
    """
    Generate a JWT token for a user with the specified email and user type.
    """
    if not SECRET_KEY:
        raise ValueError("JWT secret key is not configured")
    
    # Payload containing user email and user type
    payload = {"email": email, "user_type": user_type}

    # Generate token with specified payload and secret key
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> dict:
    """
    Decode a JWT token, returns the decoded payload.
    """
    if not SECRET_KEY:
        raise ValueError("JWT secret key is not configured")
    
    # Decode token and return payload
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
