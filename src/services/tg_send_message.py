import logging
import asyncio
from aiogram import Bot


bot_instance: Bot = None
main_loop: asyncio.AbstractEventLoop = None

def setup_sender(bot: Bot, loop: asyncio.AbstractEventLoop):

    logging.info('Инициализирую модуль отправки')

    global bot_instance, main_loop
    bot_instance = bot
    main_loop = loop

    logging.info('Модуль отправки инициализирован')


async def send_notification(telegram_id: int, job: dict):
    
    if not bot_instance:
        logging.info('Не инициализирован модуль отправки')
        return
    
    message_text = (
        f"🔥 **Новая вакансия c {job['source']}!**\n\n"
        f"**Название:** {job['title']}\n"
        f"**Описание:** _{job.get('description', '')[:200]}..._\n"
        f"**Цена:** {job['price']}\n"
        f"**Дополнительно:** {job['additionally']}"
    )

    await bot_instance.send_message(
        chat_id=telegram_id,
        text=message_text,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )

    logging.info('Увдеомление отправлено')