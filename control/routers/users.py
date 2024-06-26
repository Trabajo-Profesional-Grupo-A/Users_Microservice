"""
This module contains the API endpoints for the users service.
"""
import firebase_admin
import os

from fastapi import (
    APIRouter,
    HTTPException,
)

from control.codes import (
    USER_NOT_FOUND,
    INCORRECT_CREDENTIALS,
    BAD_REQUEST,
    CONFLICT,
)
from firebase_admin import credentials, storage

cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred, {"storageBucket": "tpp-grupoa.appspot.com"})

from control.models.models import UserSignUp, UserSignIn, UserResponse
from auth.auth_handler import hash_password, check_password, generate_token, decode_token

router = APIRouter(
    tags=["users"],
    prefix="/users",
)
origins = ["*"]

from repository.user_repository import create_user, get_user

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

# prueba, esto se hace desde el front
@router.post("/upload-image")
def upload_image():
    """
    Upload an image.
    """
    try:
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "../../image.png")
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"No such file or directory: '{image_path}'")
        
        bucket = storage.bucket() 
        blob = bucket.blob("image.png")
        blob.upload_from_filename(image_path)
        return {"message": "Image uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))

# prueba, esto se hace desde el front
# desde el front se sube el pdf a firebase storage
# este endpoint va a hacer el procesamiento del lenguaje natural
# para extraer la información del cv y va a retornar un json con 
# los campos del autocompletado
@router.post("/resume")
def upload_image(token: str):
    """
    Upload an image.
    """
    try:
        email = decode_token(token)["email"]
        user = get_user(email)
        # script_dir = os.path.dirname(__file__)

        # documento_path = os.path.join(script_dir, "../../Akshay_Srimatrix.pdf")
        bucket = storage.bucket()
        local_file_path = f"resumes/cv_{email}.pdf"
        # blob = bucket.blob(local_file_path)
        # blob.upload_from_filename(documento_path)

        temp_local_filename = "./temp.pdf"
        blob = bucket.blob(local_file_path)
        blob.download_to_filename(temp_local_filename)

        # con el read PDF2 funciona
        # with open(temp_local_filename, 'rb') as file:
        #     content = file.read()
        #     print(f'Contenido del archivo {local_file_path}:')
        #     print(content)

        return {"message": "Document uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))
    