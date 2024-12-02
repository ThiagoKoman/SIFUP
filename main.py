from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import expenses
from app.routers import frontend as frontend_router

app = FastAPI()

# Ajusta o caminho para facilitar os imports
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#ROTAS BACKEND
app.include_router(expenses.router, tags=["Expenses"])

#ROTAS FRONTEND
app.include_router(frontend_router.router, tags=["Frontend"])
