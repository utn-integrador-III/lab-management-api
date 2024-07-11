from flask_restful import Resource
from controllers.health.controller import HealthController
from controllers.lab.controller import LabController
from controllers.labbyId.controller import LabByIdController
from flask_restful import Api

from controllers.professor_info.controller import ProfessorInfoController


def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    # Lab
    api.add_resource(LabController, LabController.route)
    api.add_resource(LabByIdController, LabByIdController.route)
    # Professor_info
    api.add_resource(ProfessorInfoController, ProfessorInfoController.route)
