from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import db, crud, schemas, auth

router = APIRouter(prefix="/wallet", tags=["wallet"])

@router.get("/me", response_model=schemas.WalletOut)
def get_my_wallet(current_user = Depends(auth.get_current_user), db_s: Session = Depends(db.get_db)):
    wallet = crud.get_wallet_by_user(db_s, current_user.id)
    return wallet

@router.post("/deposit", response_model=schemas.TransactionOut)
def deposit(deposit_in: schemas.DepositIn, current_user = Depends(auth.get_current_user), db_s: Session = Depends(db.get_db)):
    wallet = crud.get_wallet_by_user(db_s, current_user.id)
    wallet, tx = crud.deposit(db_s, wallet, deposit_in.amount, deposit_in.description)
    return tx
