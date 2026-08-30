from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, Annotated
from pydantic import EmailStr, Field as pyField


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(nullable=False, primary_key=True, default=None)
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    Products: list["Product"] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade": "all, delete"})
    

#If the product table is not available it is going to create it.
class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: Optional[int] = Field(primary_key=True, nullable=False, default=None)
    name: str = Field(nullable= False)
    description: str = Field(nullable=False)
    price: int = Field(nullable=False)
    issale: Optional[bool] = Field(default=False, nullable=False)
    inventory: Optional[int] = Field(default=0, nullable=False)
    ownerId: int = Field(foreign_key="users.id", nullable=False, ondelete="CASCADE")
    owner: Optional[User] = Relationship(back_populates="Products")
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

class Vote(SQLModel, table=True):
    __tablename__ = "vote"
    ownerId: int = Field(foreign_key="users.id", nullable=False, primary_key=True, ondelete="CASCADE")
    productId: int = Field(foreign_key="products.id", nullable=False, primary_key=True, ondelete="CASCADE")
    value: int = Field(nullable=False)
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

class VoteUpdate(SQLModel):
    productId: int
    value: Annotated[int, pyField(ge=0, le=1)]

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[int] = None
    issale: Optional[bool] = None
    inventory: Optional[int] = None

class ProductCreate(SQLModel):
    name: str
    price: int 
    issale: bool = False
    inventory: int = 0

class UserRes(SQLModel):
    id: int
    name: str
    email: EmailStr
   

class ProductResponse(SQLModel):
    name: str
    price: int
    issale: bool
    inventory: int
    owner: Optional[UserRes] = None
    class Config:
        from_attributes = True 


class UserCreate(SQLModel):
    name: str
    email: EmailStr
    password: str



class LoginAuthModel(SQLModel):
    email: EmailStr
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    id: Optional[str] = None


class ProductVoteResponse(SQLModel):
    product_id: int
    product_name: str
    vote_count: int
