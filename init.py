import os
import subprocess
from tabulate import tabulate
from colorama import Style
from colorama import init as colorama_init
from psutil import virtual_memory, swap_memory, disk_usage, cpu_percent
import curses
import psutil
import time

user = subprocess.getoutput("id -un")
hostname = subprocess.getoutput("hostname")
home = home = subprocess.getoutput("echo $HOME")
active_folder = subprocess.getoutput('pwd')
date = subprocess.getoutput("date")
IP = subprocess.getoutput("ifconfig | grep 'inet ' | grep -w 127.0.0.1 | awk '{print $2}'")

all_data = [user, hostname, home, active_folder, date, IP]

<<<<<<< HEAD
# Imprime os dados com quebra de linha
print(f"""
Todos os dados:
Usuário: {all_data[0]}
Nome do computador: {all_data[1]}
Pasta pessoal: {all_data[2]}
Pasta Ativa: {all_data[3]}
Data Atual: {all_data[4]}
""")
=======
# Função para desenhar a interface dinâmica
def draw_interface(stdscr):
    curses.curs_set(0)  # Ocultar o cursor
    stdscr.nodelay(1)  # Permitir atualizações sem bloquear

    # Configurar cores no curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    while True:
        stdscr.clear()

        # Obter informações do sistema
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        swap = psutil.swap_memory()

        # Remover as barras de progresso da exibição principal
        # Adicionar as barras de progresso dentro da tabela
        table_data = [
            ["CPU (%)", f"{cpu_percent}%", f"[{('=' * int(cpu_percent // 10)).ljust(10)}]"],
            ["Memória Usada", f"{memory.used // (1024 ** 2)} MB", f"[{('=' * int(memory.percent // 10)).ljust(10)}]"],
            ["Memória Total", f"{memory.total // (1024 ** 2)} MB", ""],
            ["Disco Usado", f"{disk.used // (1024 ** 3)} GB", f"[{('=' * int(disk.percent // 10)).ljust(10)}]"],
            ["Disco Total", f"{disk.total // (1024 ** 3)} GB", ""],
            ["Swap Usado", f"{swap.used // (1024 ** 2)} MB", f"[{('=' * int(swap.percent // 10)).ljust(10)}]"],
            ["Swap Total", f"{swap.total // (1024 ** 2)} MB", ""],
            ["Usuário", user, ""],
            ["Hostname", hostname, ""],
            ["Home", home, ""],
            ["Pasta Ativa", active_folder, ""],
            ["Data", date, ""],
            ["IP", IP, ""]
        ]
        table = tabulate(table_data, headers=["Recurso", "Valor", "Progresso"], tablefmt="fancy_grid")

        # Ajustar o conteúdo para caber na janela do terminal
        max_y, max_x = stdscr.getmaxyx()
        if len(table.splitlines()) + 6 > max_y or len(max(table.splitlines(), key=len)) > max_x:
            stdscr.addstr(6, 0, "A janela do terminal é muito pequena para exibir o conteúdo.")
        else:
            stdscr.addstr(6, 0, table)

        stdscr.refresh()
        time.sleep(1)

# Inicializar a interface curses
if __name__ == "__main__":
    try:
        curses.wrapper(draw_interface)
    except KeyboardInterrupt:
        os.system("clear")
>>>>>>> 1d8fecb (updated a few things)
