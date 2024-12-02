from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from sqlalchemy import desc 

#Models
from app.models import Account
from app.models import Expense

# Criação do router para as rotas de frontend
router = APIRouter()

# Configuração dos templates
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/accounts", response_class=HTMLResponse)
async def read_accounts(request: Request, db: Session = Depends(get_db)):
    accounts = db.query(Account).all()
    return templates.TemplateResponse("pages/account.html", {"request": request, "accounts": accounts})

@router.get("/investment", response_class=HTMLResponse)
async def read_investment(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("pages/investment.html", {"request": request})

@router.get("/entries", response_class=HTMLResponse)
async def read_entries(request: Request, db: Session = Depends(get_db)):
    # Renderiza o template com variáveis
    expenses = db.query(Expense).order_by(desc(Expense.date)).all()
    return templates.TemplateResponse("pages/entries.html", {"request": request, "expenses": expenses})

@router.get("/expenses", response_class=HTMLResponse)
async def read_outs(request: Request, db: Session = Depends(get_db)):
    # Renderiza o template com variáveis
    expenses = db.query(Expense, Account).join(Account, Account.id == Expense.bank_account).order_by(desc(Expense.date)).all()
    expenses_data = [
        {
            "expense": expense,  # O objeto Expense
            "account_bank": account.bank,  # O campo bank da Account
            "account_acc_type": account.acc_type  # O campo acc_type da Account
        }
        for expense, account in expenses
    ]
    accounts = db.query(Account).all()
    return templates.TemplateResponse("pages/expenses.html", {"request": request, "expenses": expenses_data,  "accounts": accounts})

@router.get("/analytics", response_class=HTMLResponse)
async def read_analytics(request: Request, db: Session = Depends(get_db)):
    # Renderiza o template com variáveis
    expenses = []
    return templates.TemplateResponse("pages/analises.html", {"request": request, "expenses": expenses})