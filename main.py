from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils import executor
from aiogram import Bot

from config import *

stor = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=stor)


async def on_startup(_):
    pass


@dp.message_handler(commands='start')
async def start_message(message: Message):
    pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
