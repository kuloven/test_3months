from aiogram import Router
from aiogram.types import Message

echo_router = Router()

@echo_router.message()
async def echo_message(message: Message):
    reversed_message = ' '.join(message.text.split()[::-1])
    await message.answer(reversed_message)

