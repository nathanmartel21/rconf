import argparse
import sys
import yaml
import paramiko
import os
import importlib

class Colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'

AVAILABLE_MODULES = {}
_modules_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules')
if os.path.exists(_modules_dir):
    for _filename in os.listdir(_modules_dir):
        if _filename.endswith('.py') and not _filename.startswith('__'):
            _module_name = _filename[:-3]
            try:
                AVAILABLE_MODULES[f'rconf:{_module_name}'] = importlib.import_module(f'modules.{_module_name}')
            except Exception as e:
                print(f"{Colors.WARNING}Warning: Failed to load module {_module_name}: {e}{Colors.ENDC}")

def execute_task(task_name: str, module_name: str, params: dict, ssh_client, password: str = None):
    """Routes the task to the appropriate Python module and executes it via SSH."""
    print(f"    * Executing [{module_name}] : {task_name}... ", end="", flush=True)
    
    # Récupère l'option show_output de façon sécurisée
    show_output = params.get('show_output', False) if isinstance(params, dict) else False

    if module_name in AVAILABLE_MODULES:
        target_module = AVAILABLE_MODULES[module_name]
        try:
            if not hasattr(target_module, 'run'):
                raise ValueError(f"Target module '{module_name}' is improperly configured (missing 'run' function).")
                
            command = target_module.run(params)
            
            stdin, stdout, stderr = ssh_client.exec_command(command)
            
            # If we have a password, send it to standard input (stdin) in case 'sudo -S' prompts for it
            if password:
                stdin.write(password + '\n')
                stdin.flush()
            
            # Wait for execution to finish to retrieve the exit code
            exit_status = stdout.channel.recv_exit_status()
            out = stdout.read().decode('utf-8').strip()
            err = stderr.read().decode('utf-8').strip()
            
            if exit_status == 0:
                print(f"{Colors.OKGREEN}OK{Colors.ENDC}")
                if show_output and out:
                    for line in out.splitlines():
                        print(f"        | {line}{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}FAILED (Exit: {exit_status}){Colors.ENDC}")
                if show_output and out:
                    print(f"{Colors.WARNING}      Stdout:\n{out}{Colors.ENDC}")
                if err:
                    print(f"{Colors.WARNING}      Stderr: {err}{Colors.ENDC}")
                    
        except ValueError as e:
            print(f"{Colors.FAIL}MODULE ERROR{Colors.ENDC}")
            print(f"{Colors.WARNING}      Details: {e}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}UNKNOWN MODULE{Colors.ENDC}")
        print(f"{Colors.WARNING}      Details: Module '{module_name}' is not recognized by rconf.{Colors.ENDC}")

def apply_configuration(playbook_path: str, inventory_path: str):
    """Main entry point to apply a configuration."""
    
    try:
        with open(inventory_path, 'r') as file:
            inventory = yaml.safe_load(file)
        with open(playbook_path, 'r') as file:
            playbook = yaml.safe_load(file)
    except Exception as e:
        print(f"{Colors.FAIL}ERROR: Failed to read configuration files: {e}{Colors.ENDC}")
        return

    if not inventory:
        print(f"{Colors.FAIL}ERROR: Inventory file '{inventory_path}' is empty or invalid.{Colors.ENDC}")
        return

    if not playbook:
        print(f"{Colors.FAIL}ERROR: Playbook file '{playbook_path}' is empty or invalid.{Colors.ENDC}")
        return

    targets = playbook.get('targets')
    
    target_group = inventory.get(targets)
    if not target_group or 'hosts' not in target_group:
        print(f"{Colors.FAIL}ERROR: Targets '{targets}' not found in the inventory.{Colors.ENDC}")
        return
        
    print(f"{Colors.CYAN}=============================================================={Colors.ENDC}")
    print(f"{Colors.CYAN} rconf - Applying Playbook: {playbook_path}{Colors.ENDC}")
    print(f"{Colors.CYAN}=============================================================={Colors.ENDC}")
        
    for host in target_group['hosts']:
        ip = host.get('ip')
        user = host.get('user')
        port = host.get('port', 22)
        password = host.get('password')
        
        print(f"\n{Colors.HEADER}▶ Target Host: {ip} (User: {user}, Port: {port}){Colors.ENDC}")
        print(f"{Colors.HEADER}--------------------------------------------------------------{Colors.ENDC}")
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            client.connect(hostname=ip, port=port, username=user, password=password)
            
            for job in playbook.get('jobs', []):
                task_name = job.get('name', 'Anonymous Job')
                for key, value in job.items():
                    if key != 'name':
                        execute_task(task_name, key, value, client, password)
                        
        except Exception as e:
            print(f"{Colors.FAIL}    ! Connection or execution error on {ip}: {e}{Colors.ENDC}")
        finally:
            client.close()
            
    print(f"\n{Colors.CYAN}=============================================================={Colors.ENDC}")
    print(f"{Colors.CYAN} rconf - Deployment completed.{Colors.ENDC}")
    print(f"{Colors.CYAN}=============================================================={Colors.ENDC}\n")

def main():
    parser = argparse.ArgumentParser(description="rconf - A minimalist IaC tool inspired by Ansible.")
    
    parser.add_argument('playbook', help="The configuration file describing the desired state (e.g., playbooks/playbook.yml)")
    parser.add_argument('-i', '--inventory', default="inventory/inventory.yml", help="The server inventory file")
    
    args = parser.parse_args()
    
    apply_configuration(args.playbook, args.inventory)

if __name__ == "__main__":
    main()