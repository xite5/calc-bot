import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# استبدل النص التالي بالتوكن الحقيقي للبوت الخاص بك الذي أخذته من BotFather
TOKEN = "9125288758:AAFFR_nB783nhPi4hHx5IrcLtEH9RpNOshU"
bot = telebot.TeleBot(TOKEN)

# قاموس لتخزين العمليات الحسابية لكل مستخدم على حدة
user_calculations = {}

# رسالة البداية أو عند طلب الحاسبة
@bot.message_handler(commands=['start', 'calculator', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    user_calculations[chat_id] = ""
    markup = get_calculator_markup()
    bot.send_message(
        chat_id, 
        "🧮 **أهلاً بك في بوت الحاسبة التفاعلي!**\n\nالشاشة: `0`", 
        parse_mode="Markdown", 
        reply_markup=markup
    )

# تصميم أزرار الحاسبة الشبيهة بالحاسبة الحقيقية
def get_calculator_markup():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("C", callback_data="calc_clear"),
        InlineKeyboardButton("(", callback_data="calc_("),
        InlineKeyboardButton(")", callback_data="calc_)"),
        InlineKeyboardButton("/", callback_data="calc_/")
    )
    markup.row(
        InlineKeyboardButton("7", callback_data="calc_7"),
        InlineKeyboardButton("8", callback_data="calc_8"),
        InlineKeyboardButton("9", callback_data="calc_9"),
        InlineKeyboardButton("*", callback_data="calc_*")
    )
    markup.row(
        InlineKeyboardButton("4", callback_data="calc_4"),
        InlineKeyboardButton("5", callback_data="calc_5"),
        InlineKeyboardButton("6", callback_data="calc_6"),
        InlineKeyboardButton("-", callback_data="calc_-")
    )
    markup.row(
        InlineKeyboardButton("1", callback_data="calc_1"),
        InlineKeyboardButton("2", callback_data="calc_2"),
        InlineKeyboardButton("3", callback_data="calc_3"),
        InlineKeyboardButton("+", callback_data="calc_+")
    )
    markup.row(
        InlineKeyboardButton("0", callback_data="calc_0"),
        InlineKeyboardButton(".", callback_data="calc_."),
        InlineKeyboardButton("=", callback_data="calc_=")
    )
    return markup

# استقبال ضغطات الأزرار وتحديث الشاشة فوراً
@bot.callback_query_handler(func=lambda call: call.data.startswith('calc_'))
def handle_calculator(call):
    chat_id = call.message.chat.id
    action = call.data.split('_')[1]
    
    if chat_id not in user_calculations:
        user_calculations[chat_id] = ""
        
    current_expr = user_calculations[chat_id]
    
    if action == 'clear':
        current_expr = ""
    elif action == '=':
        try:
            # حساب النتيجة الرياضية للمعادلة
            result = str(eval(current_expr))
            current_expr = result
        except ZeroDivisionError:
            current_expr = "خطأ: القسمة على صفر"
        except Exception:
            current_expr = "خطأ بالعملية"
    else:
        current_expr += action
         
    user_calculations[chat_id] = current_expr
    display_text = current_expr if current_expr else "0"
    
    # تحديث نص الرسالة لتتغير الشاشة أمام المستخدم كأنها حاسبة حقيقية
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=f"🧮 **حاسبة التيليجرام التفاعلية**\n\nالشاشة: `{display_text}`",
            parse_mode="Markdown",
            reply_markup=get_calculator_markup()
        )
    except Exception:
        pass # لتجنب الأخطاء في حال ضغط المستخدم على نفس الزر ولم يتغير النص

# تشغيل البوت في الخلفية عبر الهاتف
print("Bot is running on phone...")
# استبدل bot.infinity_polling() بهذا الكود لضمان استمرار عمل البوت
if __name__ == '__main__':
    while True:
        try:
            print("Bot is running...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"حدث انقطاع بسيط، جاري إعادة الاتصال... الخطأ: {e}")
            import time
            time.sleep(3)

