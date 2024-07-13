# controllers/professor_controller.py
from flask_restful import Resource
from flask import request
from utils.server_response import *
from utils.message_codes import *
import logging
from models.professor.model import ProfessorModel
from flask import request

class ProfessorController(Resource):
    route = "/professor"

    def get(self):
        try:
            professor_email = request.args.get('professor_email')
            if not professor_email:
                logging.error("professor_email parameter is required")
                return ServerResponse(
                    message_code=PROFESSOR_EMAIL_REQUIRED,
                    status=StatusCode.BAD_REQUEST
                )

            professor = ProfessorModel.get_by_email(professor_email)
            if not professor:
                logging.error(f"Professor not found for email: {professor_email}")
                return ServerResponse(
                    message_code=PROFESSOR_NOT_FOUND,
                    status=StatusCode.NOT_FOUND
                )

            response = professor.to_dict()
            logging.info(f"Response: {response}")
            return ServerResponse(data=response, status=StatusCode.OK)
        except Exception as ex:
            logging.exception("Internal server error")
            return ServerResponse(message_code=HEALTH_NOT_FOUND, status=StatusCode.INTERNAL_SERVER_ERROR)