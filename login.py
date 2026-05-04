# Projet mindmaps : prototype d'affichage de mindmap en radial et forum 
# Taveeporn Matta SI-CA1 (projet Python) - 2025-2026
# 04 mai 2026
# login.py : fenêtres modales de connexion (login) et d'enregistrement (register)

import tkinter as tk
from tkinter import messagebox, colorchooser
from model import check_login, register_user
from utils.session import Session


def show_login(parent, db_mode="local"):
    """Affiche une fenêtre modale de connexion."""
    if Session.is_authenticated():
        messagebox.showinfo("Info", f"Déjà connecté en tant que {Session.pseudo}")
        return
    win = tk.Toplevel(parent)
    win.title("Login")

    # Fenêtre modale : empêche d'interagir avec la fenêtre principale
    win.transient(parent)
    win.grab_set()

    tk.Label(win, text="Pseudo").grid(row=0, column=0, padx=20, pady=10)
    tk.Label(win, text="Mot de passe").grid(row=1, column=0, padx=20, pady=10)

    entry_pseudo = tk.Entry(win)
    entry_pseudo.grid(row=0, column=1, padx=10)

    entry_pass = tk.Entry(win, show="*")
    entry_pass.grid(row=1, column=1, padx=10)

    def attempt_login(db_mode=db_mode):
        user = check_login(entry_pseudo.get(), entry_pass.get(), db_mode)
        if user:
            Session.login(user["pseudo"], user["level"], user["id"])
            win.destroy()
        else:
            messagebox.showerror("Erreur", "Pseudo ou mot de passe incorrect")

    tk.Button(win, text="Se connecter", command=attempt_login).grid(row=2, column=0, columnspan=2, pady=10)

    # Empêche d'accéder à la fenêtre principale tant que la fenêtre est ouverte
    parent.wait_window(win)


def show_register(parent, db_mode="local"):
    """Affiche une fenêtre modale d'enregistrement d'un nouvel utilisateur."""
    if Session.is_authenticated():
        messagebox.showinfo("Info", f"Déjà connecté en tant que {Session.pseudo}. Déconnectez-vous d'abord.")
        return

    win = tk.Toplevel(parent)
    win.title("S'enregistrer")
    win.transient(parent)
    win.grab_set()

    tk.Label(win, text="Pseudo").grid(row=0, column=0, padx=20, pady=8, sticky="e")
    tk.Label(win, text="Mot de passe").grid(row=1, column=0, padx=20, pady=8, sticky="e")
    tk.Label(win, text="Confirmer le mot de passe").grid(row=2, column=0, padx=20, pady=8, sticky="e")
    tk.Label(win, text="Couleur").grid(row=3, column=0, padx=20, pady=8, sticky="e")

    entry_pseudo = tk.Entry(win, width=25)
    entry_pseudo.grid(row=0, column=1, padx=10)

    entry_pass = tk.Entry(win, show="*", width=25)
    entry_pass.grid(row=1, column=1, padx=10)

    entry_pass2 = tk.Entry(win, show="*", width=25)
    entry_pass2.grid(row=2, column=1, padx=10)

    # Variable pour stocker la couleur choisie (par défaut bleu clair)
    chosen_color = tk.StringVar(value="#add8e6")

    # Aperçu visuel de la couleur sélectionnée
    color_preview = tk.Label(win, bg=chosen_color.get(), width=10, relief="solid")
    color_preview.grid(row=3, column=1, padx=10, sticky="w")

    def pick_color():
        """Ouvre le sélecteur de couleur tkinter."""
        result = colorchooser.askcolor(color=chosen_color.get(), title="Choisir une couleur")
        if result[1]:  # result = ((r,g,b), '#rrggbb') — on prend le code hex
            chosen_color.set(result[1])
            color_preview.config(bg=result[1])

    tk.Button(win, text="Choisir...", command=pick_color).grid(row=3, column=2, padx=5)

    def attempt_register(db_mode=db_mode):
        """Valide les champs et crée l'utilisateur en base."""
        pseudo = entry_pseudo.get().strip()
        pwd = entry_pass.get()
        pwd2 = entry_pass2.get()
        color = chosen_color.get()

        # Validations côté client
        if not pseudo:
            messagebox.showerror("Erreur", "Le pseudo ne peut pas être vide.")
            return
        if not pwd:
            messagebox.showerror("Erreur", "Le mot de passe ne peut pas être vide.")
            return
        if pwd != pwd2:
            messagebox.showerror("Erreur", "Les deux mots de passe ne correspondent pas.")
            return

        try:
            new_id = register_user(pseudo, pwd, color, db_mode)
            # Connexion automatique après l'enregistrement (level=1 par défaut)
            Session.login(pseudo, 1, new_id)
            messagebox.showinfo("Succès", f"Compte créé ! Bienvenue {pseudo} !")
            win.destroy()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            messagebox.showerror("Erreur base de données", str(e))

    tk.Button(win, text="S'enregistrer", command=attempt_register).grid(row=4, column=0, columnspan=3, pady=15)

    parent.wait_window(win)
