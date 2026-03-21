def run(params: dict) -> str:
    """Generates the DNF command based on parameters."""
    action = params.get('run')
    package = params.get('package')
    
    if action == 'update':
        return "sudo -S dnf check-update || true"
    elif action == 'makecache':
        return "sudo -S dnf makecache"
    elif action == 'upgrade':
        return "sudo -S dnf upgrade -y"
    elif action == 'install':
        if not package:
            raise ValueError("'package' parameter is required for 'install' action.")
        return f"sudo -S dnf install -y {package}"
    elif action == 'remove':
        if not package:
            raise ValueError("'package' parameter is required for 'remove' action.")
        return f"sudo -S dnf remove -y {package}"
    elif action == 'autoremove':
        return "sudo -S dnf autoremove -y"
    elif action == 'clean':
        return "sudo -S dnf clean all"
    elif action == 'reinstall':
        if not package:
            raise ValueError("'package' parameter is required for 'reinstall' action.")
        return f"sudo -S dnf reinstall -y {package}"
    elif action == 'downgrade':
        if not package:
            raise ValueError("'package' parameter is required for 'downgrade' action.")
        return f"sudo -S dnf downgrade -y {package}"
    else:
        raise ValueError(f"Unknown action '{action}' for dnf module.")