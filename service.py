from flask_restful import Resource
from controllers.booking.controller import BookingController
from controllers.health.controller import HealthController
from controllers.issue.controller import IssueController
from controllers.lab.controller import LabController
from controllers.labbyId.controller import LabByIdController
from controllers.booking.controller import BookingController
from flask_restful import Api


def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    # Lab
    api.add_resource(LabController, LabController.route)
    api.add_resource(LabByIdController, LabByIdController.route)

    #Issue
    api.add_resource(IssueController, IssueController.route)

    api.add_resource(BookingController, BookingController.route)


