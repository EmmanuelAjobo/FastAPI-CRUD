from sqlalchemy.orm import selectinload
from fastapi import Depends ,status, Body, HTTPException, Path, APIRouter, Query
from ..models import Product, ProductUpdate, ProductCreate, ProductResponse, ProductVoteResponse, User, Vote
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated, List, Optional;
from ..utils import get_db, get_current_user
from sqlmodel import select, func

################## MAJOR FUNCTIONS ##################
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

################## DELETE POST ##################

@router.delete("/{id}", response_model=ProductResponse)
async def deletePost(
        db_session: Annotated[AsyncSession, Depends(get_db)], 
        id: Annotated[int, Path()],  
        current_user: Annotated[User, Depends(get_current_user)]
    ):
    post = select(Product).where(Product.id == id).options(selectinload(Product.owner))
    post = await db_session.exec(post)
    post = post.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # 2. Authorization check: Ensure user owns the product
    if post.ownerId != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to perform requested action"
        )
    await db_session.delete(post)
    await db_session.commit()
    return post


################## GET POST ##################

@router.get("/postvote", response_model=List[ProductVoteResponse])
async def productvote(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)]
    ):
    statement = (
                    select(Product, func.count(Vote.productId).label("vote"))
                    .outerjoin(Vote, Product.id == Vote.productId)
                    .group_by(Product.id)
                 )
    result = await db_session.exec(statement)
    prodvote = result.all()

    return [
        ProductVoteResponse(
            product_id = product.id,
            product_name = product.name,
            vote_count = vote
        ) for product, vote in prodvote
    ]



#PUBLIC
@router.get("/", response_model=List[ProductResponse])
async def getProductOfUser(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
        limit: Annotated[int, Query()] = 10,
        skip: Annotated[int, Query()] = 0,
        search: Annotated[Optional[str], Query()] = ""
    ):

    statement = select(Product).options(selectinload(Product.owner))

    if search:
        statement = statement.where(Product.name.contains(search))

    statement = statement.limit(limit).offset(skip)

    result = await db_session.exec(statement)
    products = result.all()

    return products




@router.get('/{id}', response_model=ProductResponse)
async def getproduct(
        id: Annotated[int, Path()], 
        db_session: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)]
    ):
    product = select(Product).where(Product.id == id).options(selectinload(Product.owner))
    product = await db_session.exec(product)
    product = product.first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} id could not be found")

     # 2. Authorization check: Ensure user owns the product
    if product.ownerId != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to perform requested action"
        )
    return product






# ################## POST UPDATED ##################

@router.put("/{id}", response_model=ProductResponse)
async def updateProduct(
        id: Annotated[int, Path()], 
        payload: Annotated[ProductUpdate, Body()] , 
        db_session: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)]
    ):
    #Fetch an existing Item
    product = select(Product).where(Product.id == id).options(selectinload(Product.owner))
    product = await db_session.exec(product)
    product = product.first()

    if not product or product.ownerId != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to perform requested action"
        )

    #Extract Incoming data (excluding unset field if using partial updates)
    #This is responsible for partial updates, meaning only the fields provided in the request will be updated, while the rest will remain unchanged.
    update_product = payload.model_dump(exclude_unset=True)

    #Update the existing database object attributes 
    for key, val in update_product.items():
        setattr(product, key, val)

    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)

    return product

# ################## PRODUCTS CREATED ##################

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def createPost(
        payload: Annotated[ProductCreate, Body()], 
        db_session: Annotated[AsyncSession, Depends(get_db)],  
        current_user: Annotated[User, Depends(get_current_user)]
    ):
    product = Product.model_validate(payload.model_dump(), update={'ownerId': int(current_user.id)})

    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)
    print(f"Product created with ID: {product.id}, Owner ID: {product.ownerId}")
    return product

