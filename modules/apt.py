def run(params: dict) -> str:
    """Generates the APT command based on parameters."""
    action = params.get('run')
    package = params.get('package')
    
    if action == 'update':
        return "sudo -S apt-get update -y"
    elif action == 'install':
        if not package:
            raise ValueError("'package' parameter is required for 'install' action.")
        return f"sudo -S apt-get install -y {package}"
    elif action in ('remove', 'absent'):
        if not package:
            raise ValueError("'package' parameter is required for 'remove' action.")
        return f"sudo -S apt-get remove -y {package}"
    else:
        raise ValueError(f"Unknown action '{action}' for apt module.")