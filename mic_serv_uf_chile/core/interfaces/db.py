from abc import ABC, abstractmethod
from mic_serv_uf_chile.core.model import UF
from typing import List


class DBAdapter(ABC):
    """Clase adaptador de la base de datos.

    Esta clase debe reflejar todas las funcionalidades que va a
    proporcionar el adaptador de base de datos. Y la clase de
    implementación debe ser hija de esta.

    Cada funcionalidad que se escriba en el adaptador debe tener su
    contraparte en este archivo como un metodo abstracto.

    Por ejemplo si se necesita listar usuarios en esta clase debera
    existir un metodo abstracto que defina el nombre del metodo, sus
    parametros y el tipo de salida. Usuario debe ser una clase que
    represente los datos del usuario y que permita modelar los datos.

    @abstractmethod
    def listarUsuarios(query=None) -> List[Usuario]:
        pass
    """

    @abstractmethod
    def get_in_cache(self, date: str) -> UF:
        pass

    @abstractmethod
    def save_in_cache(self, uf_values: List[UF]) -> bool:
        pass
