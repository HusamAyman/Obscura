from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.user_router import router as user_router


app = FastAPI(
    title="Obscura REST API",
    version="1.0.0",
    description="A REST API for Obscura"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)