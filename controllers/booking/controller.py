from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.booking.model import BookingModel
import logging

class BookingController(Resource):
    route = "/booking"