import os
import re

def corriger_lien(fichier):
    """Corrige les liens relatifs non fonctionnels dans un fichier markdown."""
    with open(fichier, 'r', encoding='utf-8') as f:
        contenu = f.read()

    # Liste des liens à corriger
    liens_a_corriger = [
        (r'..\.\./user/guides/canaux', r'../../user/guides/canaux.md'),
        (r'..\.\./dev/bot-api', r'../../dev/bot-api.md'),
        (r'..\.\./user/studio.md/stories-and-answers', r'../../user/studio.md/stories-and-answers.md'),
        (r'..\.\./securite', r'../securite.md'),
        (r'..\.\./supervision', r'supervision.md'),
        (r'..\.\./disponibilite', r'../disponibilite.md'),
        (r'..\.\./about/showcase', r'../../about/showcase.md'),
        (r'..\.\./guide/plateforme', r'../../guide/plateforme.md'),
        (r'..\.\./dev/bot-integre', r'../../dev/bot-integre.md')
    ]
    
    liens_modifies = 0
    
    # Applique les corrections aux liens
    for old_link, new_link in liens_a_corriger:
        if old_link in contenu:
            print(f"Correction trouvée dans {fichier}: {old_link} -> {new_link}")
            contenu = contenu.replace(old_link, new_link)
            liens_modifies += 1

    # Si des liens ont été modifiés, réécrit le fichier
    if liens_modifies > 0:
        with open(fichier, 'w', encoding='utf-8') as f:
            f.write(contenu)

    return liens_modifies

def parcourir_repertoire(repertoire):
    """Parcourt tous les fichiers markdown et corrige les liens."""
    fichiers_corriges = 0
    for root, dirs, files in os.walk(repertoire):
        for fichier in files:
            if fichier.endswith('.md'):
                chemin_fichier = os.path.join(root, fichier)
                fichiers_corriges += corriger_lien(chemin_fichier)
    
    return fichiers_corriges

# Chemin du répertoire contenant tes fichiers markdown
repertoire_markdown = '/home/Titouan.Perivier-Vigouroux/Documents/tock/docs'

fichiers_corriges = parcourir_repertoire(repertoire_markdown)

# Affichage du résultat
if fichiers_corriges > 0:
    print(f"Le programme a corrigé {fichiers_corriges} fichier(s).")
else:
    print("Aucun fichier n'a été corrigé.")
