# Author: Leonardo Gonzalez (gonzalezrujano@gmail.com) 
# -- PyMongo pagination module for aggregations --

import re
import json
from math import ceil
from bson import json_util


class Pagination:
    def __init__(self, page=None, per_page=None, instance_db=None):
        self.page = page
        self.per_page = per_page

        self.instance_db = instance_db

        self.total_rows = 0
        self.next_page = None
        self.previus_page = None
        self.total_pages = 0

        if not isinstance(page, int) or page <= 0:
            raise Exception('Error: page param must be one integer > 0')

        if not isinstance(per_page, int) or per_page <= 0:
            raise Exception('Error: per_page param must be one integer > 0')


class PyMongoPagination(Pagination):
    def __init__(self, page=None, per_page=None, instance_db=None):
        super().__init__(page=page, per_page=per_page, instance_db=instance_db)

        self.old_pipeline = []
        self.original_pipeline = []
        self.pipeline = []
        self.counter_pipeline = None

        self.pipeline_results = None

        self.__is_instance_pymongo()

        self.valid_stages = [
            '$addFields',
            '$bucket',
            '$bucketAuto',
            '$collStats',
            '$count',
            '$facet',
            '$geoNear',
            '$graphLookup',
            '$group',
            '$indexStats',
            '$limit',
            '$listSessions',
            '$lookup',
            '$match',
            '$merge',
            '$out',
            '$planCacheStats',
            '$project',
            '$redact',
            '$replaceRoot',
            '$replaceWith',
            '$sample',
            '$search',
            '$set',
            '$setWindowFields',
            '$skip',
            '$sort',
            '$sortByCount',
            '$unionWith',
            '$unset',
            '$unwind',
            '<add_pagination>'
        ]

        self.is_custom_pipeline = False

        self.filters = None
        self.formatted_filters = None

        self.without_pagination = False

    def __is_instance_pymongo(self):
        try:
            if 'MongoClient' not in str(self.instance_db.database):
                raise Exception('Error: instance_db param must be collection class of PyMongo')
        except Exception:
            raise Exception('Error: instance_db param must be collection class of PyMongo')

    def __is_valid_pipeline(self):
        if not isinstance(self.pipeline, list) or self.pipeline is None:
            return False

        for stage in self.pipeline:
            if not isinstance(stage, dict):
                return False

            number_keys = len(list(stage.keys()))
            if number_keys > 1 or number_keys < 1:
                return False

            stage_name = list(stage.keys())[0]
            if stage_name not in self.valid_stages:
                return False

        return True

    def __is_valid_filters(self):
        fields = self.filters['fields']
        value = self.filters['value']

        if not isinstance(fields, list) or (not isinstance(value, str) and not isinstance(value, list)):
            return False

        for field in self.filters['fields']:
            if not isinstance(field, str):
                return False

        return True

    def __add_stage_pipeline(self, stage):
        pipeline = self.pipeline
        pipeline.append(stage)

        self.pipeline = pipeline

    def __exec_pipeline(self):
        try:
            result = self.instance_db.aggregate(self.pipeline, cursor={})
            self.pipeline_results = json.loads(json_util.dumps(result))
        except Exception:
            raise Exception("Error: An error occurred while trying to communicate with Pymongo")

    def __restore_pipeline(self):
        self.pipeline = self.original_pipeline

    def __clear_pipeline_results(self):
        self.pipeline_results = None

    def __calculate_total_pages(self):
        self.total_pages = ceil(self.total_rows / self.per_page)

    def __calculate_total_rows(self):
        if self.counter_pipeline is not None:
            self.pipeline = self.counter_pipeline

        self.__add_stage_pipeline({'$count': 'total_rows'})

        self.__exec_pipeline()

        self.total_rows = 0 if len(self.pipeline_results) == 0 else self.pipeline_results[0]['total_rows']
        self.__calculate_total_pages()

        self.__clear_pipeline_results()
        self.__restore_pipeline()

    def __set_special_format(self, special_filters=None):
        value = self.filters['value']

        if not isinstance(special_filters, list):
            raise Exception('Error: Filters must be one valid format')

        if len(special_filters) > 0:
            now_filter = special_filters[0]
            special_filters.pop(0)

            if now_filter == '$':
                now_filter = '$elemMatch'

            return {
                now_filter: self.__set_special_format(special_filters=special_filters)
            }

        return value if isinstance(value, list) else re.compile(value)

    def __format_filters_for_mongo(self):
        format_filters = []

        for filter in self.filters['fields']:
            formatted_filter = {}

            if '.$.' in filter or '.$in' in filter:
                formatted_filter = self.__set_special_format(filter.split('.'))
            else:
                formatted_filter[filter] = re.compile(self.filters['value'])

            format_filters.append(formatted_filter)

        self.formatted_filters = {
            '$match': {
                '$or': format_filters
            }
        }

    def __add_paginate_stages(self):
        skip_stage = self.get_skip_stage()
        limit_stage = self.get_limit_stage()

        if not self.without_pagination:
            if self.page > 1:
                self.__add_stage_pipeline(skip_stage)
            self.__add_stage_pipeline(limit_stage)

    def get_skip_stage(self):
        return {'$skip': self.get_skip_value()}

    def get_limit_stage(self):
        return {'$limit': self.per_page}

    def set_pipeline(self, new_pipeline, without_pagination=False):
        self.pipeline = new_pipeline
        if not self.__is_valid_pipeline():
            self.pipeline = []
            raise Exception('Error: Pipeline must be one valid format')
        self.original_pipeline = new_pipeline
        self.without_pagination = without_pagination

    def set_counter_pipeline(self, counter_pipeline):
        self.counter_pipeline = counter_pipeline

    def add_filters(self, fields, value):
        self.filters = {
            'fields': fields,
            'value': value
        }
        if not self.__is_valid_filters():
            self.filters = None
            self.formatted_filters = None
            raise Exception('Error: Filters must be one valid format')

        self.__format_filters_for_mongo()
        self.__add_stage_pipeline(self.formatted_filters)

    def clear_filters(self):
        self.filters = None
        self.formatted_filters = None

    def get_results(self):
        self.__calculate_total_rows()
        self.__add_paginate_stages()

        self.__exec_pipeline()

        return {
            'data': self.pipeline_results,
            'items': self.per_page,
            'total_pages': self.total_pages,
            'next_page': self.page + 1 if self.page < self.total_pages else '',
            'actual_page': self.page,
            'previous_page': self.page - 1 if self.page > 1 else ''
        }

    def get_skip_value(self):
        return (self.page - 1) * self.per_page

