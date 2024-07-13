from flask_restful import Resource
from controllers.health.controller import HealthController
from controllers.lab.controller import LabController
from controllers.labbyId.controller import LabByIdController
from controllers.booking.controller import BookingController
from flask_restful import Api

from controllers.professor.controller import ProfessorController


def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    # Lab
    api.add_resource(LabController, LabController.route)
    api.add_resource(LabByIdController, LabByIdController.route)
    # Booking
    api.add_resource(BookingController, BookingController.route)
    #Professor
    api.add_resource(ProfessorController, ProfessorController.route)
