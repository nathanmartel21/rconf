import base64
import json

def run(params: dict) -> str:
    """
    Generates a shell command string to execute user creation/modification logic.
    """
    name = params.get('name')
    if not name:
        raise ValueError("The 'name' parameter is required for rconf:user")

    action = params.get('action', 'create')
    password = params.get('password')
    groups = params.get('groups')
    append_groups = params.get('append', False)
    shell = params.get('shell')
    home = params.get('home')
    create_home = params.get('create_home', True)
    system = params.get('system', False)

    if isinstance(groups, list):
        groups = ",".join(groups)

    python_script_template = """
import os, sys, subprocess, pwd

name = {name!r}
action = {action!r}
password = {password!r}
groups = {groups!r}
append_groups = {append_groups!r}
shell = {shell!r}
home = {home!r}
create_home = {create_home!r}
system = {system!r}

try:
    try:
        user_info = pwd.getpwnam(name)
        exists = True
    except KeyError:
        exists = False

    msg_parts = []

    if action == 'remove':
        if exists:
            subprocess.run(['userdel', '-r', name], check=True)
            print(f"User '{{name}}' was successfully removed.")
        else:
            print(f"User '{{name}}' is already absent.")
        sys.exit(0)
    
    elif action == 'create':
        if not exists:
            cmd = ['useradd']
            if create_home: cmd.append('-m')
            else: cmd.append('-M')
            if system: cmd.append('-r')
            if shell: cmd.extend(['-s', shell])
            if home: cmd.extend(['-d', home])
            if groups: cmd.extend(['-G', groups])
            cmd.append(name)
            
            subprocess.run(cmd, check=True)
            msg_parts.append(f"User '{{name}}' created.")
        else:
            cmd = ['usermod']
            needs_update = False
            if shell and user_info.pw_shell != shell:
                cmd.extend(['-s', shell])
                needs_update = True
            if home and user_info.pw_dir != home:
                cmd.extend(['-d', home])
                needs_update = True
            if groups:
                if append_groups: cmd.append('-a')
                cmd.extend(['-G', groups])
                needs_update = True
                
            if needs_update:
                cmd.append(name)
                subprocess.run(cmd, check=True)
                msg_parts.append(f"User '{{name}}' updated.")
            else:
                msg_parts.append(f"User '{{name}}' is up-to-date.")

        if password:
            proc = subprocess.Popen(['chpasswd'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate(input=f"{{name}}:{{password}}".encode())
            if proc.returncode != 0:
                print(f"Failed to set password: {{err.decode()}}")
                sys.exit(1)
            msg_parts.append("Password configured.")

        print(" ".join(msg_parts))
        sys.exit(0)

except subprocess.CalledProcessError as e:
    print(f"Command failed with exit code {{e.returncode}}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {{str(e)}}")
    sys.exit(1)
"""
    
    formatted_script = python_script_template.format(
        name=name, action=action, password=password, groups=groups, 
        append_groups=append_groups, shell=shell, home=home, create_home=create_home, system=system
    )
    encoded_script = base64.b64encode(formatted_script.encode('utf-8')).decode('utf-8')
    command = f"sudo -S python3 -c \"import base64, sys; exec(base64.b64decode(sys.argv[1]).decode('utf-8'))\" \"{encoded_script}\""
    return command
