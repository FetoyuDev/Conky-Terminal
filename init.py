import os
import subprocess
from tabulate import tabulate
from psutil import virtual_memory, swap_memory, disk_usage, cpu_percent
import psutil
import platform
import time

try:
    import curses
    use_curses = True
except ImportError:
    if platform.system() == "Windows":
        try:
            from blessed import Terminal
            term = Terminal()
            use_curses = False
        except ImportError:
            raise ImportError("A biblioteca 'blessed' é necessária no Windows. Instale-a com 'pip install blessed'.")
    else:
        raise

# Detectar o sistema operacional
system = platform.system()

if system == "Linux":
    user = subprocess.getoutput("id -un")
    hostname = subprocess.getoutput("hostname")
    home = subprocess.getoutput("echo $HOME")
    active_folder = subprocess.getoutput('pwd')
    date = subprocess.getoutput("date")
    IP = subprocess.getoutput("ifconfig | grep 'inet ' | grep -w 127.0.0.1 | awk '{print $2}'")
    clear_command = "clear"
elif system == "Windows":
    user = subprocess.getoutput("echo %USERNAME%")
    hostname = subprocess.getoutput("hostname")
    home = subprocess.getoutput("echo %USERPROFILE%")
    active_folder = subprocess.getoutput('cd')
    date = subprocess.getoutput("date /T && time /T")
    IP = subprocess.getoutput("ipconfig | findstr /C:\"IPv4\" | findstr /C:\"127.0.0.1\"")
    clear_command = "cls"

    import wmi
    c = wmi.WMI()

    # Remover informações de Swap no Windows
    swap = None

elif system == "Darwin":  # macOS
    user = subprocess.getoutput("id -un")
    hostname = subprocess.getoutput("hostname")
    home = subprocess.getoutput("echo $HOME")
    active_folder = subprocess.getoutput('pwd')
    date = subprocess.getoutput("date")
    IP = subprocess.getoutput("ifconfig | grep 'inet ' | grep -w 127.0.0.1 | awk '{print $2}'")
    clear_command = "clear"
else:
    raise Exception("Sistema operacional não suportado")

# Limpar o terminal ao iniciar
os.system(clear_command)

all_data = [user, hostname, home, active_folder, date, IP]


# Imprime os dados com quebra de linha
print(f"""
Todos os dados:
Usuário: {all_data[0]}
Nome do computador: {all_data[1]}
Pasta pessoal: {all_data[2]}
Pasta Ativa: {all_data[3]}
Data Atual: {all_data[4]}
""")

# Função para desenhar a interface dinâmica
if use_curses:
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
            if system != "Windows":
                swap = psutil.swap_memory()

            # Remover as barras de progresso da exibição principal
            # Adicionar as barras de progresso dentro da tabela
            table_data = [
                ["CPU (%)", f"{cpu_percent}%", f"[{('=' * int(cpu_percent // 10)).ljust(10)}]"],
                ["Memória Usada", f"{memory.used // (1024 ** 2)} MB", f"[{('=' * int(memory.percent // 10)).ljust(10)}]"],
                ["Memória Total", f"{memory.total // (1024 ** 2)} MB", ""],
                ["Disco Usado", f"{disk.used // (1024 ** 3)} GB", f"[{('=' * int(disk.percent // 10)).ljust(10)}]"],
                ["Disco Total", f"{disk.total // (1024 ** 3)} GB", ""],
                ["Usuário", user, ""],
                ["Hostname", hostname, ""],
                ["Home", home, ""],
                ["Pasta Ativa", active_folder, ""],
                ["Data", date, ""],
                ["IP", IP, ""]
            ]

            # Atualizar a tabela para não exibir Swap no Windows
            if system != "Windows":
                table_data.extend([
                    ["Swap Usado", f"{swap.used // (1024 ** 2)} MB", f"[{('=' * int(swap.percent // 10)).ljust(10)}]"],
                    ["Swap Total", f"{swap.total // (1024 ** 2)} MB", ""]
                ])

            # Ajustar a tabela para remover espaços desnecessários
            table = tabulate(table_data, headers=["Recurso", "Valor", "Progresso"], tablefmt="fancy_grid")
            table_lines = table.splitlines()

            # Ajustar a posição inicial da tabela para evitar espaços no topo
            start_y = 1  # Começar logo abaixo do título

            # Verificar se a tabela cabe na janela do terminal
            max_y, max_x = stdscr.getmaxyx()
            if len(table_lines) + start_y > max_y or any(len(line) > max_x for line in table_lines):
                stdscr.addstr(0, 0, "A janela do terminal é muito pequena para exibir o conteúdo.")
            else:
                # Exibir a tabela sem linhas em branco adicionais
                for idx, line in enumerate(table_lines):
                    stdscr.addstr(start_y + idx, 0, line)

            stdscr.refresh()
            time.sleep(1)
else:
    def draw_interface():
        with term.fullscreen(), term.cbreak():
            print(term.clear)
            while True:
                print(term.move(0, 0) + "Informações do Sistema")
                # Adapte o restante do código para exibir informações com `blessed`
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                if system != "Windows":
                    swap = psutil.swap_memory()

                table_data = [
                    ["CPU (%)", f"{cpu_percent}%", f"[{('=' * int(cpu_percent // 10)).ljust(10)}]"],
                    ["Memória Usada", f"{memory.used // (1024 ** 2)} MB", f"[{('=' * int(memory.percent // 10)).ljust(10)}]"],
                    ["Memória Total", f"{memory.total // (1024 ** 2)} MB", ""],
                    ["Disco Usado", f"{disk.used // (1024 ** 3)} GB", f"[{('=' * int(disk.percent // 10)).ljust(10)}]"],
                    ["Disco Total", f"{disk.total // (1024 ** 3)} GB", ""],
                    ["Usuário", user, ""],
                    ["Hostname", hostname, ""],
                    ["Home", home, ""],
                    ["Pasta Ativa", active_folder, ""],
                    ["Data", date, ""],
                    ["IP", IP, ""]
                ]

                if system != "Windows":
                    table_data.extend([
                        ["Swap Usado", f"{swap.used // (1024 ** 2)} MB", f"[{('=' * int(swap.percent // 10)).ljust(10)}]"],
                        ["Swap Total", f"{swap.total // (1024 ** 2)} MB", ""]
                    ])

                table = tabulate(table_data, headers=["Recurso", "Valor", "Progresso"], tablefmt="fancy_grid")
                print(term.move(1, 0) + table)

                time.sleep(1)

# Inicializar a interface curses
if __name__ == "__main__":
    try:
        if use_curses:
            curses.wrapper(draw_interface)
        else:
            draw_interface()
    except KeyboardInterrupt:
        os.system(clear_command)
