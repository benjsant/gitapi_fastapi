from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="Api utilisateurs Github du 01-01-2015 à partir de 23h59",
    description="API REST interne pour explore des utilisateurs Github filtrées.",
    version="1.0.0"
)

# Inclusion des routes pour gérer les utilisateurs
app.include_router(router)