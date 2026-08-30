from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .engine import engine
from sqlmodel import SQLModel, select
from contextlib import asynccontextmanager
from .routers import user, post, auth, vote
################## CONNECTION TO DATABASE ##################

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan);

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "Home link"}

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

