def run(params: dict) -> str:
    """Generates the YUM command based on parameters."""
    action = params.get('run')
    package = params.get('package')
    
    if action == 'update':
        return "sudo -S yum makecache"
    elif action == 'check-update':
        return "sudo -S yum check-update || true"
    elif action == 'makecache':
        return "sudo -S yum makecache"
    elif action == 'upgrade':
        return "sudo -S yum upgrade -y"
    elif action in ['full-upgrade', 'distro-sync']:
        return "sudo -S yum distro-sync -y"
    elif action == 'list':
        return f"yum list {package}" if package else "yum list"
    elif action == 'search':
        if not package:
            raise ValueError("'package' parameter is required for 'search' action.")
        return f"yum search {package}"
    elif action in ['show', 'info']:
        if not package:
            raise ValueError("'package' parameter is required for 'show' action.")
        return f"yum info {package}"
    elif action == 'reinstall':
        if not package:
            raise ValueError("'package' parameter is required for 'reinstall' action.")
        return f"sudo -S yum reinstall -y {package}"
    elif action == 'install':
        if not package:
            raise ValueError("'package' parameter is required for 'install' action.")
        return f"sudo -S yum install -y {package}"
    elif action == 'remove':
        if not package:
            raise ValueError("'package' parameter is required for 'remove' action.")
        return f"sudo -S yum remove -y {package}"
    elif action == 'purge':
        if not package:
            raise ValueError("'package' parameter is required for 'purge' action.")
        return f"sudo -S yum remove -y {package}"
    elif action == 'downgrade':
        if not package:
            raise ValueError("'package' parameter is required for 'downgrade' action.")
        return f"sudo -S yum downgrade -y {package}"
    elif action == 'autoremove':
        return "sudo -S yum autoremove -y"
    elif action == 'clean':
        return "sudo -S yum clean all"
    elif action == 'autoclean':
        return "sudo -S yum clean packages"
    else:
        raise ValueError(f"Unknown action '{action}' for yum module.")