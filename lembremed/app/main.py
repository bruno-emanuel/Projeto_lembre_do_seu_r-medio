from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import crud
from .auth import criar_token
from .utils import get_current_user_id
from .scheduler import iniciar_scheduler

app = FastAPI()

Base.metadata.create_all(bind=engine)
iniciar_scheduler()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register(
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    existente = crud.buscar_usuario_por_email(db, email)
    if existente:
        return RedirectResponse("/login", status_code=303)

    usuario = crud.criar_usuario(db, nome, email, senha)
    token = criar_token(usuario.id)

    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("token", token, httponly=True)
    return response

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = crud.buscar_usuario_por_email(db, email)
    if not usuario or usuario.senha != senha:
        return RedirectResponse("/login", status_code=303)

    token = criar_token(usuario.id)
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("token", token, httponly=True)
    return response

@app.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("token")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user_id = get_current_user_id(request)
    if not user_id:
        return RedirectResponse("/login", status_code=303)

    idosos = crud.listar_idosos(db, user_id)
    remedios = crud.listar_remedios(db, user_id)
    historico = crud.listar_historico(db, user_id)[:5]

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "idosos_total": len(idosos),
            "remedios_total": len(remedios),
            "historico": historico
        }
    )
