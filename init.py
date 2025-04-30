import subprocess

# Captura os valores dos comandos
user = subprocess.getoutput("whoami")
hostname = subprocess.getoutput("hostname")
home = subprocess.getoutput('echo $XDG_CONFIG_HOME')
active_folder = subprocess.getoutput('pwd')
date = subprocess.getoutput("date")

# Combina os valores em uma lista
all_data = [user, hostname, home, active_folder, date]

print(f"Todos os dados: {all_data[1]}")