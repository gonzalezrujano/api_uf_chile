from flask import current_app
from flask_restx import Resource, inputs
from mic_serv_uf_chile.adapters.web.dto.uf import UFService
import datetime

api = UFService.api

@api.route('/sii/<string:date>')
class UFSIIRequest(Resource):
    @api.marshal_with(UFService.UFResponse, skip_none=True)
    def get(self, date):
        try:
            date = inputs.date_from_iso8601(date)
        except ValueError:
            return {'error': f'{date} is an invalid date.'}
        if date < inputs.date_from_iso8601('2013-01-01'):
            return {'error': f'{date} is lower than the last record of 2013-01-01.'}
        if date > datetime.date.today():
            return {'error': f'{date} is greater than the current date {datetime.date.today()}.'}
        
        return current_app.ms_actions.get_by_day(str(date))
