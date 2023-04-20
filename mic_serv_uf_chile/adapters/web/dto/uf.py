from flask_restx import Namespace, fields

class UFService:
    api = Namespace(
        'UF Chile service',
        description='Consulta de UF en SII',
        path='uf'
    )

    UFResponse = api.model('UF', {
        'value': fields.String(description='UF value', example='28.410,87'),
        'date': fields.String(description='Requested date', example='2020-02-20'),
        'error': fields.String(description='Error message', example='2020-02-20 is greater than the current date')
    })
