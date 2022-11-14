import json

import requests
from contextlib import closing
import sqlite3

from config import *

database = "database.db"
url = f"https://api.telegram.org/bot{TOKEN}"
with closing(sqlite3.connect(database)) as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT id, file_id, file_type FROM content WHERE chat = ? ORDER BY id LIMIT 1",
                   (chats[memes_chat_id],))
    mem = cursor.fetchone()
    if mem is None:
        pass
    else:
        cursor.execute("DELETE FROM content WHERE id = ?", (int(mem[0]),))
    connection.commit()
    if mem[2] == "photo":
        requests.post(url + "/sendPhoto", json={"chat_id": memes_channel_id, "photo": mem[1]})
    else:
        requests.post(url + "/sendAnimation", json={"chat_id": memes_channel_id, "animation": mem[1]})

    cursor.execute("SELECT id, file_id, file_type FROM content WHERE chat = ? ORDER BY id LIMIT 1",
                   (chats[cat_chat_id],))
    cat = cursor.fetchone()
    if cat is None:
        pass
    else:
        cursor.execute("DELETE FROM content WHERE id = ?", (int(cat[0]),))
    connection.commit()
    if cat[2] == "photo":
        requests.post(url + "/sendPhoto", json={"chat_id": cat_channel_id, "photo": cat[1]})
    else:
        requests.post(url + "/sendAnimation", json={"chat_id": cat_channel_id, "animation": cat[1]})
