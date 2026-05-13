import os
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@mohammeddrivevault"

# حفظ المشروع الحالي لكل يوزر
current_projects = {}


async def start_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    project_name = " ".join(context.args)

    if not project_name:
        await update.message.reply_text(
            "❌ استخدم:\n/project Project Name"
        )
        return

    current_projects[user_id] = project_name

    await update.message.reply_text(
        f"✅ Current Project:\n📁 {project_name}"
    )


async def end_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in current_projects:
        del current_projects[user_id]

    await update.message.reply_text("🛑 Project Closed")


async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user_id = update.effective_user.id

    project_name = current_projects.get(
        user_id,
        "Untitled Project"
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    caption = f"📁 {project_name}\n🕒 {now}"

    try:

        # صور
        if update.message.photo:

            await update.message.forward(
                chat_id=CHANNEL_ID
            )

            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=f"🖼 Image Saved\n{caption}"
            )

        # فيديو
        elif update.message.video:

            await update.message.forward(
                chat_id=CHANNEL_ID
            )

            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=f"🎬 Video Saved\n{caption}"
            )

        # ملفات
        elif update.message.document:

            await update.message.forward(
                chat_id=CHANNEL_ID
            )

            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=f"📦 File Saved\n{caption}"
            )

        # ألبومات
        elif update.message.media_group_id:

            await update.message.forward(
                chat_id=CHANNEL_ID
            )

        else:
            return

        await update.message.reply_text(
            f"✅ Saved To:\n📁 {project_name}"
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error: {e}"
        )


app = ApplicationBuilder().token(BOT_TOKEN).build()

# أوامر المشاريع
app.add_handler(
    CommandHandler("project", start_project)
)

app.add_handler(
    CommandHandler("end", end_project)
)

# استقبال الملفات
app.add_handler(
    MessageHandler(filters.ALL, save_file)
)

print("🚀 Mohammed Drive Running")

app.run_polling()
