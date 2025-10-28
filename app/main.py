from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import auth, users, clients, contracts, commissions, tables

app = FastAPI(title=settings.APP_NAME)

origins = settings.cors_list() or ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(contracts.router)
app.include_router(commissions.router)
app.include_router(tables.router)

@app.get("/healthz")
def healthz():
    return {"ok": True}
