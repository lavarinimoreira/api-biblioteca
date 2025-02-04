from fastapi import FastAPI
from app.routers import books, users


app = FastAPI()

@app.get('/healthy')
def health_check():
    return{'status': 'Healthy'}


app.include_router(books.router)
app.include_router(users.router)