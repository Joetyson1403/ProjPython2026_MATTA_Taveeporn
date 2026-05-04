# Affichage radial d'un mindmap (vue en étoile)
# Taveeporn Matta SI-CA1 (projet Python) - 2025-2026
# 04 mai 2026
# radial_display.py : dessine un mindmap sous forme radiale (arbre centré) sur un Canvas tkinter.
#
# Principe de l'algorithme :
#   1. On identifie la racine (nœud sans parent) et on construit un dictionnaire enfants[id] -> [enfants].
#   2. On place la racine exactement au centre du Canvas.
#   3. Pour chaque niveau de profondeur (depth), les nœuds enfants sont placés à une distance
#      fixe (RADIUS_STEP * depth) du centre, sur un arc de cercle.
#   4. Le cercle complet (2π radians = 360°) est divisé en secteurs angulaires proportionnels
#      au nombre de "feuilles" (descendants sans enfants) de chaque branche.
#      Cela garantit que les branches larges ont plus d'espace que les branches étroites.
#   5. Chaque enfant est positionné en coordonnées polaires puis converties en cartésiennes :
#         x = centre_x + rayon * cos(angle_milieu)
#         y = centre_y + rayon * sin(angle_milieu)
#   6. On dessine d'abord les lignes de connexion (parent -> enfant), puis les bulles par-dessus.

import tkinter as tk
import tkinter.ttk as ttk
import math

# -------- Constantes de mise en page --------
CHARS_PER_LINE = 15   # Nombre de caractères estimés par ligne dans une bulle
LINE_HEIGHT = 13      # Hauteur (px) d'une ligne de texte dans la bulle
NODE_WIDTH = 55       # Demi-largeur fixe de chaque bulle (ovale)
H_PADDING = 8         # Marge verticale supplémentaire dans la bulle
RADIUS_STEP = 160     # Distance (px) entre deux cercles concentriques consécutifs

# -------- Fonctions utilitaires --------

def node_bubble_height(text):
    """
    Calcule la demi-hauteur (en px) de la bulle selon le nombre de lignes nécessaires.
    Plus le texte est long, plus la bulle sera haute pour contenir le texte complet.
    """
    n_lines = math.ceil(len(text) / CHARS_PER_LINE)
    return max(18, n_lines * LINE_HEIGHT + H_PADDING)


# -------- Fonction principale --------

def display_mindmap_radial(frame, nodes):
    """
    Affiche un mindmap en mode radial (étoile) dans le frame tkinter donné.
    nodes : liste de dictionnaires avec les clés 'id', 'parent_id', 'text', 'color'.
    """

    # --- Création du conteneur avec Canvas et Scrollbars ---
    # Le canvas est plus grand que la fenêtre pour permettre le scroll
    container = tk.Frame(frame)
    container.pack(fill='both', expand=True)

    canvas = tk.Canvas(container, bg='white')
    vsb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    hsb = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)

    canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)

    # Taille virtuelle du canvas (plus grande que la fenêtre pour pouvoir scroller)
    canvas_width = 2400
    canvas_height = 2400
    canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))

    if not nodes:
        return

    # --- Étape 1 : Construction de la hiérarchie ---
    # children_map[id] = liste des nœuds enfants directs
    children_map = {}
    root_node = None

    for node in nodes:
        children_map[node['id']] = []
        # Le nœud racine est celui qui n'a pas de parent (parent_id None ou 0)
        if node['parent_id'] is None or node['parent_id'] == 0:
            root_node = node

    # On remplit le dictionnaire enfants en parcourant tous les nœuds
    for node in nodes:
        pid = node['parent_id']
        if pid is not None and pid != 0 and pid in children_map:
            children_map[pid].append(node)

    if not root_node:
        return  # Aucun nœud racine trouvé, rien à afficher

    # --- Étape 2 : Comptage des feuilles (pour la répartition angulaire) ---
    def count_leaves(n):
        """
        Retourne le nombre de feuilles (nœuds sans enfants) dans le sous-arbre de n.
        Si n est lui-même une feuille, retourne 1.
        Ce nombre sert à allouer un secteur angulaire proportionnel à chaque branche :
        une branche avec beaucoup de feuilles aura plus d'espace qu'une branche simple.
        """
        children = children_map[n['id']]
        if not children:
            return 1  # C'est une feuille
        return sum(count_leaves(c) for c in children)

    # La racine est placée au centre exact du Canvas
    center_x = canvas_width / 2
    center_y = canvas_height / 2

    # Listes pour stocker les éléments à dessiner (lignes et nœuds séparément)
    lines_to_draw = []   # Liste de tuples (x1, y1, x2, y2)
    nodes_to_draw = []   # Liste de tuples (node, x, y)

    # --- Étape 3 : Calcul récursif des positions ---
    def calculate_positions(node, x, y, start_angle, end_angle, depth):
        """
        Place récursivement les nœuds sur le canvas en coordonnées polaires.
        - (x, y) : position du nœud parent (en pixels cartésiens)
        - start_angle / end_angle : secteur angulaire (en radians) alloué à ce nœud
        - depth : profondeur dans l'arbre (rayon = depth * RADIUS_STEP)
        """
        nodes_to_draw.append((node, x, y))
        children = children_map[node['id']]
        if not children:
            return  # Feuille : pas d'enfants à positionner

        # Garantir un secteur angulaire minimal par enfant
        # pour éviter les chevauchements sur les branches très ramifiées
        n_children = len(children)
        min_angle_per_child = 0.30  # ≈ 17 degrés minimum par enfant
        total_min = n_children * min_angle_per_child
        available_angle = end_angle - start_angle
        if available_angle < total_min:
            # On élargit symétriquement autour du milieu du secteur
            mid = (start_angle + end_angle) / 2
            start_angle = mid - total_min / 2
            end_angle = mid + total_min / 2

        # Répartition proportionnelle : chaque enfant reçoit un secteur
        # proportionnel au nombre de feuilles de sa branche
        total_leaves = sum(count_leaves(c) for c in children)
        current_angle = start_angle

        for child in children:
            leaves = count_leaves(child)
            # Portion d'angle allouée à cet enfant
            slice_angle = (leaves / total_leaves) * (end_angle - start_angle)
            child_end_angle = current_angle + slice_angle

            # L'enfant est placé au milieu de son secteur angulaire
            mid_angle = current_angle + slice_angle / 2

            # Conversion polaires -> cartésiennes
            # rayon = depth * RADIUS_STEP (distance au centre)
            child_radius = depth * RADIUS_STEP
            child_x = center_x + child_radius * math.cos(mid_angle)
            child_y = center_y + child_radius * math.sin(mid_angle)

            # On mémorise la ligne parent -> enfant et on continue récursivement
            lines_to_draw.append((x, y, child_x, child_y))
            calculate_positions(child, child_x, child_y, current_angle, child_end_angle, depth + 1)

            current_angle = child_end_angle  # On avance dans le secteur angulaire

    # Lancer le calcul depuis la racine avec 360° (0 à 2π)
    calculate_positions(root_node, center_x, center_y, 0, 2 * math.pi, 1)

    # --- Étape 4 : Dessin sur le Canvas ---

    # On dessine d'abord les lignes (au fond) pour qu'elles passent sous les bulles
    for x1, y1, x2, y2 in lines_to_draw:
        canvas.create_line(x1, y1, x2, y2, fill="#aaaaaa", width=1)

    # Puis on dessine les bulles (ovales + texte) par-dessus les lignes
    for node, x, y in nodes_to_draw:
        color = node.get('color', 'lightblue')
        if not color:
            color = 'lightblue'  # couleur par défaut si aucune couleur n'est définie

        text = node['text']
        # Hauteur de la bulle adaptée à la longueur du texte
        h = node_bubble_height(text)

        # Dessin de l'ovale (largeur fixe, hauteur variable selon le texte)
        canvas.create_oval(
            x - NODE_WIDTH, y - h,
            x + NODE_WIDTH, y + h,
            fill=color, outline="black"
        )
        # Texte avec retour à la ligne automatique (wraplength = width en pixels)
        canvas.create_text(
            x, y,
            text=text,
            font=("Arial", 9, "bold"),
            justify="center",
            width=NODE_WIDTH * 2 - 10  # largeur max avant retour à la ligne
        )

    # --- Centrage automatique sur la racine au démarrage ---
    # L'événement <Map> est déclenché quand le canvas devient visible
    def on_map(e):
        canvas.xview_moveto((center_x - canvas.winfo_width() / 2) / canvas_width)
        canvas.yview_moveto((center_y - canvas.winfo_height() / 2) / canvas_height)
        canvas.unbind("<Map>")  # Ne s'exécute qu'une seule fois

    canvas.bind("<Map>", on_map)
