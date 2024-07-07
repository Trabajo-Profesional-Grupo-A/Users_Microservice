# models.py
"""
This module is dedicated for all the pydantic models the API will use.
"""
from typing import List
from pydantic import BaseModel


class UserSignUp(BaseModel):
    """
    User sign up model.
    """
    email: str
    password: str
    first_name: str
    last_name: str

class UserSignIn(BaseModel):
    """
    User sign in model.
    """
    email: str
    password: str

class UserResponse(BaseModel):
    """
    User response model.
    """
    email: str
    first_name: str
    last_name: str
    user_type: str = "candidate"

class ResumeFields(BaseModel):
    education: str
    experience: str
    job_titles: List[str]
    phone: str
    skills: List[str]
    clean_data: str
