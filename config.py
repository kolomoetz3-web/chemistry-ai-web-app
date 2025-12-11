import os

# Telegram Bot Token
# Get token from @BotFather in Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7548174106:AAGv3f2dB-aPrWILhonyEtR56qBFgfFY0L0')

# If token is not found in environment variables, replace 'YOUR_BOT_TOKEN_HERE' with your real token
if TELEGRAM_TOKEN == 'YOUR_BOT_TOKEN_HERE':
    print("WARNING: Set TELEGRAM_BOT_TOKEN in environment variables or replace in config.py")