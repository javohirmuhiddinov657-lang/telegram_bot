import telebot
from telebot import types

TOKEN = '8907733379:AAEpMU0cmDvPyysdC5vWBJD8_TYOhaGROWk'
bot = telebot.TeleBot(TOKEN)

# Majburiy obuna kanallari
CHANNELS = ['@muxiddinov_uz', '@ziyadullayevv_uz']

# Yopiq kanalning ID raqami (boshiga -100 qo'shiladi)
PRIVATE_CHANNEL_ID = -1004380860700

# Multfilm qismlari (yopiq kanaldagi post raqamlari)
MOVIES = {
    "6": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
}

# Obunani tekshiruvchi funksiya
def check_all_subscriptions(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['creator', 'administrator', 'member']:
                return False
        except:
            return False
    return True

# /start buyrug'i
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if not check_all_subscriptions(user_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("📢 1-kanalga obuna bo'lish", url="https://t.me/muxiddinov_uz")
        btn2 = types.InlineKeyboardButton("📢 2-kanalga obuna bo'lish", url="https://t.me/ziyadullayevv_uz")
        btn_check = types.InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub")
        markup.add(btn1, btn2, btn_check)
        
        bot.send_message(
            message.chat.id,
            "Botdan foydalanish uchun quyidagi **ikkala kanalga** ham obuna bo'ling:\n\n1. @muxiddinov_uz\n2. @ziyadullayevv_uz\n\nObuna bo'lgach, **'Tekshirish'** tugmasini bosing:",
            reply_markup=markup,
            parse_mode="Markdown"
        )
    else:
        name = message.from_user.first_name
        bot.send_message(
            message.chat.id,
            f"Tabriklayman, {name}! Kino kodini yuboring."
        )

# "Tekshirish" tugmasi
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_inline(call):
    user_id = call.from_user.id
    if check_all_subscriptions(user_id):
        bot.answer_callback_query(call.id, "Rahmat, obuna tasdiqlandi! ✅")
        name = call.from_user.first_name
        bot.send_message(
            call.message.chat.id,
            f"Tabriklayman, {name}! Kino kodini yuboring. Multfilmni ko'rish uchun **6** raqamini yuboring:"
        )
    else:
        bot.answer_callback_query(call.id, "Siz hali hamma kanallarga obuna bo'lmadingiz! ❌", show_alert=True)

# Raqam yuborilganda videolarni to'g'ridan-to'g'ri yuborish
@bot.message_handler(func=lambda message: True)
def get_movie(message):
    user_id = message.from_user.id
    
    if not check_all_subscriptions(user_id):
        bot.send_message(message.chat.id, "Iltimos, avval ko'rsatilgan **ikkala kanalga** ham obuna bo'ling va /start buyrug'ini bosing.")
        return

    code = message.text.strip()
    
    if code in MOVIES:
        bot.send_message(message.chat.id, "Mana siz so'ragan multfilmning 11 ta qismi:")
        for msg_id in MOVIES[code]:
            try:
                # Videolarni yopiq kanaldan to'g'ridan-to'g'ri foydalanuvchiga nusxalab yuborish
                bot.copy_message(chat_id=message.chat.id, from_chat_id=PRIVATE_CHANNEL_ID, message_id=msg_id)
            except Exception as e:
                print(f"Xatolik: {e}")
    else:
        bot.send_message(message.chat.id, "Bunday raqamdagi kino topilmadi. To'g'ri kodni yuboring (Masalan: **6**).")

print("Kino boti ishga tushdi...")
bot.infinity_polling()