import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

PURPLE = Fore.MAGENTA

def display_logo():
    logo = f"""
{PURPLE}██████╗ {PURPLE} ██╗ {PURPLE}     ██╗{PURPLE}████████╗ {PURPLE}██████╗{PURPLE}██╗  ██╗{PURPLE}███████╗{PURPLE}██████╗ {PURPLE}
██╔════╝ {PURPLE}██║ {PURPLE}     ██║{PURPLE}╚══██╔══╝{PURPLE}██╔════╝{PURPLE}██║  ██║{PURPLE}██╔════╝{PURPLE}██╔══██╗{PURPLE}
██║  ███╗{PURPLE}██║ {PURPLE}     ██║{PURPLE}   ██║   {PURPLE}██║     {PURPLE}███████║{PURPLE}█████╗  {PURPLE}██║  ██║{PURPLE}
██║   ██║{PURPLE}██║ {PURPLE}     ██║{PURPLE}   ██║   {PURPLE}██║     {PURPLE}██╔══██║{PURPLE}██╔══╝  {PURPLE}██║  ██║{PURPLE}
╚██████╔╝{PURPLE}███████╗{PURPLE} ██║{PURPLE}   ██║   {PURPLE}╚██████╗{PURPLE}██║  ██║{PURPLE}███████╗{PURPLE}██████╔╝{PURPLE}
 ╚═════╝ {PURPLE}╚══════╝{PURPLE} ╚═╝{PURPLE}   ╚═╝    {PURPLE}╚═════╝{PURPLE}╚═╝  ╚═╝{PURPLE}╚══════╝{PURPLE}╚═════╝ {PURPLE}
                                                            
████████╗ {PURPLE}██████╗  {PURPLE}██████╗ {PURPLE}██╗     {PURPLE}███████╗{PURPLE}                  
╚══██╔══╝{PURPLE}██╔═══██╗{PURPLE}██╔═══██╗{PURPLE}██║     {PURPLE}██╔════╝{PURPLE}                  
   ██║   {PURPLE}██║   ██║{PURPLE}██║   ██║{PURPLE}██║     {PURPLE}███████╗{PURPLE}                  
   ██║   {PURPLE}██║   ██║{PURPLE}██║   ██║{PURPLE}██║     {PURPLE}╚════██║{PURPLE}                  
   ██║   {PURPLE}╚██████╔╝{PURPLE}╚██████╔╝{PURPLE}███████╗{PURPLE}███████║{PURPLE}                  
   ╚═╝    {PURPLE}╚═════╝  {PURPLE}╚═════╝ {PURPLE}╚══════╝{PURPLE}╚══════╝{PURPLE}                  
                            

{PURPLE}Creator: Glitched Tools
 Glitched Tools Discord Server Nuking Tool
{Style.RESET_ALL}
    """
    print(logo)

display_logo()
