import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if user_id != ADMIN_ID:
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=user_id,
            message_id=update.message.message_id
        )
    elif update.message.reply_to_message and update.message.reply_to_message.forward_from:
        original_user_id = update.message.reply_to_message.forward_from.id
        await context.bot.send_message(chat_id=original_user_id, text=update.message.text)
        await update.message.reply_text("✅ Message sent to user.")

def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    start_bot()
