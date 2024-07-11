from datetime import datetime
import pytz
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from models.booking.db_queries import __dbmanager__
import logging

class BookingModel:
    def __init__(self, professor=None, professor_email=None, career=None, subject=None, lab=None, end_time=None, start_time=None, students=None, observations=None):
        self.professor = professor
        self.professor_email = professor_email
        self.career = career if career else {}
        self.subject = subject if subject else {}
        self.lab = lab
        self.end_time = end_time
        self.start_time = start_time
        self.students = students if students else []
        self.observations = observations

    def to_dict(self):
        return {
            "professor": self.professor,
            "professor_email": self.professor_email,
            "career": self.career,
            "subject": self.subject,
            "lab": self.lab,
            "end_time": self.end_time,
            "start_time": self.start_time,
            "students": self.students,
            "observations": self.observations,
        }

    def to_json(self):
        return {
            "professor": self.professor,
            "professor_email": self.professor_email,
            "career": self.career,
            "subject": self.subject,
            "lab": self.lab,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "students": self.students,
            "observations": self.observations,
        }

    @classmethod
    def create(cls, data):
        try:
            if "end_time" in data and isinstance(data["end_time"], str):
                data["end_time"] = cls._parse_datetime(data["end_time"])
            if "start_time" in data and isinstance(data["start_time"], str):
                data["start_time"] = cls._parse_datetime(data["start_time"])

            booking = BookingModel(**data)
            __dbmanager__.create_data(booking.to_dict())
            return booking
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to create booking: " + str(ex))

    @staticmethod
    def _parse_datetime(date_str):
        # Parse the string to a datetime object
        parsed_datetime = datetime.fromisoformat(date_str)
        costa_rica_tz = pytz.timezone('America/Costa_Rica')

        # If the datetime is naive, localize it; otherwise, convert it to the desired time zone
        if parsed_datetime.tzinfo is None:
            localized_datetime = costa_rica_tz.localize(parsed_datetime)
        else:
            localized_datetime = parsed_datetime.astimezone(costa_rica_tz)
        
        return localized_datetime
