from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import errors
from control.models.models import UserSignUp
DB_URI = "mongodb+srv://nencinoza:4VxMOntx1i2W8uQm@users.6jjtd5n.mongodb.net/?retryWrites=true&w=majority&appName=users"

client = MongoClient(DB_URI, server_api=ServerApi('1'))

db = client.users
collection = db.users
collection.create_index([('email', 1)], unique=True)


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