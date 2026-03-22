def run(params: dict) -> str:
    """Generates the command to manage systemd services."""
    name = params.get('name')
    status = params.get('status')
    enabled = params.get('enabled')
    
    if not name:
        raise ValueError("'name' parameter is required for daemon module.")
        
    cmds = []
    
    # Gestion du démarrage automatique (enable/disable)
    if enabled is not None:
        if str(enabled).lower() in ['true', 'yes', '1']:
            cmds.append(f"systemctl enable {name}")
        else:
            cmds.append(f"systemctl disable {name}")
            
    # Gestion du statut du service (start/stop/restart/reload)
    if status:
        if status in ['start', 'stop', 'restart', 'reload']:
            action = status.replace('ed', '')
            cmds.append(f"systemctl {action} {name}")
        else:
            raise ValueError(f"Invalid status '{status}' for daemon module. Allowed: start, stop, restart, reload.")
            
    if not cmds:
        # Si ni 'status' ni 'enabled' ne sont fournis, on ne fait rien
        return "true"
        
    bash_cmd = " && ".join(cmds)
    return f"sudo -S bash -c '{bash_cmd}'"