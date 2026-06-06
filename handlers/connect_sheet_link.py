import re

from aiogram import Router, F
from aiogram.types import Message
from utils.temp_storage import pending_sheet_connection
from services.database import update_sheet

router = Router()


@router.message(F.text)
async def process_sheet_link(
    message: Message
):

    user_id = message.from_user.id

    if user_id not in pending_sheet_connection:
        return

    text = message.text.strip()

    match = re.search(
        r"/spreadsheets/d/([a-zA-Z0-9-_]+)",
        text
    )

    if not match:

        await message.answer(
            "❌ Не удалось найти Google Таблицу.\n\n"
            "Отправьте полную ссылку."
        )

        return

    sheet_id = match.group(1)

    update_sheet(telegram_id=user_id,google_sheet_id=sheet_id)

    pending_sheet_connection.remove(
        user_id
    )

    await message.answer(
        "✅ Таблица успешно подключена."
    )