# Projet mindmaps : prototype d'affichage de mindmap en radial et forum 
# JCY pour SI-CA1 (projet Python) - 2025-2026
# 13 avril 2026
# tree_display.py : affichage d'un tableau de données dans un TreeView

import tkinter as tk
from tkinter import ttk
from tkinter import font

# C'est la fonction principale pour afficher un tableau de données dans un TreeView
# data doit être une liste de dictionnaires, où chaque dictionnaire représente une ligne et les clés    sont les noms des colonnes
# Exemple : data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
def display_array(frame, data):
    # nettoyer la frame
    for widget in frame.winfo_children():
        widget.destroy()

    # récupérer automatiquement les colonnes
    if not data or not isinstance(data, list) or not isinstance(data[0], dict):
        raise ValueError("data doit être une liste de dictionnaires non vide.")

    columns = list(data[0].keys())

    # --- FRAME POUR LE TREEVIEW + SCROLLBARS ---
    container = ttk.Frame(frame)
    container.pack(fill="both", expand=True)

    # Scrollbars
    vsb = ttk.Scrollbar(container, orient="vertical")
    hsb = ttk.Scrollbar(container, orient="horizontal")

    tree = ttk.Treeview(
        container,
        columns=columns,
        show="headings",
        yscrollcommand=vsb.set,
        xscrollcommand=hsb.set
    )

    # Configurer le style pour le TreeView de gauche (tables)
    style = ttk.Style()
    style.configure("Left.Treeview", font=("Arial", 10), rowheight=20)
    tree.configure(style="Left.Treeview")

    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)

    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    # colonnes + largeur automatique
    for col in columns:
        tree.heading(col, text=col)
        tree.heading(col, anchor="w") # alignement à gauche
        tree.column(col, width=tkFontMeasure(tree, col, data), stretch=True)

    # insérer données
    insert_rows(tree, data, columns)
    return tree


def insert_rows(tree, data, columns):
    # effacer existant
    for row in tree.get_children():
        tree.delete(row)

    for row_dict in data:
        values = [row_dict[col] for col in columns]
        tree.insert("", tk.END, values=values)


def tkFontMeasure(tree, col, data):
    """ Calcule automatiquement la largeur idéale d’une colonne """
    font = tk.font.nametofont("TkDefaultFont")

    # largeur selon l’en-tête
    width = font.measure(col)

    # largeur selon les données
    for row in data:
        cell_value = str(row[col])
        width = max(width, font.measure(cell_value))

    # un petit padding et limite à 200px
    return min(width + 20, 200)