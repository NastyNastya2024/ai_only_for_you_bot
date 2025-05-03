import logging
import torch
from PIL import Image
from animate_diff import AnimateDiffModel  # Пример с гипотетической библиотекой

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32
logging.info(f"Using device: {device}")

model = AnimateDiffModel.from_pretrained("animate_diff_model_path").to(device)

def generate_video(image: Image, prompt: str) -> str:
    try:
        if image.format not in ["JPEG", "PNG", "BMP", "WEBP"]:
            raise ValueError(f"Неподдерживаемый формат изображения: {image.format}")

        image = image.resize((576, 1024)).convert("RGB")
        result = model.generate(image, prompt)
        video_path = "generated_video.mp4"
        result.save(video_path)
        logging.info(f"Видео сгенерировано с помощью AnimateDiff по запросу: {prompt}.")
        return video_path

    except Exception as e:
        logging.exception("Ошибка при генерации видео с AnimateDiff:")
        raise e
