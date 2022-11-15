from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from aiogram.utils import executor
from aiogram import Bot

from contextlib import closing
import sqlite3

from config import *

stor = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=stor)

database = "database.db"


def create_table():
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS content(id INTEGER PRIMARY KEY, file_id TEXT, file_type TEXT, chat TEXT)')
        connection.commit()


def add_content(file_id, file_type, chat):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO content(file_id, file_type, chat) VALUES (?, ?, ?)", (file_id, file_type, chat))
        connection.commit()


def get_content():
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT chat_id FROM users")
        return cursor.fetchall()


async def on_startup(_):
    create_table()


@dp.message_handler(content_types="photo")
async def photo_message(message: Message):
    try:
        add_content(message.photo[-1].file_id, "photo", chats[message.chat.id])
    except KeyError:
        pass


@dp.message_handler(content_types="animation")
async def gif_message(message: Message):
    try:
        add_content(message.photo[-1].file_id, "gif", chats[message.chat.id])
    except KeyError:
        pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
