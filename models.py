from sqlalchemy import Column, Integer,Numeric, String, Float, DateTime, ForeignKey, func, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# Таблица банковских счетов
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    balance = Column(Float, default=0.0)

    incomes = relationship("Income", back_populates="account")  # Связь с доходами
    expenses = relationship("Expense", back_populates="account")  # Связь с расходами

# Таблица наличных денег
class Cash(Base):
    __tablename__ = "cash"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    updated_at = Column(TIMESTAMP, server_default=func.now())
    note = Column(String, nullable=True)

# Таблица транзакция наличных денег
class TransactionCash(Base):
    __tablename__ = "transactions_cash"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(10), nullable=False)  # "income" или "expense"
    amount = Column(Numeric(10, 2), nullable=False)
    date = Column(TIMESTAMP, server_default=func.now())


# Таблица запланированных расходов
class PlannedExpense(Base):
    __tablename__ = "planned_expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)

# Таблица истории трат
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=func.now())
    category = Column(String)
    account_id = Column(Integer, ForeignKey("accounts.id"))  # Связь с accounts
    cash_id = Column(Integer, ForeignKey("cash.id"), nullable=True)  # Наличные деньги

    account = relationship("Account", back_populates="expenses")
    cash = relationship("Cash", back_populates="expenses")  # Связь с cash

# Таблица доходов
class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=func.now())

    account_id = Column(Integer, ForeignKey("accounts.id"))  # Связь с accounts
    cash_id = Column(Integer, ForeignKey("cash.id"), nullable=True)  # Наличные деньги

    account = relationship("Account", back_populates="incomes")
    cash = relationship("Cash", back_populates="incomes")  # Связь с cash

# Таблица напоминаний
class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False)
