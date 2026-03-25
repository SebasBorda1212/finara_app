from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Transaction, User
from auth import verify_token
from fastapi.security import OAuth2PasswordBearer
import schemas

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_transaction(
    transaction: schemas.TransactionCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    data = verify_token(token)
    user = db.query(User).filter(User.email == data["sub"]).first()

    new_transaction = Transaction(
        amount=transaction.amount,
        type=transaction.type,
        description=transaction.description,
        user_id=user.id
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


@router.get("/")
def get_transactions(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    data = verify_token(token)
    user = db.query(User).filter(User.email == data["sub"]).first()

    transactions = db.query(Transaction).filter(
        Transaction.user_id == user.id
    ).all()

    return transactions