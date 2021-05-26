from flask import request
from flask_restx import Resource

from app.main import db
from sqlalchemy import desc, asc

from ..util.dto import RecommendedListDataDto
from ..service.recommened_list_data_service import save_recommended_list_data, \
    get_all_recommended_list_data

api = RecommendedListDataDto.api
_recommended_list_data = RecommendedListDataDto.recommended_list_data


@api.route('/')
class RecommendedListsData(Resource):
    def post(self):
        data = request.json
        return save_recommended_list_data(data)


@api.route('/all')
class AllRecommendedListData(Resource):
    def get(self):
        return get_all_recommended_list_data()
