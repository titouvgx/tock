import os
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

def on_page_markdown(
    markdown: str, *, page: Page, config: MkDocsConfig, files: Files
):
    print(f"Hook exécuté sur la page : {page.file.name}")
    
    # Utiliser config['docs_dir'] pour récupérer la racine du dossier docs
    docs_dir = config['docs_dir']
    
    # Réduire d'un niveau pour accéder directement à la racine du dossier 'includes'
    includes_dir = os.path.join(docs_dir, '../includes')  # Dossier 'includes' situé à la racine
    chatbot_path = os.path.join(includes_dir, 'chatbot.md')  # Chemin absolu vers chatbot.md

    # Afficher le chemin pour vérification
    print(f"Chemin de 'chatbot.md' : {chatbot_path}")

    # Vérifier si le fichier chatbot.md existe
    if not os.path.exists(chatbot_path):
        print(f"⚠️ Fichier 'chatbot.md' introuvable à {chatbot_path}")
        return markdown  # Retourner le markdown inchangé si le fichier est introuvable

    # Lire le contenu de 'chatbot.md'
    with open(chatbot_path, 'r', encoding='utf-8') as f:
        chatbot_content = f.read()

    # Ajouter le contenu de chatbot.md à la fin du markdown de la page
    markdown += "\n\n" + chatbot_content  # Ajouter chatbot.md après le contenu de la page actuelle

    # Calculer la profondeur du fichier courant dans la hiérarchie des dossiers
    depth = len(page.file.url.split('/')) - 1
    path_to_docs_root = '../' * depth

    # Remplacer toutes les occurrences de {{PATH_TO_DOCS_ROOT}} par le chemin calculé
    markdown = markdown.replace('{{PATH_TO_DOCS_ROOT}}', path_to_docs_root)

    return markdown
