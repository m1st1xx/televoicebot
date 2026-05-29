from aiogram import Router, F
from aiogram.types import Message

from utils.temp_storage import (
    editing_users,
    pending_transcriptions
)

from services.google_sheets_service import (
    save_transcription
)

from services.task_parser import (
    extract_tasks
)

from services.database import (
    get_employee
)


router = Router()


@router.message(F.text)
async def handle_edited_text(
    message: Message
):

    user_id = message.from_user.id

    if user_id not in editing_users:
        return

    edited_text = message.text

    pending_transcriptions[user_id] = edited_text

    username = (
        message.from_user.username
        or message.from_user.full_name
    )

    # Сохраняем в Google Sheets
    save_transcription(
        username=username,
        text=edited_text
    )

    # Парсим задачи
    tasks = extract_tasks(edited_text)

    # Рассылаем задачи
    for item in tasks:

        employee = get_employee(
            item["name"]
        )

        if employee:

            telegram_id, tg_username = employee

            await message.bot.send_message(
                telegram_id,
                (
                    "📌 Новая задача\n\n"
                    f"{item['task']}"
                )
            )

    editing_users.remove(user_id)

    del pending_transcriptions[user_id]

    await message.answer(
        "✅ Исправленный текст сохранён"
    )