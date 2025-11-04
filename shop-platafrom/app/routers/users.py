from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, db, auth

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db_s: Session = Depends(db.get_db)):
    existing = db_s.query(crud.models.User).filter(crud.models.User.username==user_in.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    user = crud.create_user(db_s, user_in)
    return user

@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserCreate, db_s: Session = Depends(db.get_db)):
    # Reusing UserCreate for simplicity (username + password)
    user = crud.authenticate_user(db_s, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    access_token = auth.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def read_me(current_user = Depends(auth.get_current_user)):
    return current_user
