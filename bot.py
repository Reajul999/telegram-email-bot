from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)

import smtplib
import asyncio
from email.mime.text import MIMEText
from datetime import datetime

# ====================================
# YOUR INFO
# ====================================

BOT_TOKEN = "6806483944:AAH9iZUSbha94raSegHC1SpZfH5UVrI4nrU"

EMAIL = "mdreajul9999@gmail.com"

APP_PASSWORD = "mqlt unop onvb imwk"

# ====================================
# STATES
# ====================================

(
    NAME,
    RELATION,
    STYLE,
    EMAIL_ID,
    MESSAGE_TYPE,
    CUSTOM_MESSAGE,
    SEND_TYPE,
    SCHEDULE_TIME
) = range(8)

# ====================================
# START
# ====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Welcome ❤️\n\nUse /addperson"
    )

# ====================================
# ADD PERSON
# ====================================

async def addperson(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "Enter Name:"
    )

    return NAME

# ====================================
# NAME
# ====================================

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "Relation?"
    )

    return RELATION

# ====================================
# RELATION
# ====================================

async def get_relation(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["relation"] = update.message.text

    await update.message.reply_text(
        "Message Style?\n\nemotional / funny / caring"
    )

    return STYLE

# ====================================
# STYLE
# ====================================

async def get_style(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["style"] = update.message.text

    await update.message.reply_text(
        "Enter Receiver Email:"
    )

    return EMAIL_ID

# ====================================
# EMAIL
# ====================================

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["email"] = update.message.text

    await update.message.reply_text(
        "Message Type?\n\n1 = Template Message\n2 = Custom Message"
    )

    return MESSAGE_TYPE

# ====================================
# MESSAGE TYPE
# ====================================

async def get_message_type(update: Update, context: ContextTypes.DEFAULT_TYPE):

    choice = update.message.text

    if choice == "1":

        context.user_data["custom_message"] = None

        await update.message.reply_text(
            "Send Type?\n\n1 = Instant\n2 = Scheduled"
        )

        return SEND_TYPE

    elif choice == "2":

        await update.message.reply_text(
            "Write Your Custom Message:"
        )

        return CUSTOM_MESSAGE

    else:

        await update.message.reply_text(
            "Please type 1 or 2"
        )

        return MESSAGE_TYPE

# ====================================
# CUSTOM MESSAGE
# ====================================

async def get_custom_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["custom_message"] = update.message.text

    await update.message.reply_text(
        "Send Type?\n\n1 = Instant\n2 = Scheduled"
    )

    return SEND_TYPE

# ====================================
# SEND TYPE
# ====================================

async def get_send_type(update: Update, context: ContextTypes.DEFAULT_TYPE):

    choice = update.message.text

    data = context.user_data

    if data["custom_message"]:

        message = data["custom_message"]

    else:

        message = create_template_message(
            data["name"],
            data["relation"],
            data["style"]
        )

    # ==========================
    # INSTANT
    # ==========================

    if choice == "1":

        send_email(
            data["email"],
            message
        )

        context.user_data.clear()

        await update.message.reply_text(
            "Email Sent Successfully ✅\n\nSend another email?\nUse /addperson ❤️"
        )

        return ConversationHandler.END

    # ==========================
    # SCHEDULE
    # ==========================

    elif choice == "2":

        context.user_data["final_message"] = message

        await update.message.reply_text(
            "Enter Time Like:\n21:30"
        )

        return SCHEDULE_TIME

    else:

        await update.message.reply_text(
            "Please type 1 or 2"
        )

        return SEND_TYPE

# ====================================
# SCHEDULE TIME
# ====================================

async def get_schedule_time(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        time_text = update.message.text

        now = datetime.now()

        target = datetime.strptime(
            time_text,
            "%H:%M"
        )

        scheduled_time = now.replace(
            hour=target.hour,
            minute=target.minute,
            second=0,
            microsecond=0
        )

        delay = (scheduled_time - now).total_seconds()

        if delay < 0:
            delay += 86400

        receiver = context.user_data["email"]

        message = context.user_data["final_message"]

        asyncio.create_task(
            delayed_email(
                delay,
                receiver,
                message
            )
        )

        context.user_data.clear()

        await update.message.reply_text(
            f"Scheduled Successfully ✅\n\nEmail will send at {time_text}"
        )

        return ConversationHandler.END

    except:

        await update.message.reply_text(
            "Wrong Time Format ❌\nExample: 21:30"
        )

        return SCHEDULE_TIME

# ====================================
# TEMPLATE MESSAGE
# ====================================

def create_template_message(name, relation, style):

    style = style.lower()

    if style == "emotional":

        return f"""
Hello {name} ❤️

You are truly special to me.

I hope your day becomes beautiful and full of happiness ✨
"""

    elif style == "funny":

        return f"""
Hello {name} 😂

Life is short.

Eat more biryani and smile more 😆
"""

    else:

        return f"""
Hello {name} 💖

Take care of yourself always.

Stay happy and safe ✨
"""

# ====================================
# SEND EMAIL
# ====================================

def send_email(receiver, message):

    msg = MIMEText(message)

    msg["Subject"] = "Special Message ❤️"

    msg["From"] = EMAIL

    msg["To"] = receiver

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        EMAIL,
        APP_PASSWORD
    )

    server.sendmail(
        EMAIL,
        receiver,
        msg.as_string()
    )

    server.quit()

# ====================================
# DELAYED EMAIL
# ====================================

async def delayed_email(delay, receiver, message):

    await asyncio.sleep(delay)

    send_email(receiver, message)

# ====================================
# CANCEL
# ====================================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "Cancelled ❌"
    )

    return ConversationHandler.END

# ====================================
# MAIN
# ====================================

app = ApplicationBuilder().token(
    BOT_TOKEN
).build()

conv_handler = ConversationHandler(

    entry_points=[
        CommandHandler(
            "addperson",
            addperson
        )
    ],

    states={

        NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_name
            )
        ],

        RELATION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_relation
            )
        ],

        STYLE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_style
            )
        ],

        EMAIL_ID: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_email
            )
        ],

        MESSAGE_TYPE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_message_type
            )
        ],

        CUSTOM_MESSAGE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_custom_message
            )
        ],

        SEND_TYPE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_send_type
            )
        ],

        SCHEDULE_TIME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_schedule_time
            )
        ]
    },

    fallbacks=[
        CommandHandler(
            "cancel",
            cancel
        )
    ]
)

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(conv_handler)

print("Bot Running ✅")

app.run_polling()
