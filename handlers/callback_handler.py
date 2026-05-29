from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from utils.temp_storage import pending_transcriptions
from services.google_sheets_service import save_transcription
from services.task_parser import parse_tasks
from services.database import get_employee

router = Router()

@router.message(Command('start'))

async def start(message):
    await message.answer("Это бот который умеет переводить\n аудио в текст и добавлять задачи в гугл таблицу")


@router.callback_query()
async def confirm_transcription(
    callback: CallbackQuery
):

    user_id = callback.from_user.id

    if callback.data == "confirm_yes":

        text = pending_transcriptions.get(user_id)

        if text:

            username = (
                callback.from_user.username
                or callback.from_user.full_name
            )

            save_transcription(
                username=username,
                text=text
            )
            tasks = parse_tasks(text)

            for item in tasks:

                employee = get_employee(
                    item["name"]
                )

                if employee:
                    telegram_id, username = employee

                    await callback.bot.send_message(
                        telegram_id,
                        (
                            "📌 Новая задача\n\n"
                            f"{item['task']}"
                        )
                    )

            del pending_transcriptions[user_id]

            await callback.message.edit_text(
                "✅ Текст сохранён в Google Sheets по ссылке:\n https://docs.google.com/spreadsheets/d/15sV58mArsQq-e_pgBWxXCQbNGyhCiC5c0xLWLSlPHP8/edit?hl=ru&gid=0#gid=0"
            )

    elif callback.data == "confirm_no":

        if user_id in pending_transcriptions:
            del pending_transcriptions[user_id]

        await callback.message.edit_text(
            "❌ Отправьте голосовое сообщение ещё раз"
        )

    await callback.answer()
