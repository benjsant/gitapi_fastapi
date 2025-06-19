import pytest
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials
from api.security import get_current_user 

def test_valid_credentials():
    """
    Teste la validation des identifiants valides. Vérifie que 
    l'utilisateur est correctement identifié comme "admin" 
    lorsque des identifiants valides sont fournis.
    """
    credentials = HTTPBasicCredentials(username="admin", password="admin123")
    assert get_current_user(credentials) == "admin"

def test_invalid_password():
    """
    Teste la gestion d'un mot de passe invalide. Vérifie que 
    l'appel à get_current_user lève une HTTPException avec 
    un code de statut 401 lorsque le mot de passe est incorrect.
    """
    credentials = HTTPBasicCredentials(username="admin", password="wrongpass")
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials)
    assert exc_info.value.status_code == 401 

def test_unknown_user():
    """
    Teste la gestion d'un utilisateur inconnu. Vérifie que 
    l'appel à get_current_user lève une HTTPException avec 
    un code de statut 401 lorsque le nom d'utilisateur n'est pas reconnu.
    """
    credenitials = HTTPBasicCredentials(username="unknown", password="admin123")
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credenitials)
    assert exc_info.value.status_code == 401 
