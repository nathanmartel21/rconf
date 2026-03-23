def run(params: dict) -> str:
    """
    Generates the ping command to check connectivity to one or multiple hosts.
    """
    host = params.get('host')
    
    show_output = params.get('show_output', True)

    if not host:
        raise ValueError("'host' parameter is required for ping module.")
        
    if isinstance(host, list):
        hosts_str = " ".join(f"'{h}'" for h in host)
    else:
        hosts_str = f"'{host}'"
        
    return f"ret=0; for h in {hosts_str}; do echo \" \n--- $h ---\"; out=$(ping -c 1 \"$h\"); r=$?; echo \"$out\" | grep -E 'bytes from|packets transmitted'; [ $r -ne 0 ] && ret=$r; done; exit $ret"