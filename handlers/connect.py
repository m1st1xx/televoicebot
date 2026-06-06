from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.temp_storage import pending_sheet_connection

router = Router()


@router.message(Command("connect"))
async def connect_sheet(message: Message):

    pending_sheet_connection.add(message.from_user.id)

    await message.answer(
        "📊 Подключение Google Таблицы\n\n"
        "1. Создайте Google Таблицу.\n\n"
        "2. Нажмите 'Настройки доступа'.\n\n"
        "3. Добавьте пользователя:\n\n"
        "alex-792@telegr-497211.iam.gserviceaccount.com\n\n"
        "с правами 'Редактор'.\n\n"
        "4. Отправьте мне ссылку на таблицу следующим сообщением."
    )