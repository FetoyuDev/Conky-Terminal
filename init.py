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
        curses.mousemask(1)  # Habilitar eventos do mouse

        # Configurar cores no curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

        offset = 0  # Controle de scroll

        while True:
            stdscr.clear()

            # Obter informações do sistema
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            if system != "Windows":
                swap = psutil.swap_memory()

            # Criar a tabela de informações do sistema
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
            table_lines = table.splitlines()

            # Criar a tabela de processos ativos
            process_table = get_process_table()
            process_lines = process_table.splitlines()

            # Combinar as tabelas
            combined_lines = table_lines + ["", "Tabela de Processos:"] + process_lines

            # Verificar dimensões da janela
            max_y, max_x = stdscr.getmaxyx()

            # Ajustar o offset para scroll
            if offset < 0:
                offset = 0
            elif offset > max(0, len(combined_lines) - max_y):
                offset = max(0, len(combined_lines) - max_y)

            # Exibir as linhas visíveis
            visible_lines = combined_lines[offset:offset + max_y]
            for idx, line in enumerate(visible_lines):
                if len(line) > max_x:
                    line = line[:max_x - 3] + "..."
                stdscr.addstr(idx, 0, line)

            stdscr.refresh()

            # Capturar entrada do usuário
            key = stdscr.getch()
            if key == curses.KEY_UP:
                offset = max(0, offset - 1)  # Subir
            elif key == curses.KEY_DOWN:
                offset = min(len(combined_lines) - max_y, offset + 1)  # Descer
            elif key == curses.KEY_MOUSE:
                try:
                    _, _, _, _, button = curses.getmouse()
                    if button == curses.BUTTON4_PRESSED:  # Scroll up
                        offset = max(0, offset - 1)
                    elif button == curses.BUTTON5_PRESSED:  # Scroll down
                        offset = min(len(combined_lines) - max_y, offset + 1)
                except curses.error:
                    pass  # Ignorar erros relacionados ao mouse
            elif key == ord('q'):
                break

            time.sleep(0.1)
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

def get_process_table():
    # Obter todos os processos
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Ordenar os processos pelo uso de CPU
    processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)

    # Criar a tabela
    table_data = []
    for process in processes:
        cpu_bar = f"[{('=' * int(process['cpu_percent'] // 10)).ljust(10)}]"
        mem_bar = f"[{('=' * int(process['memory_percent'] // 10)).ljust(10)}]"
        table_data.append([
            process['name'] or 'N/A',
            f"{process['cpu_percent']}%", cpu_bar,
            f"{process['memory_percent']:.2f}%", mem_bar
        ])

    # Retornar a tabela formatada
    return tabulate(table_data, headers=["Processo", "CPU (%)", "Barra CPU", "RAM (%)", "Barra RAM"], tablefmt="fancy_grid")

# Inicializar a interface curses
if __name__ == "__main__":
    try:
        if use_curses:
            curses.wrapper(draw_interface)
        else:
            draw_interface()
    except KeyboardInterrupt:
        os.system(clear_command)  # Limpar o terminal ao sair com Ctrl+C
