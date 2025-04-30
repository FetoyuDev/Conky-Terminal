import os

user = os.system("whoami")
hostname = os.system("hostname")
home = os.system("$XDG_CONFIG_HOME")
active_folder = os.system('echo "$(pwd)"')
date = os.system("date")

all_data = [user, hostname, home, active_folder, date]

print("Todos os dados: {all_data}")