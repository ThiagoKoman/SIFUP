from pydantic import BaseModel
import datetime

class ExpenseCreate(BaseModel):
    bank_account: str
    date: datetime.date
    category: str
    value: float
    description: str


class ExpenseUpdate(BaseModel):
    bank_account: str
    date: str
    category: str
    value: float
    description: str

class AccountModel(BaseModel):
    bank: str
    acc_type: str
    active: bool