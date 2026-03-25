def run(params: dict) -> str:
    """Generates the DNF command based on parameters."""
    action = params.get('run')
    package = params.get('package')
    
    if action == 'update':
        return "sudo -S dnf makecache"
    elif action == 'check-update':
        return "sudo -S dnf check-update || true"
    elif action == 'makecache':
        return "sudo -S dnf makecache"
    elif action == 'upgrade':
        return "sudo -S dnf upgrade -y"
    elif action in ['full-upgrade', 'distro-sync']:
        return "sudo -S dnf distro-sync -y"
    elif action == 'list':
        return f"dnf list {package}" if package else "dnf list"
    elif action == 'search':
        if not package:
            raise ValueError("'package' parameter is required for 'search' action.")
        return f"dnf search {package}"
    elif action in ['show', 'info']:
        if not package:
            raise ValueError("'package' parameter is required for 'show' action.")
        return f"dnf info {package}"
    elif action == 'reinstall':
        if not package:
            raise ValueError("'package' parameter is required for 'reinstall' action.")
        return f"sudo -S dnf reinstall -y {package}"
    elif action == 'install':
        if not package:
            raise ValueError("'package' parameter is required for 'install' action.")
        return f"sudo -S dnf install -y {package}"
    elif action == 'remove':
        if not package:
            raise ValueError("'package' parameter is required for 'remove' action.")
        return f"sudo -S dnf remove -y {package}"
    elif action == 'purge':
        if not package:
            raise ValueError("'package' parameter is required for 'purge' action.")
        return f"sudo -S dnf remove -y {package}"
    elif action == 'downgrade':
        if not package:
            raise ValueError("'package' parameter is required for 'downgrade' action.")
        return f"sudo -S dnf downgrade -y {package}"
    elif action == 'autoremove':
        return "sudo -S dnf autoremove -y"
    elif action == 'clean':
        return "sudo -S dnf clean all"
    elif action == 'autoclean':
        return "sudo -S dnf clean packages"
    else:
        raise ValueError(f"Unknown action '{action}' for dnf module.")