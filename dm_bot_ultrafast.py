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
import time

# Initialize colorama
init(autoreset=True)

def print_big_banner():
    """Display the HUGE main banner"""
    banner = f"""
{Fore.MAGENTA}
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║              {Fore.CYAN}🚀 ABHINAV DM BOT - EXTREME HYPER SPEED 🚀{Fore.MAGENTA}        ║
║                                                                       ║
║           {Fore.YELLOW}LIGHTNING FAST | MAXIMUM OPTIMIZATION{Fore.MAGENTA}            ║
║        {Fore.YELLOW}All Bots | 100+ msgs/sec | Zero Delay{Fore.MAGENTA}              ║
║                                                                       ║
║       {Fore.GREEN}Version 2.0 - Ultra Fast Discord DM Spammer{Fore.MAGENTA}          ║
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
    'lock': threading.Lock(),
    'current_speed': 0.0
}


class ExtremeHyperSpeedDMBot(commands.Cog):
    def __init__(self, bot, bot_index):
        self.bot = bot
        self.bot_index = bot_index
        self.messages_sent = 0
        self.messages_failed = 0

    async def send_dm_extreme(self, user_id: int, message: str, mention: bool = False):
        """Send DM with EXTREME speed - NO DELAYS"""
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
            if e.status == 429:  # Rate limited - minimal delay
                await asyncio.sleep(0.01)  # Only 10ms delay
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
    """Create and connect a bot instance with minimal delay"""
    try:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.dm_messages = True
        
        bot = commands.Bot(command_prefix="!", intents=intents)
        cog = ExtremeHyperSpeedDMBot(bot, bot_index)
        await bot.add_cog(cog)
        
        @bot.event
        async def on_ready():
            with STATS['lock']:
                STATS['bots_connected'] += 1
            print(f"{Fore.GREEN}[✓ Bot {bot_index + 1}] {bot.user.name}#{bot.user.discriminator}{Style.RESET_ALL}")
        
        asyncio.create_task(bot.start(token))
        await asyncio.sleep(0.5)  # Minimal connection delay
        
        return bot, cog
    except Exception as e:
        print(f"{Fore.RED}[✗ Bot {bot_index + 1}] Failed: {str(e)}{Style.RESET_ALL}")
        return None, None


async def send_dm_extreme_speed(user_id: int, message: str, count: int, mention: bool = False, bots_and_cogs=None):
    """Send DMs at EXTREME SPEED using maximum parallelization"""
    if not bots_and_cogs:
        return
    
    STATS['start_time'] = datetime.now()
    all_tasks = []
    message_count = 0
    
    # Pre-create ALL tasks instantly - maximum batch size
    for i in range(count):
        for bot, cog in bots_and_cogs:
            if bot and bot.user:
                task = asyncio.create_task(cog.send_dm_extreme(user_id, message, mention))
                all_tasks.append((task, i + 1, bot.user.name))
                message_count += 1
    
    # Display start info
    print(f"\n{Fore.YELLOW}{'='*75}")
    print(f"{Fore.MAGENTA}⚡ EXTREME HYPER SPEED MODE{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🚀 SENDING {message_count} MESSAGES AT MAXIMUM VELOCITY!{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}💨 All {len(bots_and_cogs)} bots firing at full throttle...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*75}{Style.RESET_ALL}\n")
    
    # Execute ALL tasks concurrently with no delays - EXTREME SPEED
    results = await asyncio.gather(*[task for task, _, _ in all_tasks], return_exceptions=True)
    
    # Live counter display
    success_count = 0
    print(f"{Fore.GREEN}", end="")
    for result, msg_num, bot_name in zip(results, [x[1] for x in all_tasks], [x[2] for x in all_tasks]):
        if isinstance(result, tuple) and result[0]:
            success_count += 1
            print("█", end="", flush=True)
            if success_count % 50 == 0:
                print(f" {success_count}", flush=True)
        else:
            print(f"{Fore.RED}✗{Fore.GREEN}", end="", flush=True)
    print(f"{Style.RESET_ALL}\n")
    
    # Calculate statistics
    elapsed = (datetime.now() - STATS['start_time']).total_seconds()
    
    print(f"{Fore.CYAN}{'='*75}")
    print(f"{Fore.MAGENTA}⚡ EXTREME SPEED COMPLETE ⚡{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Sent: {STATS['total_sent']}/{message_count}", end="")
    
    if STATS['total_failed'] > 0:
        print(f" {Fore.RED}| Failed: {STATS['total_failed']}", end="")
    
    print(f"{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}⏱️  Time: {elapsed:.3f}s")
    
    if STATS['total_sent'] > 0 and elapsed > 0:
        speed = STATS['total_sent'] / elapsed
        speed_per_min = speed * 60
        speed_per_hour = speed * 3600
        
        print(f"{Fore.CYAN}⚡ SPEED: {speed:.2f} msgs/sec")
        print(f"{Fore.MAGENTA}💨 RATE: {speed_per_min:.0f} msgs/min")
        print(f"{Fore.YELLOW}🚀 VELOCITY: {speed_per_hour:.0f} msgs/hour{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}{'='*75}{Style.RESET_ALL}")


async def interactive_menu():
    """Interactive menu for extreme speed DM sending"""
    print(f"\n{Fore.YELLOW}⚡ Connecting all bots at extreme velocity...{Style.RESET_ALL}")
    bots_and_cogs = []
    
    for i, token in enumerate(BOT_TOKENS):
        bot, cog = await create_bot_instance(token, i)
        if bot:
            bots_and_cogs.append((bot, cog))
    
    await asyncio.sleep(1)  # Minimal wait
    
    print(f"\n{Fore.GREEN}✓ {len(bots_and_cogs)} bots ready for EXTREME HYPER SPEED!{Style.RESET_ALL}\n")
    
    while True:
        print(f"\n{Fore.YELLOW}{'='*75}")
        print(f"{Fore.CYAN}📋 MAIN MENU - EXTREME HYPER SPEED MODE{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*75}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}1. ⚡ Send DM - EXTREME SPEED (All Bots)")
        print(f"{Fore.MAGENTA}2. ⚡ Send DM with Mention - EXTREME SPEED (All Bots)")
        print(f"{Fore.GREEN}3. 📊 Check Bot Status")
        print(f"{Fore.GREEN}4. 📈 View Statistics")
        print(f"{Fore.GREEN}5. 🔧 Advanced Settings")
        print(f"{Fore.RED}6. Exit")
        print(f"{Fore.YELLOW}{'='*75}{Style.RESET_ALL}")
        
        choice = input(f"{Fore.CYAN}Enter your choice (1-6): {Style.RESET_ALL}").strip()
        
        if choice == "1":
            await send_dm_menu(bots_and_cogs, mention=False)
        elif choice == "2":
            await send_dm_menu(bots_and_cogs, mention=True)
        elif choice == "3":
            print_bot_status(bots_and_cogs)
        elif choice == "4":
            print_statistics()
        elif choice == "5":
            print_advanced_settings(bots_and_cogs)
        elif choice == "6":
            print(f"{Fore.RED}⚠️  Shutting down all bots...{Style.RESET_ALL}")
            for bot, _ in bots_and_cogs:
                try:
                    await bot.close()
                except:
                    pass
            break
        else:
            print(f"{Fore.RED}Invalid choice. Try again.{Style.RESET_ALL}")


async def send_dm_menu(bots_and_cogs, mention=False):
    """Menu for sending DMs with extreme speed"""
    print(f"\n{Fore.CYAN}{'='*75}")
    if mention:
        print(f"{Fore.YELLOW}📨 SEND DM WITH MENTION - EXTREME HYPER SPEED{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}📨 SEND DM - EXTREME HYPER SPEED{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*75}{Style.RESET_ALL}")
    
    try:
        user_id = int(input(f"{Fore.GREEN}Enter user ID: {Style.RESET_ALL}").strip())
        message = input(f"{Fore.GREEN}Enter message to send: {Style.RESET_ALL}").strip()
        count = int(input(f"{Fore.GREEN}Number of times per bot (1-1000): {Style.RESET_ALL}").strip())
        
        if count < 1 or count > 1000:
            print(f"{Fore.RED}❌ Count must be between 1 and 1000{Style.RESET_ALL}")
            return
        
        if not message:
            print(f"{Fore.RED}❌ Message cannot be empty{Style.RESET_ALL}")
            return
        
        total_messages = count * len(bots_and_cogs)
        print(f"\n{Fore.MAGENTA}⚡ EXTREME SPEED MODE ACTIVATED!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🚀 Sending {total_messages} messages across {len(bots_and_cogs)} bots...{Style.RESET_ALL}")
        await send_dm_extreme_speed(user_id, message, count, mention, bots_and_cogs)
    
    except ValueError:
        print(f"{Fore.RED}❌ Invalid input. Enter valid numbers.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")


def print_bot_status(bots_and_cogs):
    """Print bot status"""
    print(f"\n{Fore.CYAN}{'='*75}")
    print(f"{Fore.YELLOW}📊 BOT STATUS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*75}{Style.RESET_ALL}")
    
    for i, (bot, cog) in enumerate(bots_and_cogs):
        if bot.user:
            print(f"{Fore.GREEN}Bot {i+1}: {bot.user.name}#{bot.user.discriminator} ✓{Style.RESET_ALL}")
            print(f"       Sent: {cog.messages_sent} | Failed: {cog.messages_failed}")
        else:
            print(f"{Fore.RED}Bot {i+1}: Offline{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}Total: {len(bots_and_cogs)} bots{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*75}{Style.RESET_ALL}")


def print_statistics():
    """Print statistics"""
    print(f"\n{Fore.CYAN}{'='*75}")
    print(f"{Fore.MAGENTA}📈 EXTREME HYPER SPEED STATISTICS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*75}{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}✓ Messages Sent: {STATS['total_sent']}")
    print(f"{Fore.RED}✗ Messages Failed: {STATS['total_failed']}")
    print(f"{Fore.YELLOW}🤖 Bots Loaded: {STATS['total_bots']}")
    print(f"{Fore.YELLOW}🟢 Connected: {STATS['bots_connected']}")
    
    if STATS['start_time']:
        elapsed = (datetime.now() - STATS['start_time']).total_seconds()
        if elapsed > 0 and STATS['total_sent'] > 0:
            speed = STATS['total_sent'] / elapsed
            print(f"{Fore.CYAN}⚡ Speed: {speed:.2f} msgs/sec")
            print(f"{Fore.MAGENTA}💨 Rate: {speed * 60:.0f} msgs/min")
            print(f"{Fore.YELLOW}🚀 Velocity: {speed * 3600:.0f} msgs/hour")
    
    print(f"{Fore.CYAN}{'='*75}{Style.RESET_ALL}")


def print_advanced_settings(bots_and_cogs):
    """Print advanced settings info"""
    print(f"\n{Fore.CYAN}{'='*75}")
    print(f"{Fore.MAGENTA}🔧 ADVANCED SETTINGS & INFO{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*75}{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}System Configuration:")
    print(f"  • Maximum Count: 1000 messages")
    print(f"  • Bots Running: {len(bots_and_cogs)}")
    print(f"  • Max Parallel Tasks: {len(bots_and_cogs) * 1000}")
    print(f"  • Processing Mode: Extreme Parallel")
    print(f"  • Rate Limit Handling: Smart (10ms delays only)")
    print(f"  • Thread Safety: Enabled with locks")
    
    print(f"\n{Fore.GREEN}Optimization Levels:")
    print(f"  ✓ Task Pre-creation: All tasks created instantly")
    print(f"  ✓ Concurrent Gathering: All tasks run simultaneously")
    print(f"  ✓ Zero Message Delays: No waiting between sends")
    print(f"  ✓ Live Progress: Real-time visual feedback")
    print(f"  ✓ Speed Tracking: msgs/sec, msgs/min, msgs/hour")
    
    print(f"\n{Fore.YELLOW}Maximum Performance:")
    print(f"  • With 5 bots × 1000 count = 5000 messages")
    print(f"  • Expected time: ~50-100 seconds")
    print(f"  • Speed: 50-100 msgs/sec")
    
    print(f"{Fore.CYAN}{'='*75}{Style.RESET_ALL}")


async def main():
    """Main entry point"""
    # Show BIG BANNER
    print_big_banner()
    
    await asyncio.sleep(2)
    
    print(f"\n{Fore.YELLOW}{'='*75}")
    print(f"{Fore.MAGENTA}⚡ Starting ABHINAV DM BOT - EXTREME HYPER SPEED")
    print(f"{Fore.GREEN}📊 Bots to load: {len(BOT_TOKENS)}")
    print(f"{Fore.YELLOW}{'='*75}{Style.RESET_ALL}")
    
    await asyncio.sleep(1)
    
    await interactive_menu()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Bot stopped by user{Style.RESET_ALL}")
        sys.exit(0)
