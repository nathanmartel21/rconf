def run(params: dict) -> str:
    """Generates the command to remove a directory."""
    path = params.get('path')
    recursive = params.get('recursive', False)
    
    if not path:
        raise ValueError("'path' parameter is required for rmdir module.")
        
    # Protection basique pour éviter de supprimer accidentellement la racine du système
    if path in ['/', '/*']:
        raise ValueError("Security violation: Refusing to remove the root directory.")
        
    if recursive:
        # 'rm -rf' est naturellement idempotent (ne renvoie pas d'erreur si le dossier n'existe pas)
        return f"sudo -S rm -rf {path}"
    else:
        # 'rmdir' classique échoue si le dossier n'existe plus.
        # On ajoute une vérification en bash pour le rendre idempotent (succès s'il est déjà supprimé).
        return f"sudo -S bash -c 'if [ -d \"{path}\" ]; then rmdir \"{path}\"; fi'"