import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 🔑 CONFIG
BOT_TOKEN = "AAG8XCQF_uFpK6JoN6SHRRWfWMC-3Rq1Vuo"
FOLDER_ID = "1PAs718ZcdbwOeQm8J93tAxg1bh2hd-87"

# JSON file name
SERVICE_ACCOUNT_FILE = "service_account.json"

# Google Drive setup
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/drive"]
)

drive_service = build("drive", "v3", credentials=credentials)

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if message.video:
        file = await message.video.get_file()
        file_name = "video.mp4"
    elif message.document:
        file = await message.document.get_file()
        file_name = message.document.file_name
    else:
        return

    await file.download_to_drive(file_name)

    media = MediaFileUpload(file_name, resumable=True)
    file_metadata = {
        "name": file_name,
        "parents": [FOLDER_ID]
    }

    drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    await message.reply_text("✅ Uploaded to Drive!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_file))
    app.run_polling()

if __name__ == "__main__":
    main()
