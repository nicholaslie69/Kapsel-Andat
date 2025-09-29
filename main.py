from fastapi import FastAPI
from modules.users.routes import create_user, read_user, update_user, delete_user

app = FastAPI(
    title="Users Module CRUD API",
    description="Kapita Selekta Analitika Data: Tugas 2 - CRUD API untuk Users Module",
    version="1.0.0"
)

app.include_router(create_user.router)
app.include_router(read_user.router)
app.include_router(update_user.router)
app.include_router(delete_user.router)

@app.get("/")
def read_root():
    return {"message": "Users Module API is running. Check /docs for documentation."}