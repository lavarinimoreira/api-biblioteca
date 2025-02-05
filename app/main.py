from fastapi import FastAPI
from app.services.scheduler import iniciar_scheduler
from app.routers import books, users, loans


app = FastAPI()

@app.get('/healthy')
def health_check():
    return{'status': 'Healthy'}

# Inicializa o Scheduler quando a aplicação inicia
@app.on_event("startup")
async def startup_event():
    iniciar_scheduler()


app.include_router(books.router)
app.include_router(users.router)
app.include_router(loans.router)