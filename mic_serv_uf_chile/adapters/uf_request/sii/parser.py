import os
import textfsm
from typing import List
from mic_serv_uf_chile.core.model import UF

UF_SSI_BY_YEAR_TEMPLATE = 'uf_ssi_by_year.textfsm'

def parser_sii_html_response(html_response: str):
    path = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    results = None
    with open(os.path.join('templates', UF_SSI_BY_YEAR_TEMPLATE)) as template:
        fsm = textfsm.TextFSM(template)
        results = fsm.ParseText(html_response)

    os.chdir(os.path.dirname(path))
    return results
    

def format_uf_values(uf_values: List, year: str) -> List:
    uf_formatted_values = list()
    last_day = '1'
    month = 1

    for item in uf_values:
        if month == 13:
            month = 1
        if item[0]:
            last_day = item[0]
        
        val = 'None' if item[1] == '&nbsp;' else item[1]
        mo = f'0{month}' if len(str(month)) == 1 else month
        da = f'0{last_day}' if len(last_day) == 1 else last_day

        uf_formatted_values.append(UF(value=val, date=f'{year}-{mo}-{da}'))

        month += 1
    
    return uf_formatted_values