from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base  # Modifique aqui
from sqlalchemy import create_engine

# Criação da base para os modelos
Base = declarative_base() 

# Tabela de Contas Bancárias (Account)
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    bank = Column(String, nullable=False)
    acc_type = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    # Relacionamento com Expense (1:N)
    expenses = relationship("Expense", back_populates="account")
    # Relacionamento com Entrie (1:N)
    entries = relationship("Entrie", back_populates="account")

# Tabela de Despesas (Expense)
class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    bank_account = Column(Integer, ForeignKey('accounts.id'), nullable=False)  # Chave estrangeira para Account
    date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    description = Column(String, nullable=True)

    # Relacionamento com Account (N:1)
    account = relationship("Account", back_populates="expenses")
    # Relacionamento com Investment (1:N)
    investments = relationship("Investment", back_populates="expense_details")

# Tabela de Entradas (Entrie)
class Entrie(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, index=True)
    bank_account = Column(Integer, ForeignKey('accounts.id'), nullable=False)  # Chave estrangeira para Account
    date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    description = Column(String, nullable=True)

    # Relacionamento com Account (N:1)
    account = relationship("Account", back_populates="entries")

# Tabela de Investimentos (Investment)
class Investment(Base):
    __tablename__ = "investments"
    id = Column(Integer, primary_key=True, index=True)
    expense = Column(Integer, ForeignKey('expenses.id'), nullable=False)  # Chave estrangeira para Expense
    date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    refund_date = Column(Date, nullable=True)
    refund_value = Column(Float, nullable=True)

    # Relacionamento com Expense (N:1)
    expense_details = relationship("Expense", back_populates="investments")
    # Relacionamento com InvestmentBalance (1:N)
    balances = relationship("InvestmentBalance", back_populates="investment_details")

# Tabela de Saldo de Investimentos (InvestmentBalance)
class InvestmentBalance(Base):
    __tablename__ = "balances"
    id = Column(Integer, primary_key=True, index=True)
    investment = Column(Integer, ForeignKey('investments.id'), nullable=False)  # Chave estrangeira para Investment
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)

    # Relacionamento com Investment (N:1)
    investment_details = relationship("Investment", back_populates="balances")


# Configurar o banco SQLite
DATABASE_URL = "sqlite:///./expenses.db"
engine = create_engine(DATABASE_URL)

# Criando a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)
