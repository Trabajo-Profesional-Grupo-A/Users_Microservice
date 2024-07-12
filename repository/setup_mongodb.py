import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import errors
from dotenv import load_dotenv
import certifi

load_dotenv()
db_url = os.getenv("DB_URI")

client = MongoClient(db_url, server_api=ServerApi('1'), tlsCAFile=certifi.where())

db = client['users']
collection = db['users']
collection.create_index([('email', 1)], unique=True)

resume_collections = db['resumes']
resume_collections.create_index([('email', 1)], unique=True)
