from fastapi import Depends ,status, Body, HTTPException, Path, APIRouter
from ..models import User, UserRes, UserCreate
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated, List;
from ..utils import hash_password, get_db
from sqlmodel import select
from sqlalchemy.exc import IntegrityError



# ################## CONNECTION ##################
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# ################## USER GOTTEN ##################
@router.get("/{id}", response_model=UserRes)
async def getUser(id: Annotated[int, Path()], session: Annotated[AsyncSession, Depends(get_db)]):
    user = await session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/", response_model=List[UserRes])
async def getAllPost(session: Annotated[AsyncSession, Depends(get_db)]):
    query = select(User)
    execquery = await session.exec(query)
    results = execquery.all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    return results

# ################## USER CREATED ##################
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserRes)
async def createUser(
    session: Annotated[AsyncSession, Depends(get_db)],
    payload: Annotated[UserCreate, Body()]):

    payload_data = payload.model_dump()
    payload_data['password'] = hash_password(payload_data['password'])
    
    user = User.model_validate(payload_data);

    try:
        session.add(user)
        #Commit is where deplicate e mail 
        await session.commit();
    
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email is already registered")

    await session.refresh(user)
    return user


 # ################## USER DELETED ##################
 