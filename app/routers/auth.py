from multiprocessing.managers import Token
from fastapi import APIRouter, Depends, status, HTTPException, Body
from typing import Annotated
from ..models import Token, User
from sqlmodel.ext.asyncio.session import AsyncSession
from ..utils import get_db, verify_password, create_access_token
from sqlmodel import select
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication", 'login']
)

 

@router.post("/login", response_model=Token)
async def login(session: Annotated[AsyncSession, Depends(get_db)], payload: Annotated[OAuth2PasswordRequestForm, Depends()]):

    query = select(User).where(User.email == payload.username)
    executeQ = await session.exec(query)
    results = executeQ.first()

    if not results or not verify_password(results.password, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_access_token({"userId": str(results.id)})
    return {"access_token": access_token, "token_type": "bearer"}
 
