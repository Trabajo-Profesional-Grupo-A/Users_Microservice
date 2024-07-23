# models.py
"""
This module is dedicated for all the pydantic models the API will use.
"""
from typing import List, Optional
from pydantic import BaseModel


class UserSignUp(BaseModel):
    """
    User sign up model.
    """
    email: str
    password: str
    first_name: str
    last_name: str
    title: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None
    address: str
    age: int

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
    title: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None
    address: str
    age: int
    
class UserResume(BaseModel):
    """
    User resume model.
    """
    education: str
    experience: str
    job_titles: List[str]
    skills: List[str]
    model_data: str
    address: str
    age: int