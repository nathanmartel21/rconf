def run(params: dict) -> str:
    """Generates the command to remove a directory."""
    path = params.get('path')
    recursive = params.get('recursive', False)
    
    if not path:
        raise ValueError("'path' parameter is required for rmdir module.")
        
    if path in ['/', '/*']:
        raise ValueError("Security violation: Refusing to remove the root directory.")
        
    if recursive:
        return f"sudo -S rm -rf {path}"
    else:
        return f"sudo -S bash -c 'if [ -d \"{path}\" ]; then rmdir \"{path}\"; fi'"