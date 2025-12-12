import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

PURPLE = Fore.MAGENTA

def display_logo():
    logo = f"""
        {PURPLE}
  ________.__  ____  __         .__           ___________           .__          
 /  _____/|  |/_   |/  |_  ____ |  |__ ___  __\__    ___/___   ____ |  |   ______
/   \  ___|  | |   \   __\/ ___\|  |  \\  \/  / |    | /  _ \ /  _ \|  |  /  ___/
\    \_\  \  |_|   ||  | \  \___|   Y  \>    <  |    |(  <_> |  <_> )  |__\___ \ 
 \______  /____/___||__|  \___  >___|  /__/\_ \ |____| \____/ \____/|____/____  >
        \/                    \/     \/      \/                               \/          
         {PURPLE}                  
                            
{PURPLE}Creator: Glitched Tools
 Glitched Tools Discord Server Nuking Tool
{Style.RESET_ALL}
    """
    print(logo)

display_logo()
