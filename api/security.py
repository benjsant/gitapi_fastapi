from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets 
import os 
from dotenv import load_dotenv

# Charger les variables d'environnement à partir d'un fichier .env
load_dotenv()

# Dictionnaire contenant les identifiants valides, chargés depuis les variables d'environnement
VALID_CREDENTIALS = {
    os.getenv("USERNAME"): os.getenv("PASSWORD")
}

# Instance de sécurité pour l'authentification HTTP Basic
security = HTTPBasic()

# # Identifiants autorisés (on peux charger ça depuis un .env également)
# VALID_CREDENTIALS = {
#     "admin": "admin123"
# }

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Récupère l'utilisateur actuel en vérifiant les identifiants fournis.

    Args:
        credentials (HTTPBasicCredentials): Les identifiants de l'utilisateur fournis via l'authentification HTTP Basic.

    Raises:
        HTTPException: Si les identifiants sont invalides, une exception HTTP 401 est levée.

    Returns:
        str: Le nom d'utilisateur de l'utilisateur authentifié.
    """
    correct_username = credentials.username
    correct_password = credentials.password

    expected_pasword = VALID_CREDENTIALS.get(correct_username)

    if not expected_pasword or not secrets.compare_digest(expected_pasword, correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants Invalide",
            headers={"WWW-Authenticate": "Basic"},
        )
    return correct_username

