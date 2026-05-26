from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

BOT_TOKEN = "6806483944:AAH9iZUSbha94raSegHC1SpZfH5UVrI4nrU"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot is Active ✅\n\nUse /time to see current time."
    )


async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    await update.message.reply_text(f"Current Time:\n{current}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"You said:\n{update.message.text}"
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("time", time_command))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    )

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
