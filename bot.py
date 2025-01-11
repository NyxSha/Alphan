import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

# Bot configuration
BOT_TOKEN = "7440221035:AAHFFQnvC0OSlnXWbGzspJNq-AfjarhqXqM"  # Replace with your actual bot token
GROUP_1_USERNAME = "@ssok56"  # Source group username
GROUP_2_ID = -1002454153117  # Destination group chat ID

# Set up logging to see what's happening
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def copy_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Copy messages from one group to another."""
    logger.info(f"Received a message: {update.message}")  # Log incoming messages for debugging

    if update.message:
        try:
            # If it's a text message, copy and send it to Group 2
            if update.message.text:
                logger.info(f"Forwarding text message: {update.message.text}")
                await context.bot.send_message(
                    chat_id=GROUP_2_ID,
                    text=update.message.text,
                    parse_mode=ParseMode.HTML,
                )
            # If the message contains a photo
            elif update.message.photo:
                logger.info("Forwarding photo message")
                await context.bot.send_photo(
                    chat_id=GROUP_2_ID,
                    photo=update.message.photo[-1].file_id,
                    caption=update.message.caption or "",
                    parse_mode=ParseMode.HTML,
                )
            # If the message contains a video
            elif update.message.video:
                logger.info("Forwarding video message")
                await context.bot.send_video(
                    chat_id=GROUP_2_ID,
                    video=update.message.video.file_id,
                    caption=update.message.caption or "",
                    parse_mode=ParseMode.HTML,
                )
            # If the message contains a document
            elif update.message.document:
                logger.info("Forwarding document message")
                await context.bot.send_document(
                    chat_id=GROUP_2_ID,
                    document=update.message.document.file_id,
                    caption=update.message.caption or "",
                    parse_mode=ParseMode.HTML,
                )
            # If the message contains a sticker
            elif update.message.sticker:
                logger.info("Forwarding sticker message")
                await context.bot.send_sticker(
                    chat_id=GROUP_2_ID,
                    sticker=update.message.sticker.file_id,
                )
        except Exception as e:
            logger.error(f"Error forwarding message: {e}")

async def main():
    """Initialize the bot and start polling."""
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add a handler to monitor messages from the source group
    application.add_handler(
        MessageHandler(
            filters.Chat(username=GROUP_1_USERNAME) & filters.ALL,
            copy_message,
        )
    )

    # Run the bot
    await application.run_polling()

# Run the bot
if __name__ == "__main__":
    import asyncio
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(
        MessageHandler(
            filters.Chat(username=GROUP_1_USERNAME) & filters.ALL,
            copy_message,
        )
    )
    application.run_polling()
