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
                   (chats[cat_chat_id],))
    cat = cursor.fetchone()
    if cat is None:
        reserv_photo = open(os.path.join("reserv/catdelo", random.choice(os.listdir("reserv/catdelo"))), "rb")
        name_photo = reserv_photo.name
        files = {"photo": reserv_photo}
        requests.post(url + "/sendPhoto", data={"chat_id": cat_channel_id}, files=files)
        reserv_photo.close()
        os.remove(reserv_photo.name)
    else:
        cursor.execute("DELETE FROM content WHERE id = ?", (int(cat[0]),))
        connection.commit()
        if cat[2] == "photo":
            requests.post(url + "/sendPhoto", json={"chat_id": cat_channel_id, "photo": cat[1]})
        else:
            requests.post(url + "/sendAnimation", json={"chat_id": cat_channel_id, "animation": cat[1]})
