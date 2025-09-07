from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.user_router import router as user_router
from api.auth_router import router as auth_router


app = FastAPI(
    title="Obscura REST API", version="1.0.0", description="A REST API for Obscura"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)

