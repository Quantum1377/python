from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class WalletOut(BaseModel):
    id: int
    user_id: int
    balance: float
    currency: str

    class Config:
        orm_mode = True

class DepositIn(BaseModel):
    amount: float = Field(..., gt=0)
    description: Optional[str] = None

class TransferIn(BaseModel):
    to_username: str
    amount: float = Field(..., gt=0)
    description: Optional[str] = None

class TransactionOut(BaseModel):
    id: int
    wallet_id: int
    type: str
    amount: float
    metadata: Optional[str]
    timestamp: datetime

    class Config:
        orm_mode = True
