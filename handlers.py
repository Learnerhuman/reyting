from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler,
    filters, ConversationHandler
)

GET_CONTACT, GET_NAME = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_button = KeyboardButton("📱 Raqamimni yuborish", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True)

    await update.message.reply_text(
        "Raqamingizni yuborish uchun tugmani bosing:",
        reply_markup=reply_markup
    )
    return GET_CONTACT

async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    context.user_data["phone"] = contact.phone_number

    await update.message.reply_text("Endi ism va familiyangizni kiriting (masalan: Ozodbek Abdusattorov):")
    return GET_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    full_name = update.message.text
    phone = context.user_data.get("phone", "Noma'lum")

    await update.message.reply_text(f"✅ Ma'lumotlar:\n👤 Ism: {full_name}\n📞 Raqam: {phone}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Jarayon bekor qilindi.")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        GET_CONTACT: [MessageHandler(filters.CONTACT, get_contact)],
        GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app = ApplicationBuilder().token("8201520268:AAFM28fe_L4wt-Hdz373ZX5pDUIqP0kHiHs").build()
app.add_handler(conv_handler)

app.run_polling()

