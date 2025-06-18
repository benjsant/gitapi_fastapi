from pydantic import BaseModel

class User(BaseModel): 
    """
    Modèle représentant un utilisateur.

    Attributs:
        login (str): Le nom d'utilisateur de l'utilisateur.
        id (int): L'identifiant unique de l'utilisateur.
        created_at (str): La date de création du compte de l'utilisateur.
        avatar_url (str): L'URL de l'avatar de l'utilisateur.
        bio (str): La biographie de l'utilisateur.
    """
    login: str
    id: int
    created_at: str
    avatar_url: str
    bio: str