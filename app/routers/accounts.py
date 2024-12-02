from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Account
from app.schemas import AccountModel
import datetime

router = APIRouter()

@router.post("/add-account/")
async def add_account(
    bank: str = Form(...),
    type: str = Form(...),
    db: Session = Depends(get_db),
):
    account = Account(
        bank=bank,
        acc_type=type
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return RedirectResponse("/accounts", status_code=303)

@router.put("/edit-account-active/{account_id}/{status}")
def edit_account(account_id: int, status: str ,db: Session = Depends(get_db)):
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    
    if status == 'true':
        db_account.active = True
    else:
        db_account.active = False

    db.commit()
    return {"message": "Registro atualizado com sucesso"}