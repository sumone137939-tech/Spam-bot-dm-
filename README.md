# 🚀 ABHINAV DM BOT - HYPER SPEED

A powerful Discord bot for sending DMs to users with multiple token support and ultra-fast parallel processing, perfect for Termux.

## ⚡ Features

✅ **Multiple Bot Support** - Manage up to 5 bot tokens  
✅ **HYPER SPEED** - All bots send messages in parallel (50+ msgs/sec)  
✅ **Interactive Menu** - Easy-to-use command interface  
✅ **Batch DM Sending** - Send multiple messages to a user  
✅ **User Mention Support** - Mention users with `<@user_id>`  
✅ **Real-time Statistics** - See messages/sec and msgs/minute speed  
✅ **Colored Output** - Beautiful console interface with BIG BANNER  
✅ **Environment Variables** - Secure token management  
✅ **Thread-safe** - Lock mechanism for accurate counting  
✅ **Zero Delay** - No waiting between messages  

## 📦 Installation

### 1. Install Python (Termux)
```bash
pkg update
pkg upgrade
pkg install python git
```

### 2. Clone Repository
```bash
git clone https://github.com/sumone137939-tech/Spam-bot-dm-.git
cd Spam-bot-dm-
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install discord.py python-dotenv colorama
```

### 4. Configure Bot Tokens
Edit `.env` file and add your Discord bot tokens:

```env
BOT_TOKEN_1=your_first_bot_token_here
BOT_TOKEN_2=your_second_bot_token_here
BOT_TOKEN_3=your_third_bot_token_here
BOT_TOKEN_4=your_fourth_bot_token_here
BOT_TOKEN_5=your_fifth_bot_token_here
```

## 🔑 How to Get Bot Tokens

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to "Bot" section and click "Add Bot"
4. Copy the token under "TOKEN"
5. Add it to `.env` file

## 🚀 Usage

### Run the Bot
```bash
python dm_bot_ultrafast.py
```

### What You'll See

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║                   🚀 ABHINAV DM BOT 🚀                      ║
║                                                                       ║
║              HYPER SPEED - ULTRA FAST                         ║
║           All Bots | Maximum Speed | Zero Delay              ║
║                                                                       ║
║          Version 1.0 - Discord DM Spammer                   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Main Menu

```
======================================================================
📋 MAIN MENU - HYPER SPEED MODE
======================================================================
1. 🚀 Send DM - MAXIMUM SPEED (All Bots)
2. 🚀 Send DM with Mention - MAXIMUM SPEED (All Bots)
3. Check Bot Status
4. View Statistics
5. Exit
======================================================================
```

### How to Send DMs

1. Select option `1` or `2`
2. Enter **User ID** (right-click user → Copy User ID in Discord)
3. Enter **Message** to send
4. Enter **Count** - how many times per bot to send
5. Bot will send messages instantly across all bots!

### Example

```
Enter user ID: 123456789
Enter message to send: Hello from ABHINAV BOT!
Number of times per bot (count): 10

💨 HYPER SPEED MODE ACTIVATED!
Sending 50 messages across 5 bots...

🚀 Result: 50 messages sent in ~1 second
⚡ Speed: 50.00 msgs/sec
💨 Rate: 3000 msgs/minute
```

## ⚙️ Requirements

- Python 3.8+
- discord.py 2.3.2+
- python-dotenv 1.0.0+
- colorama 0.4.6+

## 📊 Speed Comparison

| Feature | Details |
|---------|----------|
| **Bots** | 5 bots running in parallel |
| **Count** | 10 messages per bot |
| **Total Messages** | 50 messages |
| **Time Taken** | ~1 second |
| **Speed** | 50 msgs/sec |
| **Per Minute** | 3000 msgs/minute |

## 📨 Menu Options

| Option | Description |
|--------|-------------|
| 1 | Send DM across all bots in parallel |
| 2 | Send DM with user mention (@user) |
| 3 | View connected bots status |
| 4 | View overall statistics |
| 5 | Exit and shutdown all bots |

## ⚠️ Important Notes

🔒 **Token Security**: Never share your bot tokens publicly!

⏱️ **Rate Limiting**: Discord has rate limits. The bot includes intelligent delays on 429 errors.

👥 **User Consent**: Only send messages to users who consent.

🤖 **Bot Permissions**: Ensure bots have "Send Messages" permission in DMs.

📈 **Parallel Processing**: With 5 bots and count=10 = 50 messages sent simultaneously!

## 🐛 Troubleshooting

### "Invalid token" Error
- Check `.env` file for correct bot tokens
- Ensure no extra spaces in token
- Verify token format is correct

### "User not found" Error
- Check user ID is correct
- User might have DMs disabled
- Try with a different user

### Bot doesn't connect
- Check internet connection
- Verify Discord bot token is valid
- Ensure bot has necessary permissions

## 🎯 For Termux Users

### Run in background:
```bash
nohup python dm_bot_ultrafast.py > dm_bot.log 2>&1 &
```

### View logs:
```bash
tail -f dm_bot.log
```

### Keep running after closing terminal:
```bash
screen -S dmbot
python dm_bot_ultrafast.py
# Press Ctrl+A then D to detach
```

## 📁 File Structure

```
Spam-bot-dm-/
├── dm_bot_ultrafast.py    # Main bot script
├── .env                    # Bot tokens (edit with your tokens)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔄 Update Bot Tokens

To add/update tokens:
1. Edit `.env` file
2. Restart the bot
3. Select which token to use from the menu

## 📈 Statistics

The bot shows real-time statistics:
- ✓ Total messages sent
- ✗ Total messages failed
- ⏱️ Time taken
- ⚡ Speed in messages/second
- 💨 Speed in messages/minute

## 📞 Support

For issues or questions:
1. Check that all tokens are valid
2. Ensure bots have Send DM permissions
3. Verify user IDs are correct

## 📄 License

MIT License - Feel free to use and modify

## 👤 Author

**ABHINAV DM BOT**  
Created for ultra-fast Discord DM sending

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: ⚡ Active & Optimized
