def run(params: dict) -> str:
    """
    Generates the command to pause execution for a specific amount of time.
    """
    seconds = params.get('seconds')
    
    if seconds is None:
        raise ValueError("The 'seconds' parameter is required for the sleep module.")
        
    # We enforce integer conversion for safety
    return f"sleep {int(seconds)}"
