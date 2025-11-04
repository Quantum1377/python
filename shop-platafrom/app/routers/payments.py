from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import db, crud, schemas, auth
from ..models import User as UserModel

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/transfer", response_model=schemas.TransactionOut)
def transfer(t: schemas.TransferIn, current_user = Depends(auth.get_current_user), db_s: Session = Depends(db.get_db)):
    from_wallet = crud.get_wallet_by_user(db_s, current_user.id)
    to_user = db_s.query(UserModel).filter(UserModel.username == t.to_username).first()
    if not to_user:
        raise HTTPException(status_code=404, detail="Beneficiário não encontrado")
    try:
        from_wallet, to_wallet, tx_from, tx_to = crud.transfer(db_s, from_wallet, to_user, t.amount, t.description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # retorno: tx_from (registro do débito na conta do remetente)
    return tx_from

@router.get("/history", response_model=list[schemas.TransactionOut])
def history(limit: int = 100, current_user = Depends(auth.get_current_user), db_s: Session = Depends(db.get_db)):
    wallet = crud.get_wallet_by_user(db_s, current_user.id)
    txs = crud.get_transactions_for_wallet(db_s, wallet.id, limit)
    return txs
