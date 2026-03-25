def run(params: dict) -> str:
    """
    Generates a shell command that displays host information in a fun way.
    """

    ghost_script = r"""
HNAME=$(hostname)
IP=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -z "$IP" ]; then
    IP=$(ip -4 addr show scope global | grep -oP 'inet \K[\d.]+' | head -n 1 2>/dev/null || echo "Not found")
fi

MESSAGE="Wooo! I'm $HNAME ($IP)"

MSG_LEN=${#MESSAGE}
BORDER_LEN=$((MSG_LEN + 4))

for i in $(seq 1 $BORDER_LEN); do printf '-'; done
printf '\n'

printf '( %s )\n' "$MESSAGE"

for i in $(seq 1 $BORDER_LEN); do printf '-'; done
printf '\n'

printf '        \   \n'
printf '         \  .-.\n'
printf '           (o o)\n'
printf '           | O \\\n'
printf '            \   \\\n'
printf '             `~~~'''
"""
    
    return ghost_script