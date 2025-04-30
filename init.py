import os

user = os.system("whoami")
home = os.system("$XDG_CONFIG_HOME")
active_folder = os.system('echo "$(pwd)"')
date = os.system