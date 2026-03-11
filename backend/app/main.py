from fastapi import FastAPI
from api import rooms_endpoint
from infrastructure.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Watch Party API")

Base.metadata.create_all(bind=engine)

# Configuração de CORS para permitir que o Vue.js (em outra porta) converse com o FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Atenção: em produção, coloque a URL exata do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas que criamos no Passo 3
app.include_router(rooms_endpoint.router)

@app.get("/")
def read_root():
    return {"message": "API da Watch Party rodando!"}
