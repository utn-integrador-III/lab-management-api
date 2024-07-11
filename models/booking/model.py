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
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "students": self.students,
            "observations": self.observations,
        }

    @classmethod
    def create(cls, data):
        try:
            if "end_time" in data:
                data["end_time"] = cls._parse_datetime(data["end_time"])
            if "start_time" in data:
                data["start_time"] = cls._parse_datetime(data["start_time"])

            existing_booking = __dbmanager__.find_data({
                "professor_email": data["professor_email"],
                "career.career_id": data["career"]["career_id"],
                "subject.subject_id": data["subject"]["subject_id"],
                "lab": data["lab"],
                "start_time": data["start_time"]
            })

            if existing_booking:
                for booking in existing_booking:
                    if (booking["professor_email"] == data["professor_email"] and
                        booking["career"]["career_id"] == data["career"]["career_id"] and
                        booking["subject"]["subject_id"] == data["subject"]["subject_id"] and
                        booking["lab"] == data["lab"] and
                        booking["start_time"] == data["start_time"]):
                        return ServerResponse(
                            message="BOOKING_ALREADY_EXIST",
                            message_code=BOOKING_ALREADY_EXIST,
                            status=StatusCode.CONFLICT,
                        )
            
            booking = BookingModel(**data)
            __dbmanager__.create_data(booking.to_dict())
            return ServerResponse(booking.to_dict(), message="Booking successfully created", message_code=BOOKING_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    @staticmethod
    def _parse_datetime(date_str):
        naive_datetime = datetime.fromisoformat(date_str)
        costa_rica_tz = pytz.timezone('America/Costa_Rica')
        localized_datetime = costa_rica_tz.localize(naive_datetime)
        return localized_datetime
