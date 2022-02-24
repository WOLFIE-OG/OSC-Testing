from colorama import init, Fore
import datetime
import pathlib

class Logger:
    def __init__(self):
        """Logging module"""
        init()
    
    def writeLog(self, data):
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        with open(pathlib.Path(f"logs/event-log-{date}.log"), "a+") as x:
            x.write(f"{data}\n")
    
    def info(self, info):
        """Out put info message"""
        self.writeLog(f"INFO:        {info}")
        print(f"{Fore.BLUE}INFO{Fore.WHITE}:     {info}")
    
    def success(self, success):
        """Out put success message"""
        self.writeLog(f"SUCCESS:  {success}")
        print(f"{Fore.GREEN}SUCCESS{Fore.WHITE}:  {success}")

    def error(self, error):
        """Out put error message"""
        self.writeLog(f"ERROR:     {error}")
        print(f"{Fore.RED}ERROR{Fore.WHITE}:    {error}")

    def warning(self, warning):
        """Out put warning message"""
        self.writeLog(f"WARNING:  {warning}")
        print(f"{Fore.YELLOW}WARNING{Fore.WHITE}:  {warning}")