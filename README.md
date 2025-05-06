# Conky Terminal

## A simple application made with python, to show system related info.

### This tool can show info such as:
- CPU usage
- Ram usage
- Disc usage
- Swap Usage
- Network usage
- Current active folder
- Home folder
- Host name
- User name

and more

# Installation steps
- Run the following command to install and start the application:
```bash
git clone https://github.com/FetoyuDev/tests.git && cd tests && pip3 install tabulate psutil time platform && python3 init.py
```

- Run this command to start the application normally: 
```bash
python3 init.py
```

- Run this command to update the application:
```bash
cd .. && rm -rfv tests && git clone https://github.com/FetoyuDev/tests.git && cd tests && pip3 install tabulate psutil time platform && python3 init.py
```

# Supported OS:
- Linux (I only tested it on Ubuntu, I believe it works with any Ubuntu based distro)
- Windows (Kinda, sone bugs, like IP not showing, proccess list not showing and such things) [Planned a bug fix to next update]

# Planned support for:
- Mac OS (I can´t test it, since I don't have any)
