import httpx
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from src.backend.config import get_settings

settings = get_settings()

API_BASE_URL = settings.api_base_url


class RegisterState(StatesGroup):
    waiting_for_username = State()


router = Router()


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