import logging
from models.professor_info.model import ProfessorInfoModel
from utils.server_response import ServerResponse, StatusCode
from flask_restful import Resource
from utils.server_response import *
from utils.message_codes import *


class ProfessorInfoController(Resource):

    route = "/professor"

    def get(self):
        try:
            professors = ProfessorInfoModel.get_all()
            if isinstance(professors, dict) and "error" in professors:
                return ServerResponse(
                    data={},
                    message=professors["error"],
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )

            if not professors:
                return ServerResponse(
                    data=None,
                    message="No professors found",
                    message_code=NO_DATA,
                    status=StatusCode.BAD_REQUEST,
                )

            professors = [
                ProfessorInfoModel.convert_object_ids(prof) for prof in professors
            ]
            return ServerResponse(data=professors, status=StatusCode.OK)

        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
