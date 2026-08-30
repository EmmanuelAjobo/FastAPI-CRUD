from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlmodel.ext.asyncio.session import AsyncSession
from .engine import engine, settings
import jwt
from datetime import datetime, timedelta, timezone
import os
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from .models import TokenData, User



#################################### CONFIGURATIONS ####################################
ph = PasswordHasher()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

#SESSION 
async def get_db():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


#################################### JWT TOKEN FUNCTIONS ####################################

def create_access_token(payload: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = payload.copy()
    expires_ = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expires_})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

def verify_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id:str = payload.get("userId")
        if user_id is None:
            raise credentials_exception
        return TokenData(id=user_id)
    except jwt.PyJWTError:
        raise credentials_exception
 

async def get_current_user(token: str = Depends(oauth2_scheme), db_session: AsyncSession = Depends(get_db)) -> User:
    token_data = verify_access_token(token)

    #so easy, we only grabbed the user id from the token, now we can use it to get the user data from the database
    users_data = await db_session.get(User, int(token_data.id))

    if not users_data:
        raise credentials_exception
    return users_data
################## MAJOR FUNCTIONS ##################

def hash_password(payload: str) -> str:
    return ph.hash(payload)

def verify_password(hashed_password: str, plain_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False

