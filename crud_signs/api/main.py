from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas, crud, auth
from .database import engine, SessionLocal
from .dependencies import get_db
from .auth import get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AUTH ---
@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(user["username"])
    return {"access_token": access_token, "token_type": "bearer"}

# --- CLIENTS ---
@app.post("/clients/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.create_client(db, client)

@app.get("/clients/", response_model=list[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.get_clients(db, skip=skip, limit=limit)

@app.put("/clients/{client_id}", response_model=schemas.Client)
def update_client(client_id: int, client: schemas.ClientCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    updated = crud.update_client(db, client_id, client)
    if not updated:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated

@app.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    if crud.delete_client(db, client_id):
        return {"detail": "Deleted"}
    raise HTTPException(status_code=404, detail="Client not found")

@app.get("/clients/search/", response_model=list[schemas.Client])
def search_clients(query: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.search_clients(db, query)

# --- ORDERS ---
@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.create_order(db, order)

@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return crud.get_orders(db, skip=skip, limit=limit)

@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    updated = crud.update_order(db, order_id, order)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    if crud.delete_order(db, order_id):
        return {"detail": "Deleted"}
    raise HTTPException(status_code=404, detail="Order not found")