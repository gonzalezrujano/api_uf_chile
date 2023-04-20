from mic_serv_uf_chile.core.exceptions import NoConfigFile
from mic_serv_uf_chile.core.interfaces.db import DBAdapter
import redis
from mic_serv_uf_chile.core.model import UF
from typing import List


class DB(DBAdapter):
    def __init__(self, config=None):
        self.db = redis.Redis(host=config['host'], port=config['port'], db=config['db'])

    def get_in_cache(self, date: str) -> UF:
        return self.db.get(date)


    def save_in_cache(self, uf_values: List[UF]) -> bool:

        for item in uf_values:
            self.db.set(item.date, item.value)

        return True

