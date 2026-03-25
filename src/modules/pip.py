def run(params: dict) -> str:
    """Generates the PIP command based on parameters."""
    action = params.get('run')
    package = params.get('package')
    executable = params.get('executable', 'pip3')
    
    if action == 'install':
        if not package:
            raise ValueError("'package' parameter is required for 'install' action.")
        return f"{executable} install {package}"
    elif action in ['remove', 'uninstall']:
        if not package:
            raise ValueError("'package' parameter is required for 'remove' action.")
        return f"{executable} uninstall -y {package}"
    elif action == 'download':
        if not package:
            raise ValueError("'package' parameter is required for 'download' action.")
        return f"{executable} download {package}"
    elif action == 'list':
        return f"{executable} list"
    elif action == 'freeze':
        return f"{executable} freeze"
    elif action == 'show':
        if not package:
            raise ValueError("'package' parameter is required for 'show' action.")
        return f"{executable} show {package}"
    elif action == 'check':
        return f"{executable} check"
    elif action == 'clean':
        return f"{executable} cache purge"
    else:
        raise ValueError(f"Unknown action '{action}' for pip module.")