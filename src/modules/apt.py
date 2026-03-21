# done 21/03/26

def run(params: dict) -> str:
    """Generates the APT command based on parameters."""
    action = params.get('run')
    package = params.get('package')
    
    if action == 'update':
        return "sudo -S apt-get update -y"
    elif action == 'upgrade':
        return "sudo -S apt-get upgrade -y"
    elif action == 'full-upgrade':
        return "sudo -S apt-get full-upgrade -y"
    elif action == 'list':
        return f"apt list {package}" if package else "apt list"
    elif action == 'search':
        if not package:
            raise ValueError("'package' parameter is required for 'search' action.")
        return f"apt search {package}"
    elif action == 'show':
        if not package:
            raise ValueError("'package' parameter is required for 'show' action.")
        return f"apt show {package}"
    elif action == 'reinstall':
        if not package:
            raise ValueError("'package' parameter is required for 'reinstall' action.")
        return f"sudo -S apt-get reinstall -y {package}"
    elif action == 'install':
        if not package:
            raise ValueError("'package' parameter is required for 'install' action.")
        return f"sudo -S apt-get install -y {package}"
    elif action == 'remove':
        if not package:
            raise ValueError("'package' parameter is required for 'remove' action.")
        return f"sudo -S apt-get remove -y {package}"
    elif action == 'purge':
        if not package:
            raise ValueError("'package' parameter is required for 'purge' action.")
        return f"sudo -S apt-get purge -y {package}"
    elif action == 'satisfy':
        if not package:
            raise ValueError("'package' parameter is required for 'satisfy' action.")
        return f"sudo -S apt-get satisfy -y {package}"
    elif action == 'edit-sources':
        return "sudo -S apt edit-sources"
    elif action == 'autoremove':
        return "sudo -S apt-get autoremove -y"
    elif action == 'clean':
        return "sudo -S apt-get clean"
    elif action == 'autoclean':
        return "sudo -S apt-get autoclean"
    else:
        raise ValueError(f"Unknown action '{action}' for apt module.")