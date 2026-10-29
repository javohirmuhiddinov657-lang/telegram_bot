import telebot
from telebot import types

TOKEN = '8907733379:AAEpMU0cmDvPyysdC5vWBJD8_TYOhaGROWk'
bot = telebot.TeleBot(TOKEN)

CHANNELS = [-1003926387191, -1004313353926, -1004475706028] 

PRIVATE_CHANNEL_ID = -1004380860700

MOVIES = {
    "6": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] 
}

def check_all_subscriptions(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['creator', 'administrator', 'member']:
                return False
        except:
            return False
    return True

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🔍 Kino kodlarini qidirish")
    btn2 = types.KeyboardButton("💎 Premium")
    btn3 = types.KeyboardButton("🎲 Tasodifiy kino")
    btn4 = types.KeyboardButton("🏆 Top kinolar")
    btn5 = types.KeyboardButton("👤 Profil")
    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4, btn5)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    
    if not check_all_subscriptions(user_id):
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("🔒 1-guruhga qo'shilish", url="https://t.me/+VM_10wTxdmliZThi")
        btn2 = types.InlineKeyboardButton("🔒 2-guruhga qo'shilish", url="https://t.me/+9_glQwmckQ1lMjky")
        btn3 = types.InlineKeyboardButton("🔒 3-guruhga qo'shilish", url="https://t.me/+eHxXoF8wo3xjOTUy")
        btn_check = types.InlineKeyboardButton("🔄 Obunani tekshirish", callback_data="check_sub")
        markup_inline.add(btn1, btn2, btn3, btn_check)
        
        bot.send_message(
            message.chat.id,
            "⚠️ **Botdan foydalanish uchun quyidagi 3 ta guruhga ham obuna bo'lish so'rovini yuboring:**\n\n"
            "So'rov yuborganingizdan keyin **'Obunani tekshirish'** tugmasini bosing:",
            reply_markup=markup_inline,
            parse_mode="Markdown"
        )
    else:
        bot.send_message(
            message.chat.id,
            f"Tabriklayman, {name}! Botdan foydalanishingiz mumkin, kino kodini yuboring.",
            reply_markup=get_main_menu()
        )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_inline(call):
    user_id = call.from_user.id
    name = call.from_user.first_name
    
    if check_all_subscriptions(user_id):
        bot.answer_callback_query(call.id, "Rahmat, obuna tasdiqlandi! ✅")
        bot.send_message(
            call.message.chat.id,
            f"Tabriklayman, {name}! Botdan foydalanishingiz mumkin, kino kodini yuboring.",
            reply_markup=get_main_menu()
        )
    else:
        bot.answer_callback_query(call.id, "Siz hali hamma guruhlarga so'rov yubormadingiz yoki admin tasdiqlamadi! ❌", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    text = message.text

    if not check_all_subscriptions(user_id):
        bot.send_message(message.chat.id, "Iltimos, avval ko'rsatilgan 3 ta guruhga qo'shilish so'rovini yuboring va /start buyrug'ini bosing.")
        return

    if text == "🔍 Kino kodlarini qidirish":
        bot.send_message(message.chat.id, "Kino kodini yuboring:")
    elif text == "💎 Premium":
        bot.send_message(message.chat.id, "💎 Premium bo'limi tez orada ishga tushadi!")
    elif text == "🎲 Tasodifiy kino":
        bot.send_message(message.chat.id, "🎲 Hozircha tasodifiy kinolar mavjud emas.")
    elif text == "🏆 Top kinolar":
        bot.send_message(message.chat.id, "🏆 Top kinolar ro'yxati bo'sh.")
    elif text == "👤 Profil":
        bot.send_message(message.chat.id, f"👤 Ismingiz: {name}\n🆔 ID raqamingiz: `{user_id}`", parse_mode="Markdown")
    else:
        code = text.strip()
        if code in MOVIES:
            bot.send_message(message.chat.id, "Mana kino qismlari:")
            for msg_id in MOVIES[code]:
                try:
                    bot.copy_message(chat_id=message.chat.id, from_chat_id=PRIVATE_CHANNEL_ID, message_id=msg_id)
                except Exception as e:
                    print(f"Xatolik: {e}")
        else:
            bot.send_message(message.chat.id, "Bunday raqamdagi kino topilmadi. To'g'ri kino kodini yuboring.")

print("Kino boti ishga tushdi...")
bot.infinity_polling()
