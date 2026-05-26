from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import asyncio

# =========================
# BOT INFO
# =========================

BOT_TOKEN = "6806483944:AAH9iZUSbha94raSegHC1SpZfH5UVrI4nrU"

EMAIL = "mdreajul9999@gmail.com"

APP_PASSWORD = "mqlt unop onvb imwk"

# =========================
# STATES
# =========================

NAME, RECEIVER, SUBJECT, MESSAGE, DATETIME = range(5)

user_data_store = {}

# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Send Email"]]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "Welcome to Telegram Email Bot\n\nClick 'Send Email'",
        reply_markup=reply_markup
    )

# =========================
# NAME
# =========================

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter your name:")
    return NAME

async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Receiver Email:")
    return RECEIVER

# =========================
# RECEIVER
# =========================

async def save_receiver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["receiver"] = update.message.text
    await update.message.reply_text("Email Subject:")
    return SUBJECT

# =========================
# SUBJECT
# =========================

async def save_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["subject"] = update.message.text
    await update.message.reply_text("Write your message:")
    return MESSAGE

# =========================
# MESSAGE
# =========================

async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["message"] = update.message.text

    await update.message.reply_text(
        "Enter sending date & time\n\nFormat:\n2026-05-27 10:30"
    )

    return DATETIME

# =========================
# SEND EMAIL
# =========================

async def schedule_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_datetime = update.message.text

    try:
        send_time = datetime.strptime(user_datetime, "%Y-%m-%d %H:%M")

        now = datetime.now()

        delay = (send_time - now).total_seconds()

        if delay <= 0:
            await update.message.reply_text(
                "Time already passed."
            )
            return ConversationHandler.END

        asyncio.create_task(
            delayed_email(context.user_data, delay)
        )

        await update.message.reply_text(
            f"Email scheduled successfully!\n\nSending at: {send_time}"
        )

    except:
        await update.message.reply_text(
            "Wrong format.\nUse:\n2026-05-27 10:30"
        )

    return ConversationHandler.END

# =========================
# DELAYED EMAIL
# =========================

async def delayed_email(data, delay):
    await asyncio.sleep(delay)

    sender_name = data["name"]
    receiver = data["receiver"]
    subject = data["subject"]
    message_text = data["message"]

    msg = MIMEMultipart()

    msg["From"] = EMAIL
    msg["To"] = receiver
    msg["Subject"] = subject

    body = f"""
Sender: {sender_name}

Message:
{message_text}
"""

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(EMAIL, APP_PASSWORD)

        server.send_message(msg)

        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print("Error:", e)

# =========================
# CANCEL
# =========================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

# =========================
# MAIN
# =========================

def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_name
            )
        ],

        states={

            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_name
                )
            ],

            RECEIVER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_receiver
                )
            ],

            SUBJECT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_subject
                )
            ],

            MESSAGE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_message
                )
            ],

            DATETIME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    schedule_email
                )
            ],
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    print("Bot running...")

    app.run_polling()

# =========================

if __name__ == "__main__":
    main()
