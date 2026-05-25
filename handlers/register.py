from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.database import add_employee


router = Router()


@router.message(Command("register"))
async def register_user(
    message: Message
):

    parts = message.text.split()

    if len(parts) < 2:
        await message.answer(
            "Использование: /register Имя"
        )
        return

    name = parts[1]

    add_employee(
        name=name,
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )

    await message.answer(
        f"✅ {name} зарегистрирован"
    )