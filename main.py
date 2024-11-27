import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import F
from keyboards import user_keyboards, speaker_keyboards


load_dotenv()
bot = Bot(token=os.getenv("TG_TOKEN"))
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Выберите действие:", reply_markup=speaker_keyboards)


@dp.message(F.text == "/help")
async def cmd_help(message: Message):
    await message.answer("справка")


@dp.message(F.text == "Задать вопрос")
async def ask_question(message: Message):
    await message.answer("Пожалуйста, введите ваш вопрос:")


@dp.message(F.text == "Программа мероприятия")
async def program(message: Message):
    await message.answer("Программа на сегодня:")


@dp.message(F.text == "Список вопросов")
async def question_list(message: Message):
    await message.answer("Ваш список вопросов")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
