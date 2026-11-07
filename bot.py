
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

MATERIALS = [
    ("grammar", "📗 القواعد"),
    ("literature", "📕 الأدب"),
    ("linguistics", "📘 علم اللغة"),
    ("essay", "📙 المقالة"),
    ("assessment", "📒 القياس والتقويم"),
    ("management", "📔 القيادة والإدارة التربوية"),
    ("teaching", "📓 طرائق التدريس العامة وتطبيقاتها"),
]

# مؤقتاً، الملفات فارغة. سنضيف روابط/ملفات كل كورس لاحقاً.
COURSES = {
    key: [
        ("course1", "🟢 الكورس الأول"),
        ("course2", "🔵 الكورس الثاني"),
    ]
    for key, _ in MATERIALS
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 المواد الدراسية", callback_data="materials")],
        [InlineKeyboardButton("📢 الإعلانات", callback_data="announcements")],
        [InlineKeyboardButton("ℹ️ حول البوت", callback_data="about")],
    ]
    await update.message.reply_text(
        "🎓 أهلاً بك في English Hub\n\n"
        "بوابة طلاب اللغة الإنكليزية\n"
        "اختر من القائمة:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def materials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    keyboard = [
        [InlineKeyboardButton(label, callback_data=f"mat:{key}")]
        for key, label in MATERIALS
    ]
    keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data="home")])
    await q.edit_message_text(
        "📚 المواد الدراسية\n\nاختر المادة:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def material(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    key = q.data.split(":", 1)[1]
    label = dict(MATERIALS)[key]
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"course:{key}:{course_key}")]
        for course_key, name in COURSES[key]
    ]
    keyboard.append([InlineKeyboardButton("⬅️ رجوع للمواد", callback_data="materials")])
    await q.edit_message_text(
        f"{label}\n\nاختر الكورس:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    _, material_key, course_key = q.data.split(":")
    material_label = dict(MATERIALS)[material_key]
    course_label = dict(COURSES[material_key])[course_key]

    # هنا لاحقاً نضع ملفات PDF والكتاب والأسئلة والملخصات.
    await q.edit_message_text(
        f"{material_label} — {course_label}\n\n"
        "📚 الملفات الخاصة بهذا الكورس ستظهر هنا مباشرة.\n\n"
        "🔧 هذه النسخة التجريبية جاهزة لإضافة الملازم والكتب والملخصات والأسئلة.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ رجوع للكورسات", callback_data=f"mat:{material_key}")],
            [InlineKeyboardButton("🏠 الرئيسية", callback_data="home")],
        ])
    )

async def announcements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        "📢 الإعلانات\n\nلا توجد إعلانات حالياً.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 الرئيسية", callback_data="home")]
        ])
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        "ℹ️ حول البوت\n\n"
        "English Hub\n"
        "بوت تعليمي لخدمة طلاب قسم اللغة الإنكليزية.\n\n"
        "نسعى لتجميع الملازم والكتب والملخصات والأسئلة في مكان واحد.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 الرئيسية", callback_data="home")]
        ])
    )

async def home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    keyboard = [
        [InlineKeyboardButton("📚 المواد الدراسية", callback_data="materials")],
        [InlineKeyboardButton("📢 الإعلانات", callback_data="announcements")],
        [InlineKeyboardButton("ℹ️ حول البوت", callback_data="about")],
    ]
    await q.edit_message_text(
        "🎓 English Hub\n\nبوابة طلاب اللغة الإنكليزية\nاختر من القائمة:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    if data == "materials":
        await materials(update, context)
    elif data.startswith("mat:"):
        await material(update, context)
    elif data.startswith("course:"):
        await course(update, context)
    elif data == "announcements":
        await announcements(update, context)
    elif data == "about":
        await about(update, context)
    elif data == "home":
        await home(update, context)

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN غير موجود في متغيرات البيئة.")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_router))
    app.run_polling()

if __name__ == "__main__":
    main()
