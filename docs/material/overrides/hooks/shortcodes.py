import os
import re
from datetime import datetime

# Dossier où se trouvent vos fichiers markdown
markdown_directory = './content'

# Fichier changelog
changelog_file = './changelog.md'

def extract_version_info(file_path):
    """
    Extrait les informations de version à partir des balises Markdown spécifiées.
    """
    version_info = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Recherche de la balise de version et date dans les fichiers markdown
        version_pattern = re.compile(r'<!-- version (\d+\.\d+\.\d+) - (\d{4}-\d{2}-\d{2}) -->')
        matches = version_pattern.findall(content)
        for match in matches:
            version, date = match
            version_info.append((version, date, file_path))
    return version_info

def update_changelog(new_version_info):
    """
    Met à jour le changelog avec les nouvelles informations de version.
    """
    if os.path.exists(changelog_file):
        with open(changelog_file, 'a', encoding='utf-8') as changelog:
            for version, date, file_path in new_version_info:
                changelog.write(f"## Version {version} - {date}\n")
                changelog.write(f"Fichier mis à jour : {file_path}\n")
                changelog.write("### Description\n\n")
                changelog.write("Modification(s) à ajouter...\n")
                changelog.write("\n---\n")
    else:
        with open(changelog_file, 'w', encoding='utf-8') as changelog:
            changelog.write("# Changelog\n")
            for version, date, file_path in new_version_info:
                changelog.write(f"## Version {version} - {date}\n")
                changelog.write(f"Fichier mis à jour : {file_path}\n")
                changelog.write("### Description\n\n")
                changelog.write("Modification(s) à ajouter...\n")
                changelog.write("\n---\n")

def process_markdown_files():
    """
    Parcourt tous les fichiers Markdown dans le répertoire spécifié et met à jour le changelog.
    """
    all_versions = []
    for root, dirs, files in os.walk(markdown_directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                version_info = extract_version_info(file_path)
                if version_info:
                    all_versions.extend(version_info)
    
    if all_versions:
        update_changelog(all_versions)
        print(f"Changelog mis à jour avec {len(all_versions)} nouvelle(s) version(s).")
    else:
        print("Aucune mise à jour de version trouvée.")

if __name__ == "__main__":
    process_markdown_files()
