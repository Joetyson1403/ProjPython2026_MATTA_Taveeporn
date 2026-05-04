# Projet mindmaps : prototype d'affichage de mindmap en radial et forum 
# Taveeporn Matta SI-CA1 (projet Python) - 2025-2026
# 04 mai 2026
# model.py : définition des fonctions pour interagir avec la base de données

import mysql.connector
import bcrypt
from utils.config import get_db_config

# Fonction pour obtenir une connexion à la base de données
def get_connection(db_mode="local"):
    cfg = get_db_config(db_mode)
    return mysql.connector.connect(
        host=cfg["host"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        port=cfg["port"]
    )

# renvoie le résultat d'une requête SQL en mode dictionnaire
def fetch_all(sql_query, params=None, db_mode="local"):
    db = get_connection(db_mode)
    cursor = db.cursor(dictionary=True)
    if params:
        cursor.execute(sql_query, params)
    else:
        cursor.execute(sql_query)
    rows = cursor.fetchall()
    db.close()
    return rows


# renvoie la liste des maps (sans les nodes) pour l'affichage de la page d'accueil
def get_maps(db_mode):
    return fetch_all("select id, title, author_id from maps", None, db_mode)


# renvoie la liste de tous les nodes d'un map (avec le pseudo de l'auteur et sa couleur)
def get_nodes_for_map(map_id, db_mode):
    return fetch_all("select nodes.id, parent_id, author_id, text, nodes.level,users.color " \
    "from nodes inner join users on nodes.author_id = users.id " \
    "where map_id=%s", (map_id,), db_mode)

# renvoie la liste des utilisateurs (sans hash)
def get_users(db_mode):
    return fetch_all("select id, pseudo, level from users", None, db_mode)

# renvoie la liste de tous les nodes (données partielles)
def get_all_nodes(db_mode):
    return fetch_all("select map_id, parent_id, author_id, text, level from nodes", None, db_mode)

# fonctions pour insérer, mettre à jour et supprimer des maps et des nodes
# fonction pour insérer un node (retourne l'id du node créé)

# fonction pour vérifier les identifiants de connexion d'un utilisateur (retourne les infos de l'utilisateur si ok, sinon None)
def check_login(pseudo, password, db_mode="local"):
    db = get_connection(db_mode)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, pseudo, hash, level FROM users WHERE pseudo=%s", (pseudo,))
    row = cursor.fetchone()
    db.close()
    if not row:
        return None
    stored = row["hash"]
    if isinstance(stored, str):
        stored = stored.encode()
    # Vérifier le mot de passe avec bcrypt
    if bcrypt.checkpw(password.encode(), stored):
        return row
    return None

# Fonction pour enregistrer un nouvel utilisateur
# Retourne True si succès, lève ValueError si le pseudo est déjà pris
def register_user(pseudo, password, color, db_mode="local"):
    db = get_connection(db_mode)
    cursor = db.cursor(dictionary=True)

    # Vérifier si le pseudo est déjà utilisé
    cursor.execute("SELECT id FROM users WHERE pseudo=%s", (pseudo,))
    if cursor.fetchone():
        db.close()
        raise ValueError(f"Le pseudo '{pseudo}' est déjà pris.")

    # Hasher le mot de passe avec bcrypt
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Insérer le nouvel utilisateur (level=1 par défaut = utilisateur standard)
    cursor.execute(
        "INSERT INTO users (pseudo, hash, color, level) VALUES (%s, %s, %s, %s)",
        (pseudo, hashed, color, 1)
    )
    db.commit()
    new_id = cursor.lastrowid
    db.close()
    return new_id  # retourne l'id du nouvel utilisateur créé
