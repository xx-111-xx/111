import os
import telebot
import requests
from user_agent import generate_user_agent
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ضع التوكن في متغير بيئة بدلاً من كتابته مباشرة هنا
BOT_TOKEN = "8750258803:AAGtg9YU0MfXt5_fzEE-fndJg-XGeEKkOw4"
bot = telebot.TeleBot(BOT_TOKEN)


def get_main_menu():
    markup = InlineKeyboardMarkup()

    row1 = [
        InlineKeyboardButton("👁️ مشـاهدات انستا", callback_data="1"),
        InlineKeyboardButton("❤️ لايكات انستا", callback_data="2")
    ]
    row2 = [
        InlineKeyboardButton("💾 حفظ انستا", callback_data="3"),
        InlineKeyboardButton("📸 مشاهدات ستوري", callback_data="4")
    ]
    row3 = [
        InlineKeyboardButton("📱 لايكات تيك توك (محظور مؤقتًا)", callback_data="5"),
        InlineKeyboardButton("⚡ مشاهدات تيك توك (محظور مؤقتًا)", callback_data="6")
    ]
    # القسم الجديد: تنزيل فيديوهات بدون علامة مائية
    row4 = [
        InlineKeyboardButton("⬇️ قسم تنزيل الفيديوهات", callback_data="dl_menu")
    ]
    row5 = [
        InlineKeyboardButton("👨‍💻 التواصل مع المطور @U_10V", url="https://t.me/U_10V")
    ]

    markup.row(*row1)
    markup.row(*row2)
    markup.row(*row3)
    markup.row(*row4)
    markup.row(*row5)
    return markup


def get_download_menu():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🎵 تيك توك", callback_data="dl_tiktok")
    )
    markup.row(
        InlineKeyboardButton("🎬 ريلز انستا", callback_data="dl_ig_reel"),
        InlineKeyboardButton("📸 ستوري انستا", callback_data="dl_ig_story")
    )
    markup.row(
        InlineKeyboardButton("🔙 رجوع", callback_data="dl_back")
    )
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
    if "http" in call.data:
        return  # تجنب تداخل زر المبرمج

    if call.data == "dl_menu":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "⬇️ **اختر المنصة التي تريد التنزيل منها:**",
            reply_markup=get_download_menu()
        )
        return

    if call.data == "dl_back":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "اختر الخدمة:", reply_markup=get_main_menu())
        return

    if call.data.startswith("dl_"):
        platform_names = {
            "dl_tiktok": "تيك توك",
            "dl_ig_reel": "ريلز انستا",
            "dl_ig_story": "ستوري انستا",
        }
        platform_descriptions = {
            "dl_tiktok": "🎵 **تنزيل تيك توك**\nيرسل الرابط ويعيد لك الفيديو بأعلى جودة بدون علامة مائية.",
            "dl_ig_reel": "🎬 **تنزيل ريلز انستا**\nيعمل فقط مع حسابات عامة (Public).",
            "dl_ig_story": "📸 **تنزيل ستوري انستا**\nيعمل فقط إذا كان الحساب عام والستوري لا يزال متاحًا.",
        }
        platform = call.data
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            f"{platform_descriptions.get(platform, '')}\n\n🔗 **أرسل رابط {platform_names.get(platform, '')} الآن**",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler(call.message, process_download, platform=platform)
        return

    if call.data in ("5", "6"):
        bot.answer_callback_query(call.id, "هذه الخدمة محظورة مؤقتًا")
        bot.send_message(
            call.message.chat.id,
            "⛔ **هذه الخدمة محظورة مؤقتًا حاليًا وسيتم إعادة تفعيلها لاحقًا.**"
        )
        return

    service_descriptions = {
        "1": "👁️ **مشاهدات انستا**\nيرسل مشاهدات مجانية لفيديو أو ريلز انستا الذي ترسل رابطه.",
        "2": "❤️ **لايكات انستا**\nيرسل لايكات مجانية على منشور انستا الذي ترسل رابطه.",
        "3": "💾 **حفظ انستا**\nيزيد عدد مرات الحفظ (Saves) لمنشور انستا الذي ترسل رابطه.",
        "4": "📸 **مشاهدات ستوري**\nيرسل مشاهدات لستوري انستا (يجب أن يكون الستوري لا يزال متاحًا).",
    }

    bot.answer_callback_query(call.id, "جاري تحضير الخادم...")
    bot.send_message(
        call.message.chat.id,
        f"{service_descriptions.get(call.data, '')}\n\n📥 **تم تحديد الخدمة بنجاح.**\nيرجى إرسال الرابط المباشر للمنشور الآن:",
        parse_mode="Markdown"
    )
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


def _download_with_ytdlp(url):
    """
    تنزيل عام عبر yt-dlp (تيك توك أو انستا) — يختار أعلى جودة فيديو+صوت
    متاحة تلقائيًا. أكثر ثباتًا من الاعتماد على مواقع API خارجية لأن
    yt-dlp مكتبة مفتوحة المصدر تُحدَّث باستمرار لمواكبة تغييرات المنصات.
    تتطلب: pip install -U yt-dlp

    ملاحظة: على Termux مجلد /tmp غالبًا غير قابل للكتابة (Permission denied)،
    لذلك نستخدم مجلدًا داخل المسار الشخصي للمستخدم بدلاً منه.
    """
    import yt_dlp
    import uuid

    downloads_dir = os.path.join(os.path.expanduser("~"), "bot_downloads")
    os.makedirs(downloads_dir, exist_ok=True)

    out_path = os.path.join(downloads_dir, f"{uuid.uuid4().hex}.mp4")
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": out_path,
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if os.path.exists(out_path):
        return out_path
    return None


def download_tiktok(url):
    """تيك توك بأعلى جودة، بدون علامة مائية، عبر yt-dlp."""
    return _download_with_ytdlp(url)


def download_instagram(url):
    """
    انستا (ريلز/ستوري) بأعلى جودة عبر yt-dlp.
    ملاحظة: الستوري يعمل فقط إذا كان الحساب عام (public) والستوري لا يزال
    متاحًا (لم تنتهِ مدته). الحسابات الخاصة تحتاج كوكيز تسجيل دخول ولا
    ندعمها هنا لأسباب تتعلق بالخصوصية والأمان.
    """
    return _download_with_ytdlp(url)


def process_download(message, platform):
    """
    راوتر التنزيل: يوجّه الرابط المُرسل إلى دالة التنزيل المناسبة حسب المنصة
    المختارة من القائمة (تيك توك / ريلز انستا / ستوري انستا) بأعلى جودة متاحة.
    """
    url = message.text.strip()
    msg = bot.reply_to(message, "⏳ **جاري تحضير الفيديو بأعلى جودة...**")
    local_file = None

    try:
        if platform == "dl_tiktok":
            local_file = download_tiktok(url)
        elif platform in ("dl_ig_reel", "dl_ig_story"):
            local_file = download_instagram(url)

        if local_file:
            bot.delete_message(message.chat.id, msg.message_id)
            with open(local_file, "rb") as f:
                bot.send_video(message.chat.id, f, caption="✅ **تم التنزيل بنجاح بأعلى جودة وبدون علامة مائية.**\n👨‍💻 @U_10V")
        else:
            bot.edit_message_text(
                "❌ **تعذر تنزيل هذا الرابط.**\nتأكد أن الرابط صحيح ومتاح للعامة.",
                message.chat.id, msg.message_id
            )

    except Exception as e:
        bot.edit_message_text(f"⚠️ **فشل التنزيل:**\n`{e}`", message.chat.id, msg.message_id, parse_mode="Markdown")

    finally:
        if local_file and os.path.exists(local_file):
            os.remove(local_file)


bot.polling()
