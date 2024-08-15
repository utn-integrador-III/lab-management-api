from flask_restful import Resource
from controllers.IssueByComments.controller import IssueByCommentsController
from controllers.booking.controller import BookingController
from controllers.bookingbyId.controller import BookingByIdController
from controllers.health.controller import HealthController
from controllers.issue.controller import IssueController
from controllers.issueId.controller import IssueByIdController
from controllers.lab.controller import LabController
from controllers.labbyId.controller import LabByIdController
from controllers.booking.controller import BookingController
from controllers.bookingComputer.controller import BookingComputerController
from flask_restful import Api
from controllers.professor_info.controller import ProfessorInfoController
from controllers.professorByEmail.controller import ProfessorByEmailController
from controllers.bookingbyDate.controller import BookingByDateController


def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    # Lab
    api.add_resource(LabController, LabController.route)
    api.add_resource(LabByIdController, LabByIdController.route)

    # Professor_info
    api.add_resource(ProfessorInfoController, ProfessorInfoController.route)

    # Professor
    api.add_resource(ProfessorByEmailController, ProfessorByEmailController.route)

    # Booking
    api.add_resource(BookingController, BookingController.route)
    api.add_resource(BookingComputerController, BookingComputerController.route)
    api.add_resource(BookingByIdController, BookingByIdController.route)
    api.add_resource(BookingByDateController, BookingByDateController.route)
    # Issue
    api.add_resource(IssueController, IssueController.route)
    api.add_resource(IssueByIdController, IssueByIdController.route)
    api.add_resource(IssueByCommentsController, IssueByCommentsController.route)

