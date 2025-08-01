import os
import httpx
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv
from pathlib import Path

current_file_path = Path(__file__).resolve()
print(f"Путь к текущему файлу: {current_file_path}")

project_root = current_file_path.parent.parent.parent

env_path = project_root / ".env"

if env_path.is_file():
    load_dotenv(dotenv_path=env_path, verbose=True)
else:
    print(f"!!! ОШИБКА: .env файл НЕ НАЙДЕН по пути {env_path} !!!")

BOT_TOKEN = os.getenv('BOT_TOKEN')

API_BASE_URL = os.getenv('API_BASE_URL')

if not BOT_TOKEN or not API_BASE_URL:
    print('Не нашел важные переменные')

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавить ключевое слово'),
            KeyboardButton(text='Мои ключевые слова')
        ],
        [
            KeyboardButton(text='Удалить ключевое слово')
        ],
        [
            KeyboardButton(text='Зарегестрироваться на отправку уведомлений')
        ]
    ]
)


class RegisterState(StatesGroup):
    waiting_for_username = State()

class KeywordStates(StatesGroup):
    waiting_for_keyword = State()
    waiting_for_keyword_to_delete = State()
    


router = Router()

@router.message(CommandStart())
async def command_start_handler(message: types.Message):

    await message.answer('Привет! Я бот, который отправляет уведомление, когда появляется новая вакансия на биржах', reply_markup=main_kb)



@router.message(F.text == 'Зарегестрироваться на отправку уведомлений')
async def register_start(message: types.Message, state: FSMContext):

    await message.answer('Давайте начнем регистрацию! Введите свое имя: ')

    await state.set_state(RegisterState.waiting_for_username)


@router.message(RegisterState.waiting_for_username)
async def username_handler(message: types.Message, state: FSMContext):

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f'{API_BASE_URL}/users/register', json={'telegram_id': message.from_user.id, 'name': message.text})

            response.raise_for_status()

            await message.answer(f'{message.text}, вы успешно зарегестрированы на отправку уведомлений!')

            await state.clear()
        except httpx.RequestError:
            await message.answer('Ошибка при подключении к серверу')
            await state.clear()
        except httpx.HTTPError:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            await message.answer(error_detail)
            await state.clear()



@router.message(F.text == 'Добавить ключевое слово')
async def keyword_start(message: types.Message, state: FSMContext):

    await message.answer("Напишите новое ключевое слово. Пишите в одном сообщении одно ключевое слово. Например 'Python', 'Fast API', 'API' и так далее")

    await state.set_state(KeywordStates.waiting_for_keyword)



@router.message(KeywordStates.waiting_for_keyword)
async def keyword_handler(message: types.Message, state: FSMContext):

    json_data = {
        'telegram_id': message.from_user.id,
        'text': message.text
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f'{API_BASE_URL}/keywords', json=json_data)

            response.raise_for_status()

            await message.answer('Добавлено ключевое слово')

            await state.clear()
        except httpx.RequestError:
            await message.answer('Ошибка при подключении к серверу')
            await state.clear()
        except httpx.HTTPError:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            await message.answer(error_detail)
            await state.clear()



@router.message(F.text == 'Мои ключевые слова')
async def get_keyword_handler(message: types.Message):

    await message.answer('Загружаю ваши ключевые слова...')

    params = {
        'telegram_id': message.from_user.id
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{API_BASE_URL}/keywords', params=params)

            response.raise_for_status()

            keywords = [keyword['text'] for keyword in response.json()]

            await message.answer(f"Ваши ключевые слова: '{', '.join(keywords)}'")

        except httpx.RequestError:
            await message.answer('Ошибка при подключении к серверу')
        except httpx.HTTPError:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            await message.answer(error_detail)



@router.message(F.text == 'Удалить ключевое слово')
async def delete_keyword_start(message: types.Message, state: FSMContext):

    params = {
        'telegram_id': message.from_user.id
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{API_BASE_URL}/keywords', params=params)

            response.raise_for_status()

            keywords = [keyword['text'] for keyword in response.json()]

            await message.answer(f"Ваши ключевые слова: '{', '.join(keywords)}'")

            await message.answer('Введите ключевое слово, которое вы хотите удалить: ')

            await state.set_state(KeywordStates.waiting_for_keyword_to_delete)

        except httpx.RequestError:
            await message.answer('Ошибка при подключении к серверу')
            state.clear()
        except httpx.HTTPError:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            await message.answer(error_detail)
            state.clear()



@router.message(KeywordStates.waiting_for_keyword_to_delete)
async def delete_keyword_handler(message: types.Message, state: FSMContext):

    params = {
        'telegram_id': message.from_user.id,
        'keyword_text': message.text
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f'{API_BASE_URL}/keywords', params=params)

            response.raise_for_status()

            await message.answer('Ключевое слово успешно удалено')
        
        except httpx.RequestError:
            await message.answer('Ошибка при подключении к серверу')
            await state.clear()
        except httpx.HTTPError:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            await message.answer(error_detail)
            await state.clear()