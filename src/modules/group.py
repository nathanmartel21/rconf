import base64
import json

def run(params: dict) -> str:
    """
    Generates a shell command string to execute group creation/modification logic.
    """
    name = params.get('name')
    if not name:
        raise ValueError("The 'name' parameter is required for rconf:group")

    action = params.get('action', 'create')
    gid = params.get('gid')
    system = params.get('system', False)

    python_script_template = """
import os, sys, subprocess, grp

name = {name!r}
action = {action!r}
gid = {gid!r}
system = {system!r}

try:
    try:
        group_info = grp.getgrnam(name)
        exists = True
    except KeyError:
        exists = False

    msg_parts = []

    if action == 'remove':
        if exists:
            subprocess.run(['groupdel', name], check=True)
            print(f"Group '{{name}}' was successfully removed.")
        else:
            print(f"Group '{{name}}' is already absent.")
        sys.exit(0)
    
    elif action == 'create':
        if not exists:
            cmd = ['groupadd']
            if system: cmd.append('-r')
            if gid is not None: cmd.extend(['-g', str(gid)])
            cmd.append(name)
            
            subprocess.run(cmd, check=True)
            msg_parts.append(f"Group '{{name}}' created.")
        else:
            needs_update = False
            cmd = ['groupmod']
            if gid is not None and group_info.gr_gid != int(gid):
                cmd.extend(['-g', str(gid)])
                needs_update = True
                
            if needs_update:
                cmd.append(name)
                subprocess.run(cmd, check=True)
                msg_parts.append(f"Group '{{name}}' updated.")
            else:
                msg_parts.append(f"Group '{{name}}' is up-to-date.")

        print(" ".join(msg_parts))
        sys.exit(0)

except subprocess.CalledProcessError as e:
    print(f"Command failed with exit code {{e.returncode}}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {{str(e)}}")
    sys.exit(1)
"""
    
    formatted_script = python_script_template.format(name=name, action=action, gid=gid, system=system)
    encoded_script = base64.b64encode(formatted_script.encode('utf-8')).decode('utf-8')
    command = f"sudo -S python3 -c \"import base64, sys; exec(base64.b64decode(sys.argv[1]).decode('utf-8'))\" \"{encoded_script}\""
    return command
