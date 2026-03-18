from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.context import CryptContext
from pydantic import BaseModel
import uvicorn
import os

# Database setup
DATABASE_URL = "sqlite:///./finance_optimizer.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    category = Column(String)
    date = Column(Date)
    user = relationship("User")

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String)
    limit = Column(Float)
    period = Column(String)
    user = relationship("User")

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String)
    target_amount = Column(Float)
    current_amount = Column(Float)
    deadline = Column(Date)
    user = relationship("User")

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class BudgetCreate(BaseModel):
    user_id: int
    category: str
    limit: float
    period: str

class GoalCreate(BaseModel):
    user_id: int
    description: str
    target_amount: float
    current_amount: float
    deadline: str

# Create tables
Base.metadata.create_all(bind=engine)

# Seed data
def seed_data(db):
    if db.query(User).count() == 0:
        user = User(name="John Doe", email="john@example.com", password_hash=pwd_context.hash("password"))
        db.add(user)
        db.commit()

# FastAPI app
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return open("templates/index.html").read()

@app.post("/api/budget")
async def create_budget(budget: BudgetCreate, db: SessionLocal = Depends(get_db)):
    db_budget = Budget(**budget.dict())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

@app.get("/api/transactions")
async def get_transactions(user_id: int, db: SessionLocal = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    return transactions

@app.post("/api/goals")
async def create_goal(goal: GoalCreate, db: SessionLocal = Depends(get_db)):
    db_goal = Goal(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@app.get("/api/insights")
async def get_insights(user_id: int):
    # Mock AI-driven insights
    return {"insights": "Save more by reducing dining expenses."}

if __name__ == "__main__":
    # Seed data
    db = SessionLocal()
    seed_data(db)
    db.close()
    # Run app
    uvicorn.run(app, host="0.0.0.0", port=8000)
