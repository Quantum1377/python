from sqlalchemy.orm import Session
from . import models, schemas, auth
from typing import Optional

# Users
def create_user(db: Session, user_in: schemas.UserCreate):
    hashed = auth.get_password_hash(user_in.password)
    user = models.User(username=user_in.username, email=user_in.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    # create wallet
    wallet = models.Wallet(user_id=user.id, balance=0.0, currency="BRL")
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    if not auth.verify_password(password, user.hashed_password):
        return None
    return user

# Wallets & Transactions
def get_wallet_by_user(db: Session, user_id: int):
    return db.query(models.Wallet).filter(models.Wallet.user_id == user_id).first()

def deposit(db: Session, wallet: models.Wallet, amount: float, description: Optional[str]=None):
    wallet.balance += amount
    tx = models.Transaction(wallet_id=wallet.id, type=models.TransactionType.DEPOSIT, amount=amount, metadata=description or "")
    db.add(tx)
    db.commit()
    db.refresh(wallet)
    db.refresh(tx)
    return wallet, tx

def transfer(db: Session, from_wallet: models.Wallet, to_user: models.User, amount: float, description: Optional[str]=None):
    if from_wallet.balance < amount:
        raise ValueError("Saldo insuficiente")
    to_wallet = get_wallet_by_user(db, to_user.id)
    from_wallet.balance -= amount
    to_wallet.balance += amount
    tx_from = models.Transaction(wallet_id=from_wallet.id, type=models.TransactionType.TRANSFER, amount=-amount, metadata=f"to:{to_user.username};{description or ''}")
    tx_to = models.Transaction(wallet_id=to_wallet.id, type=models.TransactionType.TRANSFER, amount=amount, metadata=f"from:{from_wallet.user_id};{description or ''}")
    db.add_all([tx_from, tx_to])
    db.commit()
    db.refresh(from_wallet)
    db.refresh(to_wallet)
    db.refresh(tx_from)
    db.refresh(tx_to)
    return from_wallet, to_wallet, tx_from, tx_to

def get_transactions_for_wallet(db: Session, wallet_id: int, limit: int = 100):
    return db.query(models.Transaction).filter(models.Transaction.wallet_id == wallet_id).order_by(models.Transaction.timestamp.desc()).limit(limit).all()
