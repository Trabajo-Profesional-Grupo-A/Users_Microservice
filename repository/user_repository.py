from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import errors
from control.models.models import UserResume, UserSignUp
from repository.setup_mongodb import db, collection, resume_collections
from typing import List

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
    Update a user's resume, or create a new resume if it doesn't exist.
    """
    try:
        resume_dict = dict(resume)
        resume_dict["email"] = email
        resume_collections.update_one(
            {"email": email},
            {"$set": resume_dict}, 
            upsert=True  
        )
    except Exception as e:
        raise ValueError(str(e))
    
def get_resume_by_email(email: str):
    """
    Get a user's resume by email.
    """
    try:
        resume = resume_collections.find_one({"email": email})
        user_data = collection.find_one({"email": email})

        resume["address"]= user_data["address"]
        resume["age"] = user_data["age"]

        return resume
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
    
def search_users_by_name(first_name: str, offset: int = 0, amount: int = 5):
    """
    Search for users by their first_name. 
    First look for users whose first_name starts with the given prefix,
    then look for users whose first_name contains the given prefix if needed.
    """
    try:
        users_starting_with = list(
            collection.find({"first_name": {"$regex": f"^{first_name}", "$options": "i"}})
                      .skip(offset)
                      .limit(amount)
        )
        
        additional_amount = amount - len(users_starting_with)

        if additional_amount > 0:
            additional_users = list(
                collection.find({"first_name": {"$regex": f".*{first_name}.*", "$options": "i"}})
                          .skip(offset)
                          .limit(additional_amount)
            )
            
            additional_users = [user for user in additional_users if user not in users_starting_with]
            
            users_starting_with.extend(additional_users)

        return users_starting_with
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")
    
def get_users_by_emails(emails: List[str]):
    """
    Get users by a list of emails.
    """
    try:
        users = []
        for email in emails:
            user = collection.find_one({"email": email})
            if user:
                users.append(user)
        return users
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")



