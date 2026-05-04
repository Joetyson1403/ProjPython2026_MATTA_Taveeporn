# Projet mindmaps : prototype d'affichage de mindmap en radial et forum 
# JCY pour SI-CA1 (projet Python) - 2025-2026
# 13 avril 2026
# login.py : affichage de la fenêtre de connexion

import tkinter as tk
from tkinter import messagebox
from model import check_login
from utils.session import Session

def show_login(parent, db_mode="local" ):
    if Session.is_authenticated():
        messagebox.showinfo("Info", f"Déjà connecté en tant que {Session.pseudo}")
        return
    win = tk.Toplevel(parent)
    win.title("Login")

    # Empêcher d'interagir avec parent
    win.transient(parent)   # attache au parent
    win.grab_set()          # rend la fenêtre modale


    tk.Label(win, text="Pseudo").grid(row=0, column=0)
    tk.Label(win, text="Mot de passe").grid(row=1, column=0, padx=20, pady=20)

    entry_pseudo = tk.Entry(win)
    entry_pseudo.grid(row=0, column=1)

    entry_pass = tk.Entry(win, show="*")
    entry_pass.grid(row=1, column=1, padx=20, pady=20)

    def attempt_login(db_mode=db_mode):
        user = check_login(entry_pseudo.get(), entry_pass.get(), db_mode)

        if user:
            Session.login(user["pseudo"], user["level"], user["id"])
            # messagebox.showinfo("OK", f"Bienvenue {user['pseudo']} !")
            win.destroy()
        else:
            messagebox.showerror("Erreur", "Login incorrect")

    tk.Button(win, text="Se connecter", command=attempt_login).grid(row=2, column=0, columnspan=2)
    
    # Empêche d'accéder à la fenêtre principale tant que login est ouvert
    parent.wait_window(win)
