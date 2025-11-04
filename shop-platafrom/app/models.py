from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base
import enum

class TransactionType(str, enum.Enum):
    DEPOSIT = "deposit"
    TRANSFER = "transfer"
    PAYMENT = "payment"
    WITHDRAW = "withdraw"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    wallet = relationship("Wallet", uselist=False, back_populates="owner")

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    balance = Column(Float, default=0.0)
    currency = Column(String(8), default="BRL")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="wallet")
    transactions = relationship("Transaction", back_populates="wallet")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    metadata = Column(Text, nullable=True)  # e.g., {"from": userA, "to": userB, "desc": ""}
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    wallet = relationship("Wallet", back_populates="transactions")
