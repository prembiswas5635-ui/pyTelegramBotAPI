import sqlite3
from datetime import datetime
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ----------------------------
# ⚠️ বট টোকেন ও এডমিন আইডি
# ----------------------------
TOKEN = '8912507133:AAHxFe50cwEvTss51ETY0s7KCxRF_8t8Th4'
ADMIN_ID = 7063215243  # আপনার টেলিগ্রাম আইডি

bot = telebot.TeleBot(TOKEN)

# --- ডাটাবেস সেটআপ ---
conn = sqlite3.connect('bot_database.db', check_same_thread=False)
cursor = conn.cursor()

# ইউজার টেবিল
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    status TEXT DEFAULT 'active',
    balance REAL DEFAULT 0.0
)''')
conn.commit()

# --- ইউজার কমান্ড (/start) ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    
    # ইউজারকে ডাটাবেসে সেভ করা
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    
    bot.reply_to(message, "👋 স্বাগতম! বট সফলভাবে কাজ করছে।")

# --- এডমিন প্যানেল কমান্ড (/admin) ---
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    user_id = message.from_user.id
    
    # সিকিউরিটি চেক: শুধু আপনি (ADMIN_ID) ঢুকতে পারবেন
    if user_id != ADMIN_ID:
        bot.reply_to(message, "❌ দুঃখিত! আপনি এই বটের এডমিন নন।")
        return

    # এডমিন বাটনসমূহ
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("📊 মোট ইউজার", callback_data="admin_stats"),
        InlineKeyboardButton("📢 ব্রডকাস্ট নোটিশ", callback_data="admin_broadcast"),
        InlineKeyboardButton("💰 ব্যালেন্স যোগ করুন", callback_data="admin_add_balance"),
        InlineKeyboardButton("⚙️ বট সেটিংস", callback_data="admin_settings")
    )
    
    bot.send_message(message.chat.id, "⚡ **স্বাগতম এডমিন প্যানেলে!**\n\nনিচের বাটনগুলো থেকে যেকোনো অপশন বেছে নিন:", reply_markup=markup, parse_mode="Markdown")

# --- এডমিন বাটন ক্লিকে রেসপন্স ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_'))
def admin_callback(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "আপনার এই ক্ষমতা নেই!", show_alert=True)
        return

    if call.data == "admin_stats":
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"📈 **বটের মোট ব্যবহারকারী:** {total_users} জন")
        
    elif call.data == "admin_broadcast":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📢 সকল ইউজারকে নোটিশ পাঠাতে ব্রডকাস্ট ফিচারটি ব্যবহার করুন।")

    elif call.data == "admin_add_balance":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "💰 ইউজার আইডিতে ব্যালেন্স যোগ করার ম্যানুয়াল কমান্ড সামনে আসছে।")

    elif call.data == "admin_settings":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "⚙️ বট সেটিংস আপডেট হচ্ছে...")

# বট চালু রাখা
bot.infinity_polling()
