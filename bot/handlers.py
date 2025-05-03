from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import log_user_activity
from models.inference_gpu import generate_video, generate_image  # Импортируем функции генерации видео и изображений
from worker import send_task_to_worker  # Импорт отправки задачи в очередь RabbitMQ

async def start(message: types.Message):
    """
    Обработка команды /start
    """
    await message.answer(
        "Привет! Я могу генерировать видео из изображений или работать с различными моделями генерации изображений. "
        "Выбери одну из опций ниже:",
        reply_markup=main_keyboard()
    )

async def help_command(message: types.Message):
    """
    Обработка команды /help
    """
    await message.answer(
        "Ты можешь выбрать одну из моделей для генерации изображений или отправить изображение для создания видео. "
        "Просто нажми кнопку или отправь изображение!"
    )

async def button_handler(callback: types.CallbackQuery):
    """
    Обработка нажатий кнопок на панели
    """
    model_name = callback.data

    # Логирование действия пользователя
    log_user_activity(callback.from_user.id, model_name)

    # В зависимости от выбора модели выполняем соответствующую задачу
    if model_name.startswith("model_"):
        # Отправка задания на обработку изображения
        await send_task_to_worker(model_name, callback.from_user.id)
        await callback.answer(f"Запрос на {model_name} отправлен!")
    elif model_name == "generate_video":
        # Генерация видео из изображения
        await callback.answer("Пожалуйста, отправь изображение для создания видео.")
        await callback.bot.register_message_handler(generate_video_from_image, content_types=["photo"])

async def generate_video_from_image(message: types.Message):
    """
    Обработка отправленного изображения и генерация видео
    """
    try:
        # Получаем изображение от пользователя
        image = await message.photo[-1].download()

        # Генерируем видео
        video_path = generate_video(image)
        await message.answer_video(video_path, caption="Вот ваше видео!")
    except Exception as e:
        await message.answer(f"Произошла ошибка при генерации видео: {str(e)}")

def main_keyboard():
    """
    Клавиатура с кнопками для выбора модели
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Генерация изображений", callback_data="generate_image"),
        InlineKeyboardButton("Генерация видео", callback_data="generate_video"),
        InlineKeyboardButton("Модель 1", callback_data="model_1"),
        InlineKeyboardButton("Модель 2", callback_data="model_2"),
        InlineKeyboardButton("Модель 3", callback_data="model_3"),
        InlineKeyboardButton("Модель 4", callback_data="model_4"),
    )
    return keyboard

def set_handlers(dp):
    """
    Регистрация хендлеров
    """
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(help_command, commands=["help"])
    dp.register_callback_query_handler(button_handler, lambda c: c.data.startswith("model_"))
    dp.register_callback_query_handler(button_handler, lambda c: c.data == "generate_video")
