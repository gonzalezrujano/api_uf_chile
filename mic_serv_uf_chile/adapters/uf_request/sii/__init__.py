from mic_serv_uf_chile.core.model import UF
from mic_serv_uf_chile.adapters.uf_request.sii.request import get_uf_values
from flask import current_app


def request_uf(date: str):
    # Check is in cache
    result_in_cache = current_app.ms_actions.db.get_in_cache(date)
    if result_in_cache:
        result_in_cache = UF(date=date, value=result_in_cache)
        result_in_cache.value = result_in_cache.value.decode("utf-8")
        return result_in_cache.__dict__

    # Get UF values from SSI web
    results = get_uf_values(date[:4])

    # Return requested value
    result = [val for val in results if val.date == date][0]

    return result.__dict__


if __name__ == "__main__":
    print(request_uf("2021-02-30"))