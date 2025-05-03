import logging
import torch
from diffusers import StableVideoDiffusionPipeline
from PIL import Image
from diffusers.utils import export_to_video

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()  # также выводим в консоль
    ]
)

# Проверка доступности GPU и установка типа данных
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32
logging.info(f"Using device: {device}")

# Загружаем модель, учитывая доступное устройство
pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=dtype
).to(device)

# Включаем CPU offload для уменьшения использования памяти GPU
pipe.enable_model_cpu_offload()

def generate_video(image: Image) -> str:
    """
    Функция для генерации видео из изображения.
    
    :param image: Входное изображение.
    :return: Путь к сгенерированному видео.
    """
    try:
        # Проверка формата изображения
        if image.format not in ["JPEG", "PNG", "BMP", "WEBP", None]:
            raise ValueError(f"Неподдерживаемый формат изображения: {image.format}")
        
        image = image.resize((576, 1024)).convert("RGB")
        result = pipe(image, decode_chunk_size=8, num_frames=25)
        video_path = export_to_video(result.frames[0])
        logging.info("Видео успешно сгенерировано.")
        return video_path
    except Exception as e:
        logging.exception("Ошибка при генерации видео:")
        raise e
