import os
import asyncio
import httpx
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from ..services.tg_send_message import setup_sender
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

API_BASE_URL = os.getenv('API_BASE_URL')

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавить ключевыe слова'),
            KeyboardButton(text='Мои ключевые слова')
        ],
        [
            KeyboardButton(text='Изменить ключевые слова'),
            KeyboardButton(text='Удалить ключевые слова')
        ],
        [
            KeyboardButton(text='Зарегестрироваться на отправку уведомлений')
        ]
    ]
)


class RegisterState(StatesGroup):
    waiting_for_username = State()

class KeywordState(StatesGroup):
    waiting_for_keyword = State()

class NewKeywordState(StatesGroup):
    waiting_for_keyword = State()


router = Router()

@router.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext):

    await message.answer('Привет! Я бот, который отправляет уведомление, когда появляется новая вакансия на биржах', reply_markup=main_kb)

    await message.answer('Введите пожалуйста свое имя: ')

    await state.set_state(RegisterState.waiting_for_username)

    


@router.message(RegisterState.waiting_for_username)
async def username_handler(message: types.Message):

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f'{API_BASE_URL}/users/register', json={'telegram_id': message.from_user.id, 'name': message.text})

            response.raise_for_status()

            await message.answer(f'{message.text}, вы успешно зарегестрированы на отправку уведомлений!')
        except httpx.RequestError:
            await message.answer('Ошибка при подключении к серверу')
        except httpx.HTTPError as e:
            await message.answer(f'Ошибка при запросе на сервер: {e}')



@router.message(F.text == 'Добавить ключевыe слова')
async def nkeyword_start(message: types.Message, state: FSMContext):

    await message.answer('Напишите новые ключевые слова. Пишите одним сообщением: ')

    await state.set_state(KeywordState.waiting_for_keyword)



@router.message(KeywordState.waiting_for_keyword)
async def keywors_handler(message: types.Message, state: FSMContext):

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f'{API_BASE_URL}/keywords', json={'text': message.text})

            response.raise_for_status()

            await message.answer('Добавлены ключевые слова')

        except httpx.RequestError:
            await message.answer('Ошибка при подключении к серверу')
        except httpx.HTTPError as e:
            await message.answer(f'Ошибка при запросе на сервер: {e}')



@router.message(F.text == 'Мои ключевые слова')
async def get_keyword_handler(message: types.Message):

    await message.answer('Загружаю ваши ключевые слова...')

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{API_BASE_URL}/keywords/{message.from_user.id}')

            response.raise_for_status()

            keyword = response.json()

            await message.answer(f"Ваши ключевые слова: '{keyword['text']}'")

        except httpx.RequestError:
            await message.answer('Ошибка при подключении к серверу')
        except httpx.HTTPError as e:
            await message.answer(f'Ошибка: {e}')



@router.message(F.text == 'Изменить ключевые слова')
async def new_keyword_start(message: types.Message, state: FSMContext):

    await message.answer('Введите новые ключевые слова: ')

    await state.set_state(NewKeywordState.waiting_for_keyword)



@router.message(NewKeywordState.waiting_for_keyword)
async def new_keyword_handler(message: types.Message):

    new_keyword_json = {
        'text': message.text
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f'{API_BASE_URL}/keywords/{message.from_user.id}', json=new_keyword_json)

            response.raise_for_status()

            await message.answer('Ваши ключевые слова успешно изменены')

        except httpx.RequestError:
            await message.answer('Ошибка при кодключении к серверу')
        except httpx.HTTPError as e:
            await message.answer(f'Ошибка: {e}')



@router.message(F.text == 'Удалить ключевые слова')
async def delete_keyword_handler(message: types.Message):

    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f'{API_BASE_URL}/keywords/{message.from_user.id}')

            response.raise_for_status()

            await message.answer('Ваши ключевые слова успешно удалены')
        
        except httpx.RequestError:
            await message.answer('Ошикбка при подключении к серверу')
        except httpx.HTTPError as e:
            await message.answer(f'Ошибка: {e}')



async def main():
    bot = Bot(BOT_TOKEN)

    dp = Dispatcher()

    loop = asyncio.get_running_loop()

    setup_sender(bot, loop)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())