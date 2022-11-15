import asyncio
from contextlib import closing
import sqlite3
from aiogram import Bot
import random
import os

from config import *

bot = Bot(token=TOKEN)
database = "database.db"


async def main():
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, file_id, file_type FROM content WHERE chat = ? ORDER BY id LIMIT 1",
                       (chats[cat_chat_id],))
        cat = cursor.fetchone()
        if cat is None:
            reserv_photo = open(os.path.join("reserv/catdelo", random.choice(os.listdir("reserv/catdelo"))), "rb")
            name_photo = reserv_photo.name
            await bot.send_photo(cat_channel_id, photo=reserv_photo)
            reserv_photo.close()
            os.remove(name_photo)
        else:
            cursor.execute("DELETE FROM content WHERE id = ?", (int(cat[0]),))
            connection.commit()
            if cat[2] == "photo":
                await bot.send_photo(cat_channel_id, photo=cat[1])
            else:
                await bot.send_animation(cat_channel_id, animation=cat[1])
    session = await bot.get_session()
    await session.close()

if __name__ == "__main__":
    asyncio.run(main())
