import telebot
import requests
from user_agent import generate_user_agent
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot("8750258803:AAGtg9YU0MfXt5_fzEE-fndJg-XGeEKkOw4")

def get_main_menu():
    markup = InlineKeyboardMarkup()
    
    # تنظيم الأزرار في صفوف (كل زرين بجانب بعض)
    row1 = [
        InlineKeyboardButton("👁️ مشـاهدات انستا", callback_data="1"),
        InlineKeyboardButton("❤️ لايكات انستا", callback_data="2")
    ]
    row2 = [
        InlineKeyboardButton("💾 حفظ انستا", callback_data="3"),
        InlineKeyboardButton("📸 مشاهدات ستوري", callback_data="4")
    ]
    row3 = [
        InlineKeyboardButton("📱 لايكات تيك توك", callback_data="5"),
        InlineKeyboardButton("⚡ مشاهدات تيك توك", callback_data="6")
    ]
    # زر التواصل بشكل منفرد في الأسفل
    row4 = [
        InlineKeyboardButton("👨‍💻 التواصل مع المطور @U_10V", url="https://t.me/U_10V")
    ]
    
    markup.row(*row1)
    markup.row(*row2)
    markup.row(*row3)
    markup.row(*row4)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "✨ **مرحباً بك في [بوت رشق انستا+تيك توك ]**\n\n"
        "نحن نمنحك القوة لتعزيز حضورك الرقمي بكفاءة عالية.\n"
        "الرجاء اختيار الخدمة التي ترغب في تفعيلها:\n\n"
        "ملاحظه البوت قيد التطوير لتحسين الخدمات ومعالجه الطلبات بسرعه"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if "http" in call.data: return # تجنب تداخل زر المبرمج
    bot.answer_callback_query(call.id, "جاري تحضير الخادم...")
    bot.send_message(call.message.chat.id, "📥 **تم تحديد الخدمة بنجاح.**\nيرجى إرسال الرابط المباشر للمنشور الآن:")
    bot.register_next_step_handler(call.message, process_request, service_id=call.data)

def process_request(message, service_id):
    target = message.text
    msg = bot.reply_to(message, "⏳ **جاري الربط مع الخوادم...**")
    
    try:
        ua = str(generate_user_agent())
        services = {
            '1': ('https://leofame.com/ar/free-instagram-views', {'quantity': '200', 'speed': '-1'}),
            '2': ('https://leofame.com/ar/free-instagram-likes', {'speed': '-1'}),
            '3': ('https://leofame.com/ar/free-instagram-saves', {'quantity': '30', 'speed': '-1'}),
            '4': ('https://leofame.com/ar/free-instagram-story-views', {}),
            '5': ('https://leofame.com/ar/free-tiktok-likes', {'quantity': '100'}),
            '6': ('https://leofame.com/ar/free-tiktok-views', {})
        }
        
        url, extra_data = services[service_id]
        res = requests.get(url)
        data = {'token': res.cookies.get_dict()['token'], 'free_link': target}
        data.update(extra_data)
        
        resp = requests.post(url, cookies=res.cookies, data=data, headers={'user-agent': ua})
        
        if 'success' in resp.text:
            bot.edit_message_text("✅ **تم قبول الطلب.**\nسيبدأ النظام في تنفيذ العملية خلال دقائق.", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ **عذراً، الخادم مشغول.**\nيرجى المحاولة لاحقاً.", message.chat.id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"⚠️ **فشل الاتصال بالخادم:**\n`{e}`", message.chat.id, msg.message_id, parse_mode="Markdown")

bot.polling()
