import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from downloader import download_audio

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Send a YouTube URL for content you own "
        "or have permission to download."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text.strip()

    if "youtube.com/" not in url and "youtu.be/" not in url:
        await update.message.reply_text(
            "❌ Please send a valid YouTube URL."
        )
        return

    await update.message.reply_text(
        "⏳ Downloading audio..."
    )

    
    try:
        audio_file, title = download_audio(url)

        if not os.path.exists(audio_file):
            await update.message.reply_text(
                "❌ Audio file was not found."
            )
            return

        await update.message.reply_text(
            f"✅ Download complete!\n\n🎵 {title}\n\n"
            "📤 Sending audio..."
        )

        with open(audio_file, "rb") as audio:
         await update.message.reply_audio(
        audio=audio,
        title=title,
        caption="🎵 Audio file",
        read_timeout=180,
        write_timeout=180,
        connect_timeout=30,
        pool_timeout=30
    )

        print("Audio sent successfully:", audio_file)

    except Exception as e:
        print("ERROR:", e)

        await update.message.reply_text(
            "❌ Download or sending failed."
        )

    finally:
        # Remove the downloaded MP3, if it exists
        if "audio_file" in locals() and os.path.isfile(audio_file):
            try:
                os.remove(audio_file)
                print("Deleted audio file:", audio_file)
            except OSError as cleanup_error:
                print("Could not delete audio:", cleanup_error)



def main():

    if not TOKEN:
        print("❌ BOT_TOKEN is missing from .env")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("🤖 Telegram bot is connected!")
    print("Waiting for messages...")

    app.run_polling()


if __name__ == "__main__":
    main()