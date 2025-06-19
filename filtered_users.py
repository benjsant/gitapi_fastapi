import json
from datetime import datetime
from typing import List, Dict

def load_users(filepath: str) -> List[Dict]:
    """
    Charge les utilisateurs à partir d'un fichier JSON.

    Args:
        filepath (str): Le chemin du fichier JSON à charger.

    Returns:
        List[Dict]: Une liste de dictionnaires représentant les utilisateurs.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        users = json.load(file)  # Charge le contenu JSON du fichier dans une variable
    return users  # Retourne la liste des utilisateurs

def remove_duplicates(users: List[Dict]) -> List[Dict]:
    """
    Supprime les utilisateurs en double d'une liste d'utilisateurs.

    Args:
        users (List[Dict]): Une liste de dictionnaires représentant les utilisateurs.

    Returns:
        List[Dict]: Une liste d'utilisateurs sans doublons.
    """
    seen_ids = set()  # Ensemble pour garder une trace des IDs déjà vus
    unique_users = []  # Liste pour stocker les utilisateurs uniques
    for user in users: 
        if user["id"] not in seen_ids:  # Vérifie si l'ID de l'utilisateur n'a pas été vu
            seen_ids.add(user["id"])  # Ajoute l'ID à l'ensemble des IDs vus
            unique_users.append(user)  # Ajoute l'utilisateur à la liste des utilisateurs uniques
    return unique_users  # Retourne la liste des utilisateurs uniques

def is_valid_user(user: Dict) -> bool:
    """
    Vérifie si un utilisateur est valide selon certains critères.

    Args:
        user (Dict): Un dictionnaire représentant un utilisateur.

    Returns:
        bool: True si l'utilisateur est valide, False sinon.
    """
    bio = user.get("bio")  # Récupère la biographie de l'utilisateur
    avatar = user.get("avatar_url")  # Récupère l'URL de l'avatar de l'utilisateur
    created_at = user.get("created_at")  # Récupère la date de création de l'utilisateur

    if not bio or not avatar:  # Vérifie si la biographie ou l'avatar est manquant
        return False  # L'utilisateur n'est pas valide si l'un des deux est manquant
    
    try:
        created_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")  # Convertit la date de création en objet datetime
        if created_date <= datetime(2015, 1, 1):  # Vérifie si la date de création est antérieure ou égale à 2015-01-01
            return False  # L'utilisateur n'est pas valide si la date est trop ancienne
    except Exception:  # Gère les exceptions lors de la conversion de la date
        return False  # L'utilisateur n'est pas valide en cas d'erreur de conversion
    
    return True  # L'utilisateur est valide

def filter_users(users: List[Dict]) -> List[Dict]: 
    """
    Filtre les utilisateurs pour ne garder que ceux qui sont valides.

    Args:
        users (List[Dict]): Une liste de dictionnaires représentant les utilisateurs.

    Returns:
        List[Dict]: Une liste d'utilisateurs valides.
    """
    return [user for user in users if is_valid_user(user)]  # Retourne une liste d'utilisateurs valides

def save_filtered_users(users: List[Dict], output_path: str):
    """
    Sauvegarde les utilisateurs filtrés dans un fichier JSON.

    Args:
        users (List[Dict]): Une liste de dictionnaires représentant les utilisateurs filtrés.
        output_path (str): Le chemin du fichier où sauvegarder les utilisateurs filtrés.
    """
    cleaned_users = [
        {
            "login": user["login"],  # Récupère le login de l'utilisateur
            "id": user["id"],  # Récupère l'ID de l'utilisateur
            "created_at": user["created_at"],  # Récupère la date de création de l'utilisateur
            "avatar_url": user["avatar_url"],  # Récupère l'URL de l'avatar de l'utilisateur
            "bio": user["bio"],  # Récupère la biographie de l'utilisateur
        }
        for user in users  # Pour chaque utilisateur dans la liste
    ]
    with open(output_path, 'w', encoding='utf-8') as file: 
        json.dump(cleaned_users, file, indent=4, ensure_ascii=False)  # Sauvegarde la liste d'utilisateurs dans un fichier JSON
    
def print_summary(initial_count: int, after_dedup: int, final_count: int):
    """
    Affiche un résumé du traitement des utilisateurs.

    Args:
        initial_count (int): Le nombre initial d'utilisateurs chargés.
        after_dedup (int): Le nombre d'utilisateurs après suppression des doublons.
        final_count (int): Le nombre d'utilisateurs après filtrage.
    """
    print("Résumé du traitement :")  # Affiche le titre du résumé
    print(f"Utilisateurs chargés       : {initial_count}")  # Affiche le nombre d'utilisateurs chargés
    print(f"Doublons supprimés         : {initial_count - after_dedup}")  # Affiche le nombre de doublons supprimés
    print(f"Utilisateurs après filtre  : {final_count}")  # Affiche le nombre d'utilisateurs après filtrage

def main():
    """
    Fonction principale qui exécute le traitement des utilisateurs.

    Charge les utilisateurs à partir d'un fichier JSON, supprime les doublons,
    filtre les utilisateurs valides, et sauvegarde le résultat dans un fichier JSON.
    Affiche également un résumé du traitement.
    """
    input_file = "data/users.json"  # Chemin du fichier d'entrée contenant les utilisateurs
    output_file = "data/filtered_users.json"  # Chemin du fichier de sortie pour les utilisateurs filtrés

    users = load_users(input_file)  # Charge les utilisateurs à partir du fichier d'entrée
    initial_count = len(users)  # Compte le nombre initial d'utilisateurs

    unique_users = remove_duplicates(users)  # Supprime les doublons des utilisateurs
    after_dedup = len(unique_users)  # Compte le nombre d'utilisateurs après suppression des doublons

    filtered_users = filter_users(unique_users)  # Filtre les utilisateurs valides
    final_count = len(filtered_users)  # Compte le nombre d'utilisateurs après filtrage

    save_filtered_users(filtered_users, output_file)  # Sauvegarde les utilisateurs filtrés dans le fichier de sortie
    print_summary(initial_count, after_dedup, final_count)  # Affiche le résumé du traitement

if __name__ == "__main__":
    main()  # Exécute la fonction principale si le script est exécuté directement

