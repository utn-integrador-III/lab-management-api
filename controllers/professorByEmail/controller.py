# controllers/professor_controller.py
from flask_restful import Resource
from flask import request
from utils.server_response import *
from utils.message_codes import *
import logging
from models.professor_info.model import ProfessorInfoModel
from flask import request

class ProfessorByEmailController(Resource):
    route = "/professor/byemail"

    def get(self):
        try:
            professor_email = request.args.get('professor_email')
            if not professor_email:
                logging.error("professor_email parameter is required")
                return ServerResponse(
                    message="Professor email required",
                    message_code=PROFESSOR_EMAIL_REQUIRED,
                    status=StatusCode.BAD_REQUEST
                )

            professor = ProfessorInfoModel.get_by_email(professor_email)
            if not professor:
                logging.error(f"Professor not found for email: {professor_email}")
                return ServerResponse(
                    message="Professor not found",
                    message_code=PROFESSOR_NOT_FOUND,
                    status=StatusCode.NOT_FOUND
                )

            response = professor.to_dict()
            logging.info(f"Response: {response}")
            return ServerResponse(data=response, status=StatusCode.OK)
        except Exception as ex:
            logging.exception("Internal server error")
            return ServerResponse(message="Internal server error",message_code=INTERNAL_SERVER_ERROR_MSG, status=StatusCode.INTERNAL_SERVER_ERROR)