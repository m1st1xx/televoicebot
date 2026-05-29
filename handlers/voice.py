from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from services.deepgram import DeepgramService
from utils.formatting import format_transcription
from config.config import config

from loguru import logger

import traceback

from utils.temp_storage import pending_transcriptions

router = Router()

deepgram_service = DeepgramService(
    config.DEEPGRAM_API_KEY
)

# Временное хранение распознанного текста


@router.message(F.voice)
async def handle_voice(message: Message):

    try:

        # Показываем статус "печатает..."
        await message.bot.send_chat_action(
            message.chat.id,
            "typing"
        )

        # Получаем файл
        file = await message.bot.get_file(
            message.voice.file_id
        )

        file_url = (
            f"https://api.telegram.org/file/bot"
            f"{config.BOT_TOKEN}/{file.file_path}"
        )

        logger.debug(
            f"Processing voice message. "
            f"File URL: {file_url}"
        )

        # Распознавание речи
        result = await deepgram_service.transcribe_audio(
            file_url
        )

        # Форматирование текста
        parts, _ = format_transcription(result)

        # Объединяем весь текст
        transcription_text = "\n".join(parts)

        # Сохраняем текст временно
        user_id = message.from_user.id

        pending_transcriptions[user_id] = transcription_text

        # Клавиатура подтверждения
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Да",
                        callback_data="confirm_yes"
                    ),

                    InlineKeyboardButton(
                        text="✏️ Редактировать",
                        callback_data="edit_text"
                    ),
                    InlineKeyboardButton(
                        text="❌ Отмена",
                        callback_data="confirm_no"
                    )
                ]
            ]
        )

        # Отправляем подтверждение
        await message.answer(
            (
                "Правильно ли я вас понял?\n\n"
                f"{transcription_text}"
            ),
            reply_markup=keyboard
        )

    except Exception as e:

        error_msg = f"Ошибка: {str(e)}"

        logger.error(
            f"Error processing voice message: "
            f"{str(e)}\n{traceback.format_exc()}"
        )

        await message.answer(error_msg)
