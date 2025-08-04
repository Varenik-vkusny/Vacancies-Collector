from aiogram.filters import CommandStart
from ..keyboards.reply_kb import main_kb
from aiogram import Router, types


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message):

    await message.answer('Привет! Я бот, который отправляет уведомление, когда появляется новая вакансия на биржах', reply_markup=main_kb)
