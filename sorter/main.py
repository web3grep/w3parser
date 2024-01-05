import logging
import json
import asyncio
from telethon import TelegramClient, events

# Настройки бота и ID каналов загружаются из файла settings.py
from settings import API_ID, API_HASH, BOT_TOKEN, MONITORED_CHANNEL_ID

# Настройка логгирования для отслеживания действий бота
logging.basicConfig(format='[%(levelname)s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем клиента Telegram
bot = TelegramClient('bot', API_ID, API_HASH)

# Функция для проверки наличия слов из черного списка в тексте
def contains_blacklisted_keywords(text, blacklisted_keywords):
    return any(keyword.lower() in text.lower() for keyword in blacklisted_keywords)

# Функция для проверки наличия ключевых слов в тексте сообщения
def contains_keywords(text, keywords):
    return any(keyword.lower() in text.lower() for keyword in keywords)

# Асинхронная функция для перезагрузки ключевых слов и черного списка из файлов
async def reload_keywords_and_blacklist():
    global KEYWORDS, BLACKLISTED_KEYWORDS
    while True:
        try:
            with open('keywords.json', 'r', encoding='utf-8') as f:
                KEYWORDS = json.load(f)
            with open('blacklisted_keywords.json', 'r', encoding='utf-8') as f:
                BLACKLISTED_KEYWORDS = json.load(f)
            logger.info("KEYWORDS UPDATED")
        except Exception as e:
            logger.error(f"Ошибка при загрузке словарей: {e}")
        await asyncio.sleep(60)  # Перезагрузка каждый минуту

# Функция для загрузки данных из JSON-файла
async def reload_source_channels():
    global SOURCE_CHANNELS
    while True:
        try:
            with open('source_channels.json', 'r', encoding='utf-8') as f:
                SOURCE_CHANNELS = json.load(f)
            logger.info("SOURCE CHANNELS UPDATED")
        except Exception as e:
            logger.error(f"Ошибка при загрузке каналов-источников: {e}")
        await asyncio.sleep(60)  # Перезагрузка каждый минуту

# Обработчик новых сообщений в канале
@bot.on(events.NewMessage(chats=MONITORED_CHANNEL_ID))
async def handler(event):
    # Проверяем, является ли сообщение пересланным
    if event.message.forward:
        original_channel_id = event.message.forward.chat_id
        logger.info(f"Сообщение переслано из канала {original_channel_id}")
    else:
        logger.info("Сообщение не является пересланным.")
        return

    # Получаем текст сообщения или подпись к медиа
    message_text = event.message.text
    if event.message.media and hasattr(event.message, 'caption'):
        message_text = event.message.caption

    if not message_text:
        logger.info("Сообщение без текста получено и проигнорировано.")
        return

    # Проверка на соответствие каналу-источнику и пересылка в нужный канал
    for target_channel, source_channels in SOURCE_CHANNELS.items():
        if str(original_channel_id) in source_channels:
            try:
                await bot.forward_messages(int(target_channel), event.message)
                logger.info(f"Сообщение переслано в канал {target_channel} из исходного канала {original_channel_id}")
                return
            except Exception as e:
                logger.error(f"Ошибка при пересылке сообщения: {e}")
                return

    # Логика обработки на основе ключевых слов
    matched_channels = []
    for channel_id, data in KEYWORDS.items():
        if channel_id == "multiple_keywords_channel":
            continue  # Пропускаем специальный канал для множественных ключевых слов

        keywords = data.get('keywords', [])
        exceptions = data.get('exceptions', [])

        if any(word.lower() in message_text.lower() for word in exceptions):
            logger.info(f"Сообщение содержит исключения для канала {channel_id} и не будет переслано.")
            continue

        if contains_keywords(message_text, keywords):
            matched_channels.append(channel_id)

    if len(matched_channels) > 2:
        # Если обнаружено более двух ключевых слов, пересылаем в специальный канал
        multiple_keywords_channel_id = KEYWORDS["multiple_keywords_channel"]["channel_id"]
        try:
            await bot.forward_messages(int(multiple_keywords_channel_id), event.message)
            logger.info(f"Сообщение с множественными ключевыми словами переслано в канал {multiple_keywords_channel_id}")
        except Exception as e:
            logger.error(f"Ошибка при пересылке сообщения: {e}")
    else:
        # Иначе пересылаем в соответствующие каналы
        for channel_id in matched_channels:
            try:
                await bot.forward_messages(int(channel_id), event.message)
                logger.info(f"Сообщение переслано в канал {channel_id}")
            except Exception as e:
                logger.error(f"Ошибка при пересылке сообщения: {e}")



# Запускаем бота и функцию перезагрузки словарей
bot.start(bot_token=BOT_TOKEN)
logger.info("Бот запущен...")
loop = asyncio.get_event_loop()
loop.create_task(reload_source_channels())
loop.create_task(reload_keywords_and_blacklist())
bot.run_until_disconnected()
