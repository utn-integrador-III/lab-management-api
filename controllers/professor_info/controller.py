import logging
from models.professor_info.model import ProfessorInfoModel
from utils.server_response import ServerResponse, StatusCode
from flask_restful import Resource
from utils.server_response import *
from utils.message_codes import *
from utils.auth_manager import auth_required

class ProfessorInfoController(Resource):

    route = "/professor"

    @auth_required(permission='update', with_args=True)
    def get(self, **kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            # Proceed with access to current_user data
            print(f"Current user: {current_user}")
        else:
            # Handle cases where current_user is not provided
            print("No user data available")
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
                    message="Professors not found",
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
