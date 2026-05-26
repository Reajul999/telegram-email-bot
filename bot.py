from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from datetime import datetime

BOT_TOKEN = "6806483944:AAH9iZUSbha94raSegHC1SpZfH5UVrI4nrU"

# start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot Active ✅\n\n"
        "Send any message.\n"
        "Use /time for current time."
    )

# time command
async def time_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    await update.message.reply_text(f"Current Time:\n{now}")

# echo message
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"You said:\n{text}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("time", time_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
