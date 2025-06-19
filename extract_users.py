import requests
import json
import time 
import os 
from dotenv import load_dotenv
from pathlib import Path
from argparse import ArgumentParser

#Chargement du token Github depus le fichier .env
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# Chemin de fichiers de sortie 
OUTPUT_PATH = Path("data/users.json")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def check_rate_limit(response):
    """
    Vérifie la limite de taux de l'API GitHub.

    Si le quota de requêtes est atteint, la fonction met le programme en pause
    jusqu'à ce que le quota soit réinitialisé.

    Args:
        response (requests.Response): La réponse de la requête API pour vérifier les en-têtes de limite de taux.
    """
    remaining = int(response.headers.get("X-RateLimit-Remaining", 1))
    reset_time = int(response.headers.get("X-RateLimit-Reset", time.time()))
    if remaining == 0:
        # Calcule le temps de sommeil jusqu'à la réinitialisation du quota
        sleep_duration = max(0, reset_time - int(time.time())) + 1
        print(f"Quota atteint. Pause de {sleep_duration} secondes.")
        time.sleep(sleep_duration)

def fetch_user_details(login):
    """
    Récupère les détails d'un utilisateur GitHub à partir de son login.

    Effectue une requête à l'API GitHub pour obtenir les informations de l'utilisateur
    et renvoie un dictionnaire contenant les détails pertinents.

    Args:
        login (str): Le login de l'utilisateur GitHub.

    Returns:
        dict: Un dictionnaire contenant les détails de l'utilisateur ou None en cas d'erreur.
    """ 
    url=f"https://api.github.com/users/{login}"
    resp = requests.get(url, headers=HEADERS)
    check_rate_limit(resp) # Vérifie la limite de taux après la requête

    if resp.status_code == 200: 
        data = resp.json()
        return {
            "login": data.get("login"),
            "id" : data.get("id"),
            "avatar_url" : data.get("avatar_url"),
            "created_at" : data.get("created_at"),
            "bio" : data.get("bio")
        }
    else:
        print(f"[!] Erreur lors de la récupération de {login} ({resp.status_code})")
        return None

def extract_users(max_users=120):
    """
    Extrait les utilisateurs GitHub en utilisant la pagination.

    Récupère les utilisateurs par lots jusqu'à atteindre le nombre maximum spécifié.
    Pour chaque utilisateur, les détails sont récupérés et stockés dans un fichier JSON.

    Args:
        max_users (int): Le nombre maximum d'utilisateurs à extraire (par défaut 120).
    """
    since = 10367555  # ID de l'utilisateur à partir duquel commencer la récupération
    users = [] # Liste pour stocker les détails des utilisateurs

    while len(users) < max_users: 
        url = f"https://api.github.com/users?since={since}"
        resp = requests.get(url, headers=HEADERS)
        check_rate_limit(resp) # Vérifie la limite de taux après la requête

        if resp.status_code != 200:
            print(f"[!] Erreur HTTP {resp.status_code} sur {url}")
            time.sleep(5)  # Pause en cas d'erreur pour éviter de surcharger l'API
            continue

        batch = resp.json()  # Récupère le lot d'utilisateurs
        for user in batch: 
            details = fetch_user_details(user["login"]) # Récupère les détails de chaque utilisateur
            if details: 
                users.append(details)  # Ajoute les détails à la liste
            if len(users) >= max_users:
                break
        
        # Met à jour l'ID de l'utilisateur pour la prochaine requête
        since = batch[-1]["id"] if batch else since + 1 
        time.sleep(1) #pause légéres pour éviter les limites 

    # Écrit les détails des utilisateurs dans un fichier JSON
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)
    print(f"✅ {len(users)} utilisateurs enregistrés dans {OUTPUT_PATH}")

if __name__ == "__main__":
    # Configuration de l'analyseur d'arguments pour la ligne de commande
    parser = ArgumentParser()
    parser.add_argument("--max-users", type=int, default=120, help="Nombre d'utilisateurs à extraire")
    args = parser.parse_args()

    extract_users(args.max_users)