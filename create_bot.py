from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os


# Создаем экземпляр бота 
bot = Bot(token=os.getenv("TOKEN"), parse_mode='HTML')

# Создаем экземпляр Dispatcher
dp = Dispatcher(bot, storage=MemoryStorage())