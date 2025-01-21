import os
import shutil
from pathlib import Path
from mkdocs.plugins import BasePlugin

tock_apistatic = {
    "../../bot/connector-web/web-connector.html":"api/web-connector.html",
    "../../bot/connector-web/Swagger_TOCKWebConnector.yaml":"api/Swagger_TOCKWebConnector.yaml",
    "../../nlp/api/doc/src/main/doc/admin.html":"api/admin.html",
    "../../nlp/api/doc/src/main/doc/admin.yaml":"api/admin.yaml",
    "../../nlp/api/doc/src/main/doc/index.html":"api/index.html",
    "../../nlp/api/doc/src/main/doc/nlp.yaml":"api/nlp.yaml"

    
}

def on_pre_build(config):
    # Define the mapping of source to destination (relative to the docs folder)
    docs_dir = Path(config['docs_dir'])
    
    # Get the `docs_dir` path from the MkDocs configuration
    global tock_apistatic

    for source, relative_dest in tock_apistatic.items():
        # Construct the full destination path
        destination = docs_dir/relative_dest
        source = docs_dir/source
        # Ensure the destination directory exists
        destination.parent.mkdir(exist_ok=True)

        # Copy the file from source to destination
        try:
            print('///////////////////////////////////////////////////////////')
            print(f"Debug {source} to {destination}")
            shutil.copy(source, destination)
            print(f"Copied {source} to {destination}")
        except FileNotFoundError:
            print(f"Error: Source file {source} not found.")
        except Exception as e:
            print(f"Error copying {source} to {destination}: {e}")
                

