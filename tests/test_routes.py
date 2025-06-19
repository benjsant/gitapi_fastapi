import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from api.main import app
from dotenv import load_dotenv

# Charger les variables d'environnement à partir d'un fichier .env
load_dotenv()

client = TestClient(app)

# Credentials valides 
auth = (os.getenv("USERNAME"),os.getenv("PASSWORD"))

def test_get_users_success():
    """
    Teste la récupération de la liste des utilisateurs avec des 
    identifiants valides. Vérifie que le code de statut de la 
    réponse est 200 et que le contenu de la réponse est une liste.
    """
    response = client.get("/users", auth=auth)
    assert response.status_code == 200 
    assert isinstance(response.json(), list)

def test_get_user_by_login_success():
    """
    Teste la récupération d'un utilisateur par son login avec des 
    identifiants valides. Vérifie que le code de statut de la 
    réponse est 200 et que le login de l'utilisateur correspond 
    à celui recherché. Si l'utilisateur n'est pas trouvé, 
    vérifie que le code de statut est 404.
    """
    verif = "MatzeJ"
    response = client.get("/users/{verif}", auth=auth)
    if response.status_code == 200:
        data = response.json()
        assert data["login"].lower() == verif.lower()
    else:
        assert response.status_code == 404  # au cas où l'utilisateur n'est pas dans le JSON

def test_get_user_by_login_not_found():
    """
    Teste la récupération d'un utilisateur par un login inexistant. 
    Vérifie que le code de statut de la réponse est 404.
    """
    response = client.get("/users/inexistantuser", auth=auth)
    assert response.status_code == 404

def test_search_users_success():
    """
    Teste la recherche d'utilisateurs avec des identifiants valides. 
    Vérifie que le code de statut de la réponse est 200 et que le 
    contenu de la réponse est une liste.
    """
    response = client.get("/users/search?q=ma", auth=auth)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_unauthorized_access():
    """
    Teste l'accès non autorisé à la liste des utilisateurs sans 
    fournir d'identifiants. Vérifie que le code de statut de la 
    réponse est 401.
    """
    response = client.get("/users")
    assert response.status_code == 401 
