import requests
from typing import List
from mic_serv_uf_chile.adapters.uf_request.sii.parser import parser_sii_html_response, format_uf_values
from mic_serv_uf_chile.core.model import UF
from flask import current_app


def request_to_sii_html(year: str) -> str:
    r = requests.get(f'https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm')
    return r.text

def get_uf_values(year: str) -> List[UF]:
    html_response = request_to_sii_html(year)
    ufs_without_format = parser_sii_html_response(html_response)

    uf_values = format_uf_values(ufs_without_format, year)
    current_app.ms_actions.db.save_in_cache(uf_values)

    return uf_values