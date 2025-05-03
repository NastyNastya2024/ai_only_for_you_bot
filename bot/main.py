# main.py

import logging
import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from aiogram import Bot, Dispatcher, types
from aiogram import F
from handlers import set_handlers  # Подключаем обработчики

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем экземпляр FastAPI
app = FastAPI()

# Токен вашего бота
API_TOKEN = os.getenv('BOT_API_TOKEN')

# Создаем экземпляры бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Настроим обработчики
set_handlers(dp)  # Подключаем обработчики команд и событий бота

@app.post("/webhook/")
async def webhook(request: Request):
    """Обрабатываем вебхуки, отправляемые на /webhook."""
    payload = await request.json()
    
    # Обработаем входящие обновления
    update = types.Update(**payload)
    await dp.process_update(update)
    
    return JSONResponse(content={"status": "ok"})

# Новый способ запуска бота через polling или webhook
async def on_start():
    # Запускаем polling
    await dp.start_polling()

# Если нужно использовать webhook, нужно будет настроить FastAPI на прием вебхуков
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_start())


