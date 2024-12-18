import os
from telegram import Update
from telegram.ext import CallbackContext
from .models import TGUser, Images
from django.core.files import File

# Ensure the 'media' folder exists
if not os.path.exists('media'):
    os.makedirs('media')


async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    db_user = TGUser.objects.filter(user_id=user.id).first()
    if db_user is None:
        TGUser.objects.create(user_id=user.id)
    await update.message.reply_text(f"Hi, {user.first_name}!, i can download images/files and show them on an admin panel")


async def document_handler(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user

    # Get the document object
    document = update.message.document

    # Get the file ID and file
    file = await document.get_file()

    # Save the file inside the 'media' folder
    file_path = os.path.join('media', document.file_name)

    # Download the file to the local storage in the 'media' folder
    await file.download_to_drive(file_path)

    # Open the file and save it in Django model
    with open(file_path, 'rb') as f:
        django_file = File(f)
        image_instance = Images.objects.create(user_id=user.id, image=django_file)
    # Send the message after the download is complete
    await update.message.reply_text(f"Download completed! File saved as {file_path}")


async def message_handler(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user

    # Check if the message contains a photo
    if update.message.photo:
        # Get the largest photo
        photo = update.message.photo[-1]  # The last element is usually the largest resolution
        # Get the file ID and the file
        file = await photo.get_file()

        # Define the path where the image will be saved
        file_path = os.path.join('media', f"{photo.file_id}.jpg")

        # Download the image to the local storage in the 'media' folder
        await file.download_to_drive(file_path)

        # Open the file and save it in Django model
        with open(file_path, 'rb') as f:
            django_file = File(f)
            image_instance = Images.objects.create(user_id=user.id, image=django_file)

        # Notify the user that the image has been downloaded
        await update.message.reply_text(f"Image downloaded and saved")
    else:
        await update.message.reply_text("Send me Files so that i can download them on an admin panel")