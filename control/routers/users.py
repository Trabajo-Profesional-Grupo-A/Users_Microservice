"""
This module contains the API endpoints for the users service.
"""

from fastapi import (
    APIRouter,
    HTTPException,
)
import requests

from control.codes import (
    USER_NOT_FOUND,
    INCORRECT_CREDENTIALS,
    BAD_REQUEST,
    CONFLICT,
)

API_MATCHING_URL = "http://34.42.161.58:8000"

from control.models.models import UserResume, UserSignUp, UserSignIn, UserResponse
from auth.auth_handler import hash_password, check_password, generate_token, decode_token

router = APIRouter(
    tags=["users"],
    prefix="/users",
)

origins = ["*"]

from repository.user_repository import create_user, get_resume_by_email, get_user, upload_user_resume, update_user_info

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

@router.get("/user", response_model=UserResponse)
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
    
@router.get("/user/email", response_model=UserResponse)
def get_user_by_email(email: str):
    """
    Get a user by email.
    """
    try:
        user = get_user(email)
        if not user:
            raise HTTPException(status_code=USER_NOT_FOUND, detail="User not found.")
        return UserSignUp.parse_obj(user)

    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))

@router.post("/user/upload_resume")
def upload_resume(token: str, resume: UserResume):
    """
    Upload a resume for a user.
    """
    try:
        email = decode_token(token)["email"]
        user = get_user(email)
        if not user:
            raise HTTPException(status_code=USER_NOT_FOUND, detail="User not found.")
        
        upload_user_resume(email, resume)

        url = API_MATCHING_URL + f"/matching/candidate/{email}/"
        data = {"model_data": resume.model_data}
        print(url)
        print(data)

        response = requests.post(
            url,
            json=data
        )
        print(response.status_code)
        print(response.json())

        if response.status_code != 200:
            raise HTTPException(status_code=BAD_REQUEST, detail="Error uploading resume to model.")

        return {"message": "Resume uploaded successfully."}

    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))

@router.get("/user/resume/{email}", response_model=UserResume)
def get_resume(email: str):
    """
    Get a user's resume by token.
    """
    try:
        resume = get_resume_by_email(email)
        return UserResume.parse_obj(resume)

    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))
    

