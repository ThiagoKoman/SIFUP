from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseUpdate
import datetime

router = APIRouter()

@router.post("/add-expense/")
async def add_expense(
    bank_account: int = Form(...),
    date: str = Form(...),
    category: str = Form(...),
    value: float = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    expense = Expense(
        bank_account=bank_account,
        date=datetime.datetime.strptime(date, "%Y-%m-%d").date(),
        category=category,
        value=value,
        description=description,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return RedirectResponse("/expenses", status_code=303)


@router.delete("/delete-expense/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    db.delete(expense)
    db.commit()
    return {"message": "Registro excluído com sucesso"}


@router.put("/edit-expense/{expense_id}")
def edit_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    db_expense.bank_account = expense.bank_account
    db_expense.date = datetime.datetime.strptime(expense.date, '%Y-%m-%d').date()
    db_expense.category = expense.category
    db_expense.value = expense.value
    db_expense.description = expense.description
    db.commit()
    return {"message": "Registro atualizado com sucesso"}


@router.get("/get-expense/{expense_id}")
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return expense
