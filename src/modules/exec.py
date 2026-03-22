def run(params: dict) -> str:
    """Generates the command to execute arbitrary shell commands."""
    command = params.get('run')
    chdir = params.get('chdir')
    creates = params.get('creates')
    removes = params.get('removes')
    
    if not command:
        raise ValueError("'run' parameter is required for exec module.")
        
    cmds = []
    
    if creates:
        cmds.append(f"[ -e \"{creates}\" ] && exit 0")
        
    if removes:
        cmds.append(f"[ ! -e \"{removes}\" ] && exit 0")
        
    if chdir:
        cmds.append(f"cd \"{chdir}\"")
        
    cmds.append(command)
    full_command = " ; ".join(cmds)
    
    escaped_command = full_command.replace("'", "'\\''")
    return f"sudo -S bash -c '{escaped_command}'"