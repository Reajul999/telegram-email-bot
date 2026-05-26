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

NAME, EMAIL_ID, MESSAGE, DATE_TIME = range(4)

# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome!\n\nSend your name:"
    )
    return NAME

# =========================
# NAME
# =========================

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "Send receiver email:"
    )
    return EMAIL_ID

# =========================
# EMAIL
# =========================

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["receiver"] = update.message.text

    await update.message.reply_text(
        "Send your message:"
    )
    return MESSAGE

# =========================
# MESSAGE
# =========================

async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["message"] = update.message.text

    await update.message.reply_text(
        "Send date & time like:\n\n2026-05-27 10:30"
    )
    return DATE_TIME

# =========================
# DATE & TIME
# =========================

async def get_datetime(update: Update, context: ContextTypes.DEFAULT_TYPE):

    date_time_text = update.message.text

    try:
        send_time = datetime.strptime(date_time_text, "%Y-%m-%d %H:%M")

    except:
        await update.message.reply_text(
            "Wrong format!\nUse:\n2026-05-27 10:30"
        )
        return DATE_TIME

    now = datetime.now()

    delay = (send_time - now).total_seconds()

    if delay <= 0:
        await update.message.reply_text(
            "Time already passed."
        )
        return DATE_TIME

    await update.message.reply_text(
        f"Email scheduled successfully!\n\nWill send at:\n{send_time}"
    )

    asyncio.create_task(
        schedule_email(
            context.user_data["receiver"],
            context.user_data["message"],
            context.user_data["name"],
            delay,
        )
    )

    return ConversationHandler.END

# =========================
# SEND EMAIL
# =========================

async def schedule_email(receiver, message, sender_name, delay):

    await asyncio.sleep(delay)

    try:

        msg = MIMEMultipart()

        msg["From"] = EMAIL
        msg["To"] = receiver
        msg["Subject"] = "Message From Telegram Bot"

        body = f"""
Sender: {sender_name}

Message:
{message}
"""

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(EMAIL, APP_PASSWORD)

        server.sendmail(
            EMAIL,
            receiver,
            msg.as_string()
        )

        server.quit()

        print("Email Sent Successfully")

    except Exception as e:
        print("Error:", e)

# =========================
# CANCEL
# =========================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Cancelled."
    )
    return ConversationHandler.END

# =========================
# MAIN
# =========================

app = ApplicationBuilder().token(BOT_TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],

    states={
        NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)
        ],

        EMAIL_ID: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)
        ],

        MESSAGE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_message)
        ],

        DATE_TIME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_datetime)
        ],
    },

    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)

print("Bot Running...")

app.run_polling()
