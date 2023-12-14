from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message) -> None:
    await msg.answer("Я могу помочь тебе узнать твой ID, просто отправь мне любое сообщение")


@router.message()
async def message_handler(msg: Message) -> None:
    if msg.from_user is None:
        await msg.answer("Can't identify your ID")
    else:
        await msg.answer(f"Your ID: {msg.from_user.id}")
