import sqlite3
from datetime import datetime
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# --------------------------------------------------
# ⚠️ বট টোকেন ও এডমিন আইডি
# --------------------------------------------------
TOKEN = '8912507133:AAHxFe50cwEvTss51ETY0s7KCxRF_8t8Th4'
ADMIN_ID = 7063215243

bot = telebot.TeleBot(TOKEN)

# --- ডেটাবেস সেটআপ ---
conn = sqlite3.connect('bot_database.db', check_same_thread=False)
cursor = conn.cursor()

# ইউজার টেবিল
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    status TEXT DEFAULT 'active'
)'''
)

# উইথড্র টেবিল
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS withdraws (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    time TEXT
)'''
)

conn.commit()


# --- /start কমান্ড (ইউজারদের জন্য) ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
  user_id = message.from_user.id

  cursor.execute('SELECT status FROM users WHERE user_id = ?', (user_id,))
  user = cursor.fetchone()

  if user and user[0] == 'banned':
    bot.reply_to(message, '❌ আপনাকে এই বটে ব্যান করা হয়েছে!')
    return

  if not user:
    cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()

  bot.reply_to(
      message,
      '👋 স্বাগতম! বট সফলভাবে কাজ করছে।',
  )


print('বট সফলভাবে চালু হয়েছে...')
bot.infinity_polling()
