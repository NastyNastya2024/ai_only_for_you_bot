import logging
from models.StableVideoDiffusion import generate_video as generate_video_stable_diffusion
from models.I2VGenXL import generate_video as generate_video_i2vgen_xl
from models.VideoCrafter1 import generate_video as generate_video_videocrafter1
from models.CogVideoX import generate_video as generate_video_cogvideox
from models.AnimateDiff import generate_video as generate_video_animatediff
from models.impactframes import generate_video as generate_video_impactframes

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("user_activity.log")
    ]
)

def log_user_activity(user_id: int, model_name: str):
    """
    Логирование активности пользователя
    """
    logging.info(f"Пользователь {user_id} запросил модель {model_name}.")

# Генерация видео с использованием различных моделей
async def generate_video(image, model_name):
    """
    Генерация видео по выбранной модели.
    
    :param image: Изображение, которое будет использовано для генерации видео.
    :param model_name: Название модели, которая будет использована для генерации видео.
    
    :return: Путь к сгенерированному видео.
    """
    # В зависимости от выбранной модели, вызов соответствующей функции генерации видео
    if model_name == "StableVideoDiffusion":
        return await generate_video_stable_diffusion(image)
    elif model_name == "I2VGenXL":
        return await generate_video_i2vgen_xl(image)
    elif model_name == "VideoCrafter1":
        return await generate_video_videocrafter1(image)
    elif model_name == "CogVideoX":
        return await generate_video_cogvideox(image)
    elif model_name == "AnimateDiff":
        return await generate_video_animatediff(image)
    elif model_name == "impactframes":
        return await generate_video_impactframes(image)
    else:
        # Если модель не поддерживается, генерируем ошибку
        raise ValueError("Модель не поддерживается.")
