from mic_serv_uf_chile.core.model import UF
from mic_serv_uf_chile.adapters.uf_request.sii import request_uf

def get_uf_by_day(date: str) -> UF:
    """Request UF by day.

    Args:
      date str: Date target (Example: '2021-01-01')

    Returns:
      Union[float, None]: UF of day or None
    """

    return request_uf(date)


if __name__ == "__main__":
    print(get_uf_by_day("2020-01-02"))