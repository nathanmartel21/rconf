def run(params: dict) -> str:
    """Generates the command to print a message (similar to debug)."""
    msg = params.get('msg')
    color = params.get('color')
    file_path = params.get('file')
    
    if msg is None:
        raise ValueError("'msg' parameter is required for print module.")
        
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'end': '\033[0m'
    }
    
    c_start = colors.get(color, "")
    c_end = colors['end'] if c_start else ""
    
    print(f"\n      => MSG: {c_start}{msg}{c_end}")
    
    if file_path:
        escaped_msg = str(msg).replace("'", "'\\''")
        return f"sudo -S bash -c \"echo '{escaped_msg}' >> {file_path}\""
    else:
        return "true"