def run(params: dict) -> str:
    """Generates the command to reboot the system."""
    delay = params.get('delay', 'now')
    msg = params.get('msg')
    
    if isinstance(delay, int) and delay > 0:
        time_arg = f"+{delay}"
    elif str(delay) == '0':
        time_arg = "now"
    else:
        time_arg = str(delay)
        
    cmd = f"sudo -S shutdown -r {time_arg}"
    
    if msg:
        escaped_msg = str(msg).replace("'", "'\\''")
        cmd += f" '{escaped_msg}'"
        
    return cmd