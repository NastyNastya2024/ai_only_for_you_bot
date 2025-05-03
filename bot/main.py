import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from handlers import set_handlers
import os
import asyncio

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

app = FastAPI()

# Устанавливаем хендлеры
set_handlers(dp)

@app.post("/webhook")
async def handle_webhook(request: Request):
    """
    Обрабатывает запросы через вебхук, поступающие от Telegram.
    """
    json_data = await request.json()
    update = types.Update(**json_data)

    # Для того, чтобы все было асинхронно, используем asyncio.create_task,
    # чтобы обработка обновлений Telegram не блокировала остальной код
    asyncio.create_task(dp.process_update(update))
    
    return JSONResponse(status_code=200, content={"message": "OK"})
