import subprocess

# Captura os valores dos comandos
user = subprocess.getoutput("id -un")
hostname = subprocess.getoutput("hostname")
home = subprocess.getoutput('echo $XDG_CONFIG_HOME')
active_folder = subprocess.getoutput('pwd')
date = subprocess.getoutput("date")

# Combina os valores em uma lista
all_data = [user, hostname, home, active_folder, date]

# Imprime os dados com quebra de linha
print(f"""Todos os dados:
Usuário: {all_data[0]}
Nome do computador: {all_data[1]}
Pasta pessoal: {all_data[2]}
Pasta Ativa: {all_data[3]}
Data Atual: {all_data[4]}""")