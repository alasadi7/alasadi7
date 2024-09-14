import telebot
from telebot import types

# توكن البوت
token = '7295573231:AAEZ6ptBdU2bAtqYiZ64NhHKNh9xX0sVYt0'
# قائمة المشرفين بحد أقصى 2
sudo = [6824730285, 5157353813]
bot = telebot.TeleBot(token)

# قائمة لتخزين ايديات المستخدمين
users = set()

# وظيفة لمعالجة الأمر /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # إضافة المستخدم إلى قائمة المستخدمين
    users.add(user_id)
    
    # التحقق من إذا كان المستخدم مشرف
    if user_id in sudo:
        # عرض الأزرار للمشرفين فقط
        markup = types.InlineKeyboardMarkup()
        broadcast_btn = types.InlineKeyboardButton("إرسال إذاعة", callback_data="broadcast")
        markup.add(broadcast_btn)
        bot.send_message(
            message.chat.id,
            text="<strong>مرحبا بك في بوت تواصل الفرقه المهدويه\n\n اختر أحد الأزرار أدناه:</strong>",
            parse_mode="HTML",
            reply_markup=markup
        )
    else:
        bot.send_message(
            message.chat.id,
            text="<strong>مرحبا بك في بوت تواصل الفرقه المهدويه\n\n أرسل رسالتك وستصل للأدمن.</strong>",
            parse_mode="HTML"
        )

# وظيفة لمعالجة الأزرار
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id

    if user_id in sudo:
        if call.data == "broadcast":
            bot.send_message(
                call.message.chat.id,
                "أرسل الرسالة التي تريد إذاعتها بصيغة /broadcast <message>"
            )
    else:
        bot.answer_callback_query(call.id, "ليس لديك الصلاحية لاستخدام هذا الزر.")

# وظيفة لمعالجة الأوامر من المشرفين
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id in sudo:
        # إرسال رسالة إلى كل المستخدمين
        msg = message.text.split(maxsplit=1)
        if len(msg) > 1:
            message_text = msg[1]
            failed_users = []
            for user_id in users:
                try:
                    bot.send_message(user_id, message_text)
                except Exception as e:
                    failed_users.append(user_id)
            
            if failed_users:
                failed_ids = ", ".join(map(str, failed_users))
                bot.send_message(message.chat.id, f"تم إرسال الرسالة بنجاح إلى بعض المستخدمين، لكن فشلت محاولة إرسالها إلى: {failed_ids}")
            else:
                bot.send_message(message.chat.id, "تم إرسال الرسالة إلى جميع المستخدمين.")
        else:
            bot.send_message(message.chat.id, "استخدم الأمر بهذا الشكل: /broadcast <message>")
    else:
        bot.send_message(message.chat.id, "ليس لديك الصلاحية لاستخدام هذا الأمر.")

# وظيفة لمعالجة جميع الرسائل
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id

    # إرسال تأكيد للمستخدم
    bot.send_message(
        message.chat.id,
        text="<strong>تم إرسال رسالتك للأدمن.</strong>",
        parse_mode="HTML"
    )
    
    # إرسال الرسالة إلى المشرفين
    for admin_id in sudo:
        bot.forward_message(admin_id, message.chat.id, message.message_id)

# بدء البوت
bot.polling(True)