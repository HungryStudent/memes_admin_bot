from contextlib import closing
import sqlite3

import requests
import random
import os

from config import *

database = "database.db"
url = f"https://api.telegram.org/bot{TOKEN}"
with closing(sqlite3.connect(database)) as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT id, file_id, file_type FROM content WHERE chat = ? ORDER BY id LIMIT 1",
                   (chats[memes_chat_id],))
    mem = cursor.fetchone()
    if mem is None:
        reserv_photo = open(os.path.join("reserv/memdelo", random.choice(os.listdir("reserv/memdelo"))), "rb")
        name_photo = reserv_photo.name
        files = {"photo": reserv_photo}
        res = requests.post(url + "/sendPhoto", data={"chat_id": memes_channel_id}, files=files)
        reserv_photo.close()
        os.remove(name_photo)
    else:
        cursor.execute("DELETE FROM content WHERE id = ?", (int(mem[0]),))
        connection.commit()
        if mem[2] == "photo":
            requests.post(url + "/sendPhoto", json={"chat_id": memes_channel_id, "photo": mem[1]})
        else:
            requests.post(url + "/sendAnimation", json={"chat_id": memes_channel_id, "animation": mem[1]})