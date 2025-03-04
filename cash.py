from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Cash, TransactionCash
from schemas import CashResponse, TransactionCreate

router = APIRouter()

# Получение текущего баланса наличных
@router.get("/cash", response_model=CashResponse)
def get_cash_balance(db: Session = Depends(get_db)):
    cash = db.query(Cash).first()
    if not cash:
        return {"amount": 0.00, "updated_at": None}
    return cash

# Добавление новой операции
@router.post("/cash/add")
def add_cash(transaction: TransactionCreate, db: Session = Depends(get_db)):
    if transaction.type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Тип операции должен быть 'income' или 'expense'")

    # Получаем текущий баланс
    cash = db.query(Cash).first()
    if not cash:
        cash = Cash(amount=0.00)
        db.add(cash)
        db.commit()
        db.refresh(cash)

    # Обновляем баланс
    if transaction.type == "income":
        cash.amount += transaction.amount
    elif transaction.type == "expense":
        if cash.amount < transaction.amount:
            raise HTTPException(status_code=400, detail="Недостаточно средств")
        cash.amount -= transaction.amount

    # Добавляем запись в историю транзакций
    new_transaction = TransactionCash(type=transaction.type, amount=transaction.amount)
    db.add(new_transaction)
    db.commit()
    db.refresh(cash)

    return {"new_balance": cash.amount}
