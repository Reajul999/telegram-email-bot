from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from datetime import datetime

BOT_TOKEN = "6806483944:AAH9iZUSbha94raSegHC1SpZfH5UVrI4nrU"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot Active ✅"
    )


async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    await update.message.reply_text(current_time)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("time", time_command))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    )

    print("Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
