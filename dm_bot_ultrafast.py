#!/usr/bin/env python3
import discord
from discord.ext import commands
import os
import sys
import asyncio
from dotenv import load_dotenv
from colorama import Fore, Back, Style, init
from datetime import datetime
import threading

# Initialize colorama
init(autoreset=True)

def print_big_banner():
    """Display the HUGE main banner"""
    banner = f"""
{Fore.MAGENTA}
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║                   {Fore.CYAN}🚀 ABHINAV DM BOT 🚀{Fore.MAGENTA}                      ║
║                                                                       ║
║              {Fore.YELLOW}HYPER SPEED - ULTRA FAST{Fore.MAGENTA}                         ║
║           {Fore.YELLOW}All Bots | Maximum Speed | Zero Delay{Fore.MAGENTA}              ║
║                                                                       ║
║          {Fore.GREEN}Version 1.0 - Discord DM Spammer{Fore.MAGENTA}                   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
    """
    print(banner)


# Load environment variables
load_dotenv()

# Get all bot tokens
BOT_TOKENS = []
for i in range(1, 6):
    token = os.getenv(f"BOT_TOKEN_{i}")
    if token and token != "your_bot_token_1_here":
        BOT_TOKENS.append(token)

if not BOT_TOKENS:
    print(f"{Fore.RED}❌ No valid bot tokens found in .env file!")
    sys.exit(1)

print(f"{Fore.GREEN}✓ Loaded {len(BOT_TOKENS)} bot token(s){Style.RESET_ALL}")

# Global statistics with thread safety
STATS = {
    'total_sent': 0,
    'total_failed': 0,
    'total_bots': len(BOT_TOKENS),
    'start_time': None,
    'bots_connected': 0,
    'lock': threading.Lock()
}


class HyperSpeedDMBot(commands.Cog):
    def __init__(self, bot, bot_index):
        self.bot = bot
        self.bot_index = bot_index
        self.messages_sent = 0
        self.messages_failed = 0

    async def send_dm_fast(self, user_id: int, message: str, mention: bool = False):
        """Send DM with no delays - HYPER SPEED"""
        try:
            user = await self.bot.fetch_user(user_id)
            
            if mention:
                final_message = f"<@{user_id}> {message}"
            else:
                final_message = message
            
            await user.send(final_message)
            
            with STATS['lock']:
                self.messages_sent += 1
                STATS['total_sent'] += 1
            
            return True, user
        except discord.NotFound:
            with STATS['lock']:
                self.messages_failed += 1
                STATS['total_failed'] += 1
            return False, None
        except discord.Forbidden:
            with STATS['lock']:
                self.messages_failed += 1
                STATS['total_failed'] += 1
            return False, None
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(0.1)
                try:
                    await user.send(final_message)
                    with STATS['lock']:
                        self.messages_sent += 1
                        STATS['total_sent'] += 1
                    return True, user
                except:
                    with STATS['lock']:
                        self.messages_failed += 1
                        STATS['total_failed'] += 1
                    return False, None
            with STATS['lock']:
                self.messages_failed += 1
                STATS['total_failed'] += 1
            return False, None
        except Exception as e:
            with STATS['lock']:
                self.messages_failed += 1
                STATS['total_failed'] += 1
            return False, None


async def create_bot_instance(token, bot_index):
    """Create and connect a bot instance"""
    try:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.dm_messages = True
        
        bot = commands.Bot(command_prefix="!", intents=intents)
        cog = HyperSpeedDMBot(bot, bot_index)
        await bot.add_cog(cog)
        
        @bot.event
        async def on_ready():
            with STATS['lock']:
                STATS['bots_connected'] += 1
            print(f"{Fore.GREEN}[✓ Bot {bot_index + 1}] Connected: {bot.user.name}#{bot.user.discriminator}{Style.RESET_ALL}")
        
        asyncio.create_task(bot.start(token))
        await asyncio.sleep(1)
        
        return bot, cog
    except Exception as e:
        print(f"{Fore.RED}[✗ Bot {bot_index + 1}] Connection failed: {str(e)}{Style.RESET_ALL}")
        return None, None


async def send_dm_hyper_speed(user_id: int, message: str, count: int, mention: bool = False, bots_and_cogs=None):
    """Send DMs using ALL BOTS in HYPER SPEED"""
    if not bots_and_cogs:
        return
    
    STATS['start_time'] = datetime.now()
    tasks = []
    message_count = 0
    
    for i in range(count):
        for bot, cog in bots_and_cogs:
            if bot and bot.user:
                task = asyncio.create_task(cog.send_dm_fast(user_id, message, mention))
                tasks.append((task, i + 1, bot.user.name, cog))
                message_count += 1
    
    print(f"\n{Fore.YELLOW}{'='*70}")
    print(f"{Fore.CYAN}🚀 HYPER SPEED MODE - SENDING {message_count} MESSAGES INSTANTLY!{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}💨 All {len(bots_and_cogs)} bots firing at maximum speed...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
    
    results = await asyncio.gather(*[task for task, _, _, _ in tasks], return_exceptions=True)
    
    success_count = 0
    for result, msg_num, bot_name, cog in zip(results, [x[1] for x in tasks], [x[2] for x in tasks], [x[3] for x in tasks]):
        if isinstance(result, tuple) and result[0]:
            if result[1]:
                success_count += 1
                print(f"{Fore.GREEN}[✓ {bot_name}] Message {msg_num} sent{Style.RESET_ALL}", end=" ")
                if success_count % 5 == 0:
                    print()
        else:
            print(f"{Fore.RED}[✗ {bot_name}] Message {msg_num} failed{Style.RESET_ALL}", end=" ")
    
    print()
    
    elapsed = (datetime.now() - STATS['start_time']).total_seconds()
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.YELLOW}📊 HYPER SPEED COMPLETE{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Total Sent: {STATS['total_sent']}/{message_count}")
    print(f"{Fore.RED}✗ Total Failed: {STATS['total_failed']}")
    print(f"{Fore.YELLOW}⏱️  Time Taken: {elapsed:.3f}s")
    if STATS['total_sent'] > 0:
        speed = STATS['total_sent'] / elapsed
        print(f"{Fore.CYAN}⚡ HYPER SPEED: {speed:.2f} msgs/sec")
        print(f"{Fore.MAGENTA}💨 Rate: {speed * 60:.0f} msgs/minute")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")


async def interactive_menu():
    """Interactive menu for sending bulk DMs"""
    print(f"\n{Fore.YELLOW}🔌 Connecting all bots at lightning speed...{Style.RESET_ALL}")
    bots_and_cogs = []
    
    for i, token in enumerate(BOT_TOKENS):
        bot, cog = await create_bot_instance(token, i)
        if bot:
            bots_and_cogs.append((bot, cog))
    
    await asyncio.sleep(2)
    
    print(f"\n{Fore.GREEN}✓ All {len(bots_and_cogs)} bots ready for HYPER SPEED!{Style.RESET_ALL}\n")
    
    while True:
        print(f"\n{Fore.YELLOW}{'='*70}")
        print(f"{Fore.CYAN}📋 MAIN MENU - HYPER SPEED MODE{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}1. 🚀 Send DM - MAXIMUM SPEED (All Bots)")
        print(f"{Fore.MAGENTA}2. 🚀 Send DM with Mention - MAXIMUM SPEED (All Bots)")
        print(f"{Fore.GREEN}3. Check Bot Status")
        print(f"{Fore.GREEN}4. View Statistics")
        print(f"{Fore.RED}5. Exit")
        print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
        
        choice = input(f"{Fore.CYAN}Enter your choice (1-5): {Style.RESET_ALL}").strip()
        
        if choice == "1":
            await send_dm_menu(bots_and_cogs, mention=False)
        elif choice == "2":
            await send_dm_menu(bots_and_cogs, mention=True)
        elif choice == "3":
            print_bot_status(bots_and_cogs)
        elif choice == "4":
            print_statistics()
        elif choice == "5":
            print(f"{Fore.RED}Shutting down all bots...{Style.RESET_ALL}")
            for bot, _ in bots_and_cogs:
                try:
                    await bot.close()
                except:
                    pass
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")


async def send_dm_menu(bots_and_cogs, mention=False):
    """Menu for sending DMs"""
    print(f"\n{Fore.CYAN}{'='*70}")
    if mention:
        print(f"{Fore.YELLOW}📨 SEND DM WITH MENTION - HYPER SPEED{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}📨 SEND DM - HYPER SPEED{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    try:
        user_id = int(input(f"{Fore.GREEN}Enter user ID: {Style.RESET_ALL}").strip())
        message = input(f"{Fore.GREEN}Enter message to send: {Style.RESET_ALL}").strip()
        count = int(input(f"{Fore.GREEN}Number of times per bot (count): {Style.RESET_ALL}").strip())
        
        if count < 1:
            print(f"{Fore.RED}❌ Count must be at least 1{Style.RESET_ALL}")
            return
        
        if not message:
            print(f"{Fore.RED}❌ Message cannot be empty{Style.RESET_ALL}")
            return
        
        total_messages = count * len(bots_and_cogs)
        print(f"\n{Fore.MAGENTA}💨 HYPER SPEED MODE ACTIVATED!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Sending {total_messages} messages across {len(bots_and_cogs)} bots...{Style.RESET_ALL}")
        await send_dm_hyper_speed(user_id, message, count, mention, bots_and_cogs)
    
    except ValueError:
        print(f"{Fore.RED}❌ Invalid input. Please enter valid numbers.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")


def print_bot_status(bots_and_cogs):
    """Print bot status information"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.YELLOW}📊 BOT STATUS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    for i, (bot, cog) in enumerate(bots_and_cogs):
        if bot.user:
            print(f"{Fore.GREEN}Bot {i+1}: {bot.user.name}#{bot.user.discriminator} ✓ Online{Style.RESET_ALL}")
            print(f"        Sent: {cog.messages_sent} | Failed: {cog.messages_failed}")
        else:
            print(f"{Fore.RED}Bot {i+1}: Offline{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}Total Bots: {len(bots_and_cogs)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")


def print_statistics():
    """Print overall statistics"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.YELLOW}📈 HYPER SPEED STATISTICS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}✓ Messages Sent: {STATS['total_sent']}")
    print(f"{Fore.RED}✗ Messages Failed: {STATS['total_failed']}")
    print(f"{Fore.YELLOW}🤖 Bots Loaded: {STATS['total_bots']}")
    print(f"{Fore.YELLOW}🟢 Bots Connected: {STATS['bots_connected']}")
    
    if STATS['start_time']:
        elapsed = (datetime.now() - STATS['start_time']).total_seconds()
        if elapsed > 0 and STATS['total_sent'] > 0:
            speed = STATS['total_sent'] / elapsed
            print(f"{Fore.CYAN}⚡ Speed: {speed:.2f} msgs/sec")
            print(f"{Fore.MAGENTA}💨 Rate: {speed * 60:.0f} msgs/min")
    
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")


async def main():
    """Main entry point"""
    # Show BIG BANNER first when program starts
    print_big_banner()
    
    await asyncio.sleep(2)  # Show banner for 2 seconds
    
    print(f"\n{Fore.YELLOW}{'='*70}")
    print(f"{Fore.MAGENTA}💨 Starting ABHINAV DM BOT - HYPER SPEED MODE")
    print(f"{Fore.GREEN}📊 Bots to load: {len(BOT_TOKENS)}")
    print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
    
    await asyncio.sleep(1)
    
    await interactive_menu()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Bot stopped by user{Style.RESET_ALL}")
        sys.exit(0)
