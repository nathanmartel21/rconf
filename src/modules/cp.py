def run(params: dict) -> str:
    """Generates the command to copy a file or directory on the remote system."""
    src = params.get('src')
    dest = params.get('dest')
    recursive = params.get('recursive', False)
    
    if not src or not dest:
        raise ValueError("'src' and 'dest' parameters are required for cp module.")
        
    if recursive:
        return f"sudo -S cp -rf {src} {dest}"
    else:
        return f"sudo -S cp -f {src} {dest}"