import os
import re

def verifier_et_corriger_lien(fichier, base_path):
    """Vérifie et corrige les liens dans le fichier markdown."""
    liens_non_fonctionnels = []  # Liste des liens non fonctionnels
    with open(fichier, 'r', encoding='utf-8') as f:
        contenu = f.read()

    pattern = r'\[([^\]]+)\]\(([^)]+)\)'  # Trouver tous les liens Markdown

    def corriger_lien(match):
        """Corrige le lien s'il est invalide et ajoute le lien à la liste si besoin."""
        texte, chemin = match.groups()
        chemin_complet = os.path.join(base_path, chemin)
        
        # Vérifie si le chemin existe
        if not os.path.exists(chemin_complet):
            # Recherche d'un fichier dans le même répertoire
            nouveau_chemin = os.path.join(os.path.dirname(fichier), chemin)
            if os.path.exists(nouveau_chemin):
                return f"[{texte}]({nouveau_chemin})"  # Le lien a été corrigé
            else:
                liens_non_fonctionnels.append((texte, chemin, chemin_complet))
                return match.group(0)  # Le lien reste inchangé
        return match.group(0)

    contenu_modifie = re.sub(pattern, corriger_lien, contenu)

    if contenu_modifie != contenu:
        with open(fichier, 'w', encoding='utf-8') as f:
            f.write(contenu_modifie)
        return 1, liens_non_fonctionnels  # Fichier modifié, et liste des liens non fonctionnels
    return 0, liens_non_fonctionnels  # Aucun changement

def verifier_et_corriger_nommage(fichier, base_path):
    """Vérifie et corrige les erreurs de nommage dans le fichier markdown."""
    erreurs_nommage = []
    with open(fichier, 'r', encoding='utf-8') as f:
        contenu = f.read()

    pattern = r'(\[([^\]]+)\]\()([^\)]+)(\))'  # Trouver les liens avec les noms dans les fichiers

    def corriger_nommage(match):
        """Corrige les erreurs de nommage dans les liens."""
        texte, texte_lien, chemin, parenthese_fermee = match.groups()
        chemin_complet = os.path.join(base_path, chemin)

        # Si le fichier n'existe pas et que le nom contient une erreur possible
        if not os.path.exists(chemin_complet) and '.' not in chemin:  # Fichier sans extension
            erreur_possible = chemin + '.md'  # Ajoute l'extension .md
            chemin_complet_possible = os.path.join(base_path, erreur_possible)
            if os.path.exists(chemin_complet_possible):
                erreurs_nommage.append((texte, chemin, erreur_possible))
                return f"{texte_lien}{erreur_possible}{parenthese_fermee}"
        return match.group(0)

    contenu_modifie = re.sub(pattern, corriger_nommage, contenu)

    if contenu_modifie != contenu:
        with open(fichier, 'w', encoding='utf-8') as f:
            f.write(contenu_modifie)
        return 1, erreurs_nommage  # Fichier modifié, et liste des erreurs de nommage
    return 0, erreurs_nommage  # Aucun changement

def parcourir_repertoire(repertoire):
    """Parcourt tous les fichiers Markdown et corrige les liens et les erreurs de nommage."""
    liens_non_fonctionnels = []  # Liste des liens non fonctionnels globaux
    erreurs_nommage = []  # Liste des erreurs de nommage
    for root, dirs, files in os.walk(repertoire):
        for fichier in files:
            if fichier.endswith('.md'):
                chemin_fichier = os.path.join(root, fichier)
                _, liens_non_fonctionnels_fichier = verifier_et_corriger_lien(chemin_fichier, root)
                _, erreurs_nommage_fichier = verifier_et_corriger_nommage(chemin_fichier, root)
                liens_non_fonctionnels.extend(liens_non_fonctionnels_fichier)
                erreurs_nommage.extend(erreurs_nommage_fichier)
    
    return liens_non_fonctionnels, erreurs_nommage

# Chemin du répertoire contenant tes fichiers markdown
repertoire_markdown = '/home/Titouan.Perivier-Vigouroux/Documents/tock/docs'

liens_non_fonctionnels, erreurs_nommage = parcourir_repertoire(repertoire_markdown)

# Afficher uniquement les liens non fonctionnels et leurs solutions
print(f"Total des liens non fonctionnels détectés : {len(liens_non_fonctionnels)}")
if liens_non_fonctionnels:
    print("\nLiens non fonctionnels détectés :")
    for texte, chemin, chemin_complet in liens_non_fonctionnels:
        print(f"- [{texte}]({chemin}) ne fonctionne pas. Recherche de solution : {chemin_complet}")

print(f"\nTotal des erreurs de nommage détectées : {len(erreurs_nommage)}")
if erreurs_nommage:
    print("\nErreurs de nommage détectées :")
    for texte, chemin, nouvelle_extension in erreurs_nommage:
        print(f"- [{texte}]({chemin}) n'a pas d'extension correcte. Solution suggérée : [{texte}]({nouvelle_extension})")
else:
    print("\nAucune erreur de lien ou de nommage trouvée.")
