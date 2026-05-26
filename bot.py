from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime

BOT_TOKEN = "6806483944:AAH9iZUSbha94raSegHC1SpZfH5UVrI4nrU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Active ✅")


async def time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    await update.message.reply_text(now)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("time", time))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
