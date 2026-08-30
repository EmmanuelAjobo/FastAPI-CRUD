from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from ..utils import get_db, get_current_user
from typing import Annotated
from ..models import User, Product, VoteUpdate, Vote
from sqlmodel import select

router = APIRouter(
    prefix="/vote",
    tags=['votes']
);
# Schema expecting 0 (remove vote), or 1 (upvote)
# class VoteUpdate(SQLModel): 
#     productId: int
#     value: int = Field(ge=0, le=1)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def addVote(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    payload: Annotated[VoteUpdate, Body()],
    current_user: Annotated[User, Depends(get_current_user)],
):
    # 1. Verify Product exists
    product = await db_session.get(Product, payload.productId)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Product not found"
        )

    # 2. Check existing vote
    statement = select(Vote).where(
        Vote.productId == payload.productId,
        Vote.ownerId == current_user.id
    )
    result = await db_session.exec(statement)
    existing_vote = result.first()

    # 3. Handle Vote logic
    if payload.value == 1:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="You have already liked this product"
            )
        
        new_vote = Vote(
            value=1,
            ownerId=current_user.id,
            productId=payload.productId
        )
        db_session.add(new_vote)
        await db_session.commit()
        return {"message": "Vote created successfully"}

    elif payload.value == 0:
        if not existing_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="You cannot remove a vote that does not exist"
            )

        await db_session.delete(existing_vote)
        await db_session.commit()
        return {"message": "Vote removed successfully"}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Invalid vote value. Allowed values are 0 or 1."
    )


