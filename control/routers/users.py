"""
This module contains the API endpoints for the users service.
"""

from fastapi import (
    APIRouter,
    HTTPException,
)

from control.codes import (
    USER_NOT_FOUND,
    INCORRECT_CREDENTIALS,
    BAD_REQUEST,
    CONFLICT,
)

from control.models.models import UserSignUp, UserSignIn, UserResponse
from auth.auth_handler import hash_password, check_password, generate_token, decode_token

router = APIRouter(
    tags=["users"],
    prefix="/users",
)
origins = ["*"]

from repository.user_repository import create_user, get_user

@router.post("/sign-up")
def sign_up(user: UserSignUp):
    """
    Sign up a new user.
    """
    try: 
        user.password = hash_password(user.password)
        create_user(user)
        token = generate_token(user.email)
        return {"message": "User created successfully.", "token": token}
    except ValueError as e:
        raise HTTPException(status_code=CONFLICT, detail=str(e))

@router.post("/sign-in")
def sign_in(user: UserSignIn):
    """
    Sign in a user.
    """
    try:
        stored_user = get_user(user.email)
        if not stored_user:
            raise HTTPException(status_code=USER_NOT_FOUND, detail="User not found.")
        if check_password(user.password, stored_user["password"]):
            token = generate_token(user.email)
            return {"message": "User signed in successfully.", "token": token}
        else: 
            raise HTTPException(status_code=INCORRECT_CREDENTIALS, detail="Incorrect email or password.")
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))

@router.get("/get-user", response_model=UserResponse)
def get_user_by_token(token: str):
    """
    Get a user by token.
    """
    try:
        email = decode_token(token)["email"]
        user = get_user(email)
        if not user:
            raise HTTPException(status_code=USER_NOT_FOUND, detail="User not found.")
        return UserSignUp.parse_obj(user)

    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))