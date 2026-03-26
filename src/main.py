import argparse
import sys
import yaml
import paramiko
import os
import importlib
import re
import json
import base64

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

def execute_task(task_name: str, module_name: str, params: dict, ssh_client, password: str = None, host_vars: dict = None):
    """Routes the task to the appropriate Python module and executes it via SSH."""
    print(f"    * Executing [{module_name}] : {task_name}... ", end="", flush=True)
    
    if host_vars is None:
        host_vars = {}

    def inject_vars(data):
        if isinstance(data, str):
            for k, v in host_vars.items():
                data = data.replace(f"<< {k} >>", str(v)).replace(f"<<{k}>>", str(v))
            return data
        elif isinstance(data, dict):
            return {k: inject_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [inject_vars(v) for v in data]
        return data

    if isinstance(params, dict):
        params = inject_vars(params)

    show_output = params.get('show_output', False) if isinstance(params, dict) else False
    save_var = params.get('save') if isinstance(params, dict) else None

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
                if save_var:
                    host_vars[save_var] = f"\n{out}" if out else ""
                if show_output and out:
                    for line in out.splitlines():
                        print(f"        | {line}{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}FAILED (Exit: {exit_status}){Colors.ENDC}")
                if not params.get('ignore_failure', False): sys.exit(1)
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
        key_file = host.get('key_file')
        
        if key_file:
            key_file = os.path.expanduser(key_file)
        
        host_vars = {}
        
        print(f"\n{Colors.HEADER}▶ Target Host: {ip} (User: {user}, Port: {port}){Colors.ENDC}")
        print(f"{Colors.HEADER}--------------------------------------------------------------{Colors.ENDC}")
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            client.connect(hostname=ip, port=port, username=user, password=password, key_filename=key_file)
            
            if playbook.get('inspect_system', True):
                print(f"    * Inspecting system environment... ", end="", flush=True)
                sys_info_script = """
import platform, json, socket, os
try:
    import pwd
except ImportError:
    pwd = None
info = {}
info['sys_hostname'] = socket.gethostname()
info['sys_arch'] = platform.machine()
info['sys_platform'] = platform.system()
try:
    info['sys_user'] = os.getlogin()
except Exception:
    try:
        info['sys_user'] = os.environ.get('USER') or (pwd.getpwuid(os.getuid())[0] if pwd else 'unknown')
    except Exception:
        info['sys_user'] = 'unknown'
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    info['sys_ipv4'] = s.getsockname()[0]
    s.close()
except Exception:
    info['sys_ipv4'] = '127.0.0.1'
info['sys_distro'] = 'unknown'
info['sys_distro_version'] = 'unknown'
info['sys_distro_like'] = 'unknown'
try:
    with open('/etc/os-release') as f:
        for line in f:
            line = line.strip()
            if line.startswith('ID='):
                info['sys_distro'] = line.split('=', 1)[1].strip('"').strip("'")
            elif line.startswith('VERSION_ID='):
                info['sys_distro_version'] = line.split('=', 1)[1].strip('"').strip("'")
            elif line.startswith('ID_LIKE='):
                info['sys_distro_like'] = line.split('=', 1)[1].strip('"').strip("'")
except Exception:
    pass
try:
    info['sys_cpu_cores'] = os.cpu_count() or 1
except Exception:
    info['sys_cpu_cores'] = 'unknown'
try:
    info['sys_swap_total_mb'] = 'unknown'
    info['sys_swap_free_mb'] = 'unknown'
    with open('/proc/meminfo') as f:
        for line in f:
            if line.startswith('MemTotal:'):
                info['sys_mem_total_mb'] = int(line.split()[1]) // 1024
            elif line.startswith('MemFree:'):
                info['sys_mem_free_mb'] = int(line.split()[1]) // 1024
            elif line.startswith('SwapTotal:'):
                info['sys_swap_total_mb'] = int(line.split()[1]) // 1024
            elif line.startswith('SwapFree:'):
                info['sys_swap_free_mb'] = int(line.split()[1]) // 1024
except Exception:
    info['sys_mem_total_mb'] = 'unknown'
    info['sys_mem_free_mb'] = 'unknown'
info['sys_kernel_version'] = platform.release()
try:
    with open('/proc/uptime') as f:
        info['sys_uptime_seconds'] = int(float(f.readline().split()[0]))
except Exception:
    info['sys_uptime_seconds'] = 'unknown'
try:
    load = os.getloadavg()
    info['sys_load_1m'], info['sys_load_5m'], info['sys_load_15m'] = load[0], load[1], load[2]
except Exception:
    info['sys_load_1m'], info['sys_load_5m'], info['sys_load_15m'] = 'unknown', 'unknown', 'unknown'
import time
try:
    with open('/etc/timezone') as f:
        info['sys_timezone'] = f.read().strip()
except Exception:
    info['sys_timezone'] = time.tzname[0]
try:
    import shutil
    st = shutil.disk_usage('/')
    info['sys_disk_total_gb'] = st.total // (1024**3)
    info['sys_disk_free_gb'] = st.free // (1024**3)
    info['sys_has_docker'] = bool(shutil.which('docker'))
    info['sys_has_systemd'] = bool(shutil.which('systemctl'))
except Exception:
    info['sys_disk_total_gb'] = 'unknown'
    info['sys_disk_free_gb'] = 'unknown'
    info['sys_has_docker'] = False
    info['sys_has_systemd'] = False
info['sys_python_version'] = platform.python_version()
print(json.dumps(info))
"""
                encoded_script = base64.b64encode(sys_info_script.encode('utf-8')).decode('utf-8')
                cmd = f"python3 -c \"import base64, sys; exec(base64.b64decode(sys.argv[1]).decode('utf-8'))\" \"{encoded_script}\""
                stdin, stdout, stderr = client.exec_command(cmd)
                exit_status = stdout.channel.recv_exit_status()
                out = stdout.read().decode('utf-8').strip()
                
                if exit_status == 0:
                    try:
                        sys_data = json.loads(out)
                        host_vars.update(sys_data)
                        print(f"{Colors.OKGREEN}OK{Colors.ENDC}")
                    except Exception as e:
                        print(f"{Colors.WARNING}FAILED (JSON Parse: {e}){Colors.ENDC}")
                else:
                    print(f"{Colors.WARNING}FAILED (Exit Code: {exit_status}){Colors.ENDC}")

            for job in playbook.get('jobs', []):
                base_task_name = job.get('name', 'Anonymous Job')
                
                raw_loop = job.get('foreach')
                if raw_loop is not None:
                    # Support loops over a saved variable from previous command
                    if isinstance(raw_loop, str) and raw_loop.strip().startswith("<<") and raw_loop.strip().endswith(">>"):
                        var_name = raw_loop.strip("<> ").strip()
                        loop_items = host_vars.get(var_name, [])
                        if isinstance(loop_items, str):
                            loop_items = [i.strip() for i in loop_items.split('\n') if i.strip()]
                    elif isinstance(raw_loop, list):
                        loop_items = raw_loop
                    else:
                        loop_items = [raw_loop]
                else:
                    loop_items = [None]
                    
                for item in loop_items:
                    # Inject value variable into host_vars context for this iteration
                    if raw_loop is not None:
                        host_vars['value'] = item
                        if isinstance(item, dict):
                            for k, v in item.items():
                                host_vars[f"value_{k}"] = v
                            task_name = f"{base_task_name} [value=dict]"
                        else:
                            task_name = f"{base_task_name} [value={item}]"
                    else:
                        task_name = base_task_name

                    raw_while = job.get('while')
                    retry_limit = job.get('retry_limit', 30)
                    while_iteration = 0
                    
                    while True:
                        host_vars['while_iteration'] = while_iteration
                        
                        if raw_while is not None:
                            eval_cond = raw_while
                            for k, v in host_vars.items():
                                safe_val = str(v).replace('\\', '\\\\').replace('\n', '\\n').replace('\r', '\\r').replace("'", "\\'")
                                eval_cond = eval_cond.replace(f"<< {k} >>", safe_val).replace(f"<<{k}>>", safe_val)
                            try:
                                if not bool(eval(eval_cond)):
                                    break
                            except Exception as e:
                                print(f"{Colors.WARNING}    * Stopping while loop [{task_name}] : Eval error on '{raw_while}' -> {e}{Colors.ENDC}")
                                break
                                
                            if while_iteration >= retry_limit:
                                print(f"{Colors.WARNING}    * While loop [{task_name}] reached max retries ({retry_limit}). Stopping.{Colors.ENDC}")
                                break
                                
                            current_task_name = f"{task_name} [while={while_iteration}]"
                        else:
                            current_task_name = task_name

                        condition = job.get('if')
                        condition_met = True
                        
                        if condition:
                            eval_cond = condition
                            for k, v in host_vars.items():
                                safe_val = str(v).replace('\\', '\\\\').replace('\n', '\\n').replace('\r', '\\r').replace("'", "\\'")
                                eval_cond = eval_cond.replace(f"<< {k} >>", safe_val).replace(f"<<{k}>>", safe_val)
                            try:
                                condition_met = bool(eval(eval_cond))
                            except Exception as e:
                                print(f"{Colors.WARNING}    * Skipping [{current_task_name}] : Eval error on '{condition}' -> {e}{Colors.ENDC}")
                                break

                        if condition_met:
                            for key, value in job.items():
                                if key not in ['name', 'if', 'elif', 'else', 'foreach', 'while', 'retry_limit']:
                                    execute_task(current_task_name, key, value, client, password, host_vars)
                        else:
                            elif_executed = False
                            elif_blocks = job.get('elif', [])
                            if isinstance(elif_blocks, dict):
                                elif_blocks = [elif_blocks]
                            elif elif_blocks and not isinstance(elif_blocks, list):
                                print(f"{Colors.WARNING}    ! Syntax warning [{current_task_name}] : 'elif' must be indented as a block (dictionary or list).{Colors.ENDC}")
                                elif_blocks = []
                                
                            for elif_block in elif_blocks:
                                elif_cond = elif_block.get('if')
                                if elif_cond:
                                    eval_cond = elif_cond
                                    for k, v in host_vars.items():
                                        safe_val = str(v).replace('\\', '\\\\').replace('\n', '\\n').replace('\r', '\\r').replace("'", "\\'")
                                        eval_cond = eval_cond.replace(f"<< {k} >>", safe_val).replace(f"<<{k}>>", safe_val)
                                    try:
                                        if bool(eval(eval_cond)):
                                            elif_executed = True
                                            for key, value in elif_block.items():
                                                if key not in ['if', 'foreach', 'while', 'retry_limit']:
                                                    execute_task(f"{current_task_name} (elif)", key, value, client, password, host_vars)
                                            break
                                    except Exception as e:
                                        print(f"{Colors.WARNING}    * Skipping [{current_task_name} (elif)] : Eval error on '{elif_cond}' -> {e}{Colors.ENDC}")
                            
                            if not elif_executed:
                                if 'else' in job:
                                    if isinstance(job['else'], dict):
                                        for key, value in job['else'].items():
                                            if key not in ['foreach', 'while', 'retry_limit']:
                                                execute_task(f"{current_task_name} (else)", key, value, client, password, host_vars)
                                    else:
                                        print(f"{Colors.WARNING}    ! Syntax warning [{current_task_name}] : 'else' must be indented as a block (dictionary).{Colors.ENDC}")
                                elif condition is not None:
                                    print(f"{Colors.CYAN}    * Skipping [{current_task_name}] : Condition not met{Colors.ENDC}")
                                    
                        if raw_while is None:
                            break
                            
                        while_iteration += 1
                        
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