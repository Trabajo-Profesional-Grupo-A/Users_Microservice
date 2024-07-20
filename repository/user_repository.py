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
    
def get_resume_by_email(email: str):
    """
    Get a user's resume by email.
    """
    try:
        return resume_collections.find_one({"email": email})
    except Exception as e:
        raise ValueError(str(e))
    
def update_user_info(email: str, user_info: dict):
    """
    Update a user's info.
    """
    try:
        collection.update_one({"email": email}, {"$set": user_info})
    except Exception as e:
        raise ValueError(str(e))
    
def search_users_by_name(first_name: str, limit: int = 5):
    """
    Search for users by their first_name. 
    First look for users whose first_name starts with the given prefix,
    then look for users whose first_name contains the given prefix if needed.
    """
    try:
        users = list(collection.find({"first_name": {"$regex": f"^{first_name}", "$options": "i"}}).limit(limit))

        if len(users) < limit:
            additional_limit = limit - len(users)

            additional_users = list(collection.find(
                {"first_name": {"$regex": first_name, "$options": "i"}}
            ).limit(additional_limit))
            
            additional_users = [user for user in additional_users if user not in users]
            
            users.extend(additional_users)
        
        return users
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")

