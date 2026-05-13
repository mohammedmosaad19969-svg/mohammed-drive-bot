import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from datetime import datetime

BOT_TOKEN = os.getenv("8319848858:AAEHrur1oWNjFtGM548heLcRycAaRQ0FBiQ")
CHANNEL_ID = "@mohammeddrivevault"

async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    caption = f"📁 Uploaded\n🕒 {now}"

    try:

        if update.message.photo:
            await update.message.forward(chat_id=CHANNEL_ID)
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=f"🖼️ Image Saved\n{caption}\n#image"
            )

        elif update.message.video:
            await update.message.forward(chat_id=CHANNEL_ID)
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=f"🎬 Video Saved\n{caption}\n#video"
            )

        elif update.message.document:
            await update.message.forward(chat_id=CHANNEL_ID)
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=f"📦 File Saved\n{caption}\n#file"
            )

        else:
            await update.message.forward(chat_id=CHANNEL_ID)

        await update.message.reply_text("✅ Saved To Mohammed Drive")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.ALL, save_file))

print("🚀 Mohammed Drive Running")

app.run_polling()
