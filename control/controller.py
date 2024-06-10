from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from control.routers import users
from annoy import AnnoyIndex
from scipy.spatial.distance import cosine

app = FastAPI(
    title="Users API", description="This is the API for the users service."
)

origins = ["*"]
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
