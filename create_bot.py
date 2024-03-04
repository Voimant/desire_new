from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(storage=MemoryStorage())
# объeкт бота

