# models.py
"""
This module is dedicated for all the pydantic models the API will use.
"""
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