from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .models import User
from .security import get_current_user 
import json 

# Création d'un routeur API pour gérer les routes liées aux utilisateurs
router = APIRouter()

# Chargement unique des utilisateurs à l'import 
with open("data/filtered_users.json", encoding='utf-8') as f:
    users_data = json.load(f)

@router.get("/users", response_model=List[User], summary="Liste des utilisateurs", description="Retourne tous les utilisateurs filtrés disponibles")
def get_users(current_user: str = Depends(get_current_user)):
    """
    Récupère la liste de tous les utilisateurs filtrés.

    Args:
        current_user (str): Le nom d'utilisateur de l'utilisateur authentifié.

    Returns:
        List[User]: Une liste d'objets utilisateur.
    """
    return users_data

@router.get("/users/search", response_model=List[User], summary="Recherche d'utilisateurs", description="Recherche les utilisateurs dont le login contient un mot-clé")
def search_users(q: str, current_user: str = Depends(get_current_user)):
    """
    Recherche des utilisateurs dont le login contient un mot-clé.

    Args:
        q (str): Le mot-clé à rechercher dans les logins des utilisateurs.
        current_user (str): Le nom d'utilisateur de l'utilisateur authentifié.

    Returns:
        List[User]: Une liste d'objets utilisateur correspondant à la recherche.
    """
    results = [user for user in users_data if q.lower() in user["login"].lower()]
    return results

@router.get("/users/{login}", response_model=User, summary="Détails d'un utilisateur", description="Retourne les détails d'un utilisateur via son login exact")
def get_users_by_login(login: str, current_user: str = Depends(get_current_user)):
    """
    Récupère les détails d'un utilisateur en fonction de son login.

    Args:
        login (str): Le login de l'utilisateur à rechercher.
        current_user (str): Le nom d'utilisateur de l'utilisateur authentifié.

    Raises:
        HTTPException: Si l'utilisateur n'est pas trouvé, une exception 404 est levée.

    Returns:
        User: L'objet utilisateur correspondant au login fourni.
    """
    for user in users_data:
        if user["login"].lower() == login.lower():
            return user
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
