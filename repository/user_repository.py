from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import errors
from control.models.models import UserResume, UserSignUp
from repository.setup_mongodb import db, collection, resume_collections

def create_user(user: UserSignUp): 
    """
    Create a new user.
    """
    try:
        user_dict = dict(user)
        collection.insert_one(user_dict)
    except errors.DuplicateKeyError as e:
        raise ValueError("User with this email already exists.")


def get_user(email: str):
    """
    Get a user by email.
    """
    try:
        return collection.find_one({"email": email})
    except Exception as e:
        raise ValueError(str(e))
    
def upload_user_resume(email:str, resume: UserResume):
    """
    Update a user's resume.
    """
    try:
        resume_dict = dict(resume)
        resume_dict["email"] = email
        resume_collections.insert_one(resume_dict)
    except Exception as e:
        raise ValueError(str(e))