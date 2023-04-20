"""Micro service core actions."""

from mic_serv_uf_chile.adapters.uf_request import get_uf_by_day


class Actions:
    """Clase de acciones del Core.

    En esta clase se definen y se implementan todas las acciones que
    realizara el microservicio.
    """

    def __init__(self, config=None, db=None):
        """Object constructor."""
        self.config = config
        self.db = db

    @staticmethod
    def say_hello() -> str:
        """Return string."""
        return "Hello"
    
    def get_by_day(self, date: str) -> float:
        return get_uf_by_day(date)

    