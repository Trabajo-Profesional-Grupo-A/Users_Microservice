"""
This module contains the API endpoints for the users service.
"""

from typing import List
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

from control.models.models import UploadResumeRequest, UserResume, UserSignUp, UserSignIn, UserResponse
from auth.auth_handler import hash_password, check_password, generate_token, decode_token
from typing import List

router = APIRouter(
    tags=["users"],
    prefix="/users",
)

origins = ["*"]

from repository.user_repository import create_user, get_resume_by_email, get_user, search_users_by_name, upload_user_resume, get_users_by_emails

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
def upload_resume(token: str, resume: UploadResumeRequest):
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
    
@router.get("/search", response_model=List[UserResponse])
def search_users(name: str, offset: int = 0, amount: int = 5):
    """
    Search for users by their first_name.
    """
    try:
        users = search_users_by_name(name, offset, amount)
        if not users:
            raise HTTPException(status_code=USER_NOT_FOUND, detail="No users found.")
        return [UserResponse.parse_obj(user) for user in users]
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))
    
@router.post("/by_emails", response_model=List[UserResponse])
def get_users_by_emails_api(emails: List[str]):
    """
    Get a list of users by their emails.
    """
    try:
        
        users = get_users_by_emails(emails)
        if not users:
            raise HTTPException(status_code=404, detail="No users found for the provided emails.")
        return [UserResponse.parse_obj(user) for user in users]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

