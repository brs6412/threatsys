from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.routers import organizations, users, iocs
from src.exceptions import setup_handlers

settings = get_settings()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_handlers(app)

app.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(iocs.router, prefix="/iocs", tags=["IOCs"])

@app.get("/healthy")
async def root():
    return {"message": "Welcome to Threatsys API"}
