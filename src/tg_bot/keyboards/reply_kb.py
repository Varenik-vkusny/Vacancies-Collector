from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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