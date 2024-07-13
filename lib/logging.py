import colorama as c
import threading as t
import datetime

def log(msg):
    print(f"{c.Fore.BLUE}i {c.Style.RESET_ALL}{datetime.datetime.now().strftime("[%H:%M:%S]")} <{t.currentThread().getName()}:LOG>{c.Fore.BLUE} {msg}{c.Style.RESET_ALL}")

def info(msg):
    print(f"{c.Fore.CYAN}i {c.Style.RESET_ALL}{datetime.datetime.now().strftime("[%H:%M:%S]")} <{t.currentThread().getName()}:INFO>{c.Fore.CYAN} {msg}{c.Style.RESET_ALL}")

def warn(msg):
    print(f"{c.Fore.YELLOW}! {c.Style.RESET_ALL}{datetime.datetime.now().strftime("[%H:%M:%S]")} <{t.currentThread().getName()}:WARN>{c.Fore.YELLOW} {msg}{c.Style.RESET_ALL}")
    
def error(msg):
    print(f"{c.Fore.RED}! {c.Style.RESET_ALL}{datetime.datetime.now().strftime("[%H:%M:%S]")} <{t.currentThread().getName()}:ERROR>{c.Fore.RED} {msg}{c.Style.RESET_ALL}")

def fatalError(msg):
    print(f"{c.Fore.RED}× {c.Style.RESET_ALL}{datetime.datetime.now().strftime("[%H:%M:%S]")} <{t.currentThread().getName()}:FATAL>{c.Fore.RED} {msg}{c.Style.RESET_ALL}")