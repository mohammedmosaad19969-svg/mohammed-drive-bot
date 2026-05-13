import os
import asyncio
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

current_projects = {}
current_clients = {}
media_groups = {}


# =========================
# PROJECT COMMAND
# =========================

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


# =========================
# CLIENT COMMAND
# =========================

async def start_client(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    client_name = " ".join(context.args)

    if not client_name:
        await update.message.reply_text(
            "❌ استخدم:\n/client Client Name"
        )
        return

    current_clients[user_id] = client_name

    await update.message.reply_text(
        f"👤 Current Client:\n{client_name}"
    )


# =========================
# END PROJECT
# =========================

async def end_project(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id in current_projects:
        del current_projects[user_id]

    await update.message.reply_text(
        "🛑 Project Closed"
    )


# =========================
# SEARCH COMMAND
# =========================

async def search_project(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = " ".join(context.args)

    await update.message.reply_text(
        f"🔎 Search Ready\nKeyword: {query}"
    )


# =========================
# AUTO TAGGING
# =========================

def generate_tags(filename=""):

    filename = filename.lower()

    tags = []

    if "ugc" in filename:
        tags.append("#UGC")

    if "asmr" in filename:
        tags.append("#ASMR")

    if "cinematic" in filename:
        tags.append("#Cinematic")

    if "product" in filename:
        tags.append("#ProductShot")

    if "hook" in filename:
        tags.append("#Hook")

    return " ".join(tags)


# =========================
# SAVE FILES
# =========================

async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user_id = update.effective_user.id

    project_name = current_projects.get(
        user_id,
        "Untitled Project"
    )

    client_name = current_clients.get(
        user_id,
        "No Client"
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    filename = ""

    if update.message.document:
        filename = update.message.document.file_name or ""

    tags = generate_tags(filename)

    caption = (
        f"📁 {project_name}\n"
        f"👤 {client_name}\n"
        f"🕒 {now}\n\n"
        f"{tags}"
    )

    try:

        # =========================
        # ALBUM HANDLING
        # =========================

        if update.message.media_group_id:

            group_id = update.message.media_group_id

            if group_id not in media_groups:
                media_groups[group_id] = []

            media_groups[group_id].append(update.message)

            await asyncio.sleep(2)

            if len(media_groups[group_id]) > 0:

                first = media_groups[group_id][0]

                await context.bot.copy_message(
                    chat_id=CHANNEL_ID,
                    from_chat_id=first.chat_id,
                    message_id=first.message_id,
                    caption=caption
                )

                for msg in media_groups[group_id][1:]:

                    await context.bot.copy_message(
                        chat_id=CHANNEL_ID,
                        from_chat_id=msg.chat_id,
                        message_id=msg.message_id
                    )

                del media_groups[group_id]

                await update.message.reply_text(
                    f"✅ Album Saved\n📁 {project_name}"
                )

                return

        # =========================
        # SINGLE PHOTO
        # =========================

        elif update.message.photo:

            await context.bot.copy_message(
                chat_id=CHANNEL_ID,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id,
                caption=caption
            )

        # =========================
        # VIDEO
        # =========================

        elif update.message.video:

            await context.bot.copy_message(
                chat_id=CHANNEL_ID,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id,
                caption=caption
            )

        # =========================
        # DOCUMENT
        # =========================

        elif update.message.document:

            await context.bot.copy_message(
                chat_id=CHANNEL_ID,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id,
                caption=caption
            )

        else:
            return

        await update.message.reply_text(
            f"✅ Saved Successfully\n📁 {project_name}"
        )

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )


# =========================
# BUILD APP
# =========================

app = ApplicationBuilder().token(BOT_TOKEN).build()


# COMMANDS
app.add_handler(CommandHandler("project", start_project))
app.add_handler(CommandHandler("client", start_client))
app.add_handler(CommandHandler("end", end_project))
app.add_handler(CommandHandler("search", search_project))


# FILES
app.add_handler(
    MessageHandler(filters.ALL, save_file)
)

print("🚀 Ultimate AI Drive Running")

app.run_polling()
