# handlers.py

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import log_user_activity, generate_video  # Импортируем утилиты
from worker import send_task_to_worker  # Функция для отправки задачи в очередь RabbitMQ

# Состояние для хранения изображения и выбранной модели
user_state = {}

async def start(message: types.Message):
    """
    Обработка команды /start
    """
    await message.answer(
        "Привет! Я могу генерировать видео из изображений. Загрузите изображение, "
        "и затем выберите модель для генерации видео по этому изображению. "
        "Нажмите одну из кнопок ниже, чтобы выбрать модель:",
        reply_markup=main_keyboard()
    )

async def help_command(message: types.Message):
    """
    Обработка команды /help
    """
    await message.answer(
        "Ты можешь отправить мне изображение, а затем выбрать одну из моделей для генерации видео. "
        "Просто загрузите картинку и выбери модель!"
    )

async def button_handler(callback: types.CallbackQuery):
    """
    Обработка нажатий кнопок на панели
    """
    model_name = callback.data

    # Логирование действия пользователя
    log_user_activity(callback.from_user.id, model_name)

    # Сохраняем выбранную модель для пользователя
    user_state[callback.from_user.id] = {'model': model_name}
    
    # Уведомление пользователя
    await callback.answer(f"Модель {model_name} выбрана. Теперь отправьте мне изображение.")

async def process_image(message: types.Message):
    """
    Обработка изображения, отправленного пользователем, и генерация видео
    """
    try:
        # Получаем изображение от пользователя
        image = await message.photo[-1].download()

        # Проверка, выбрал ли пользователь модель
        if message.from_user.id not in user_state or 'model' not in user_state[message.from_user.id]:
            await message.answer("Сначала выберите модель для генерации видео.")
            return

        model_name = user_state[message.from_user.id]['model']
        
        # Генерация видео по выбранной модели через утилиту
        video_path = await generate_video(image, model_name)

        # Отправляем сгенерированное видео пользователю
        await message.answer_video(video_path, caption=f"Вот ваше видео, сгенерированное с помощью {model_name}!")

    except Exception as e:
        await message.answer(f"Произошла ошибка при генерации видео: {str(e)}")

def main_keyboard():
    """
    Клавиатура с кнопками для выбора модели
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Stable Video Diffusion", callback_data="StableVideoDiffusion"),
        InlineKeyboardButton("I2VGen-XL", callback_data="I2VGenXL"),
        InlineKeyboardButton("Video Crafter 1", callback_data="VideoCrafter1"),
        InlineKeyboardButton("Cog Video X", callback_data="CogVideoX"),
        InlineKeyboardButton("Animate Diff", callback_data="AnimateDiff"),
        InlineKeyboardButton("Impact Frames", callback_data="impactframes"),
    )
    return keyboard

def set_handlers(dp):
    """
    Регистрация хендлеров
    """
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(help_command, commands=["help"])
    dp.register_callback_query_handler(button_handler, lambda c: c.data in [
        "StableVideoDiffusion", "I2VGenXL", "VideoCrafter1", "CogVideoX", "AnimateDiff", "impactframes"
    ])
    dp.register_message_handler(process_image, content_types=["photo"])
