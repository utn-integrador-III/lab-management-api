from datetime import datetime
from bson import ObjectId
from bson import ObjectId
from bson.errors import InvalidId
import pytz
from utils.message_codes import *
from models.booking.db_queries import __dbmanager__, find_by_id, update
import logging
from pymongo.errors import ServerSelectionTimeoutError
from datetime import datetime


class BookingModel:
    def __init__(self, _id=None, professor=None, professor_email=None, career=None, subject=None, lab=None, end_time=None, start_time=None, students=None, observations=None):
        self._id = _id
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
        def student_to_json(student):
            return {
                "student_email": student.get('student_email', ''),
                "student_name": student.get('student_name', ''),
                "computer": student.get('computer', ''),
                "usage_time": student.get('usage_time').isoformat() if isinstance(student.get('usage_time'), datetime) else None,
                "observations": student.get('observations', '')
            }

        return {
            "id": str(self._id) if self._id else None,
            "professor": self.professor,
            "professor_email": self.professor_email,
            "career": self.career,
            "subject": self.subject,
            "lab": self.lab,
            "end_time": self.end_time.isoformat() if isinstance(self.end_time, datetime) else None,
            "start_time": self.start_time.isoformat() if isinstance(self.start_time, datetime) else None,
            "students": [student_to_json(student) for student in self.students] if self.students else [],
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
        
    @classmethod
    def get_by_query(cls, query):
        try:
            results = __dbmanager__.get_by_query(query)
            return [cls(**doc).to_dict() for doc in results]
        except Exception as ex:
            logging.error(f"Error fetching bookings with query: {query} - {ex}")
            raise Exception(f"Error fetching bookings with query: {query}")
    @classmethod
    def get_by_id(cls, id):
        try:
            if not ObjectId.is_valid(id):
                raise InvalidId(f"Invalid ObjectId: {id}")
            return __dbmanager__.get_by_id(id)
        except InvalidId as ex:
            raise ex
        except Exception as ex:
            raise Exception(f"Error fetching booking by id {id}: {ex}")
        

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
    
    @staticmethod
    def delete_reservation(lab_id, student_email, computer):
        try:
            lab = find_by_id(lab_id)
            if not lab:
                logging.error("Laboratorio no encontrado")
                return False, 'Laboratorio no encontrado'

            logging.info(f"Estudiantes antes de eliminar la reserva: {lab['students']}")

            for student in lab['students']:
                logging.info(f"Procesando estudiante: {student}")
                if student['student_email'] == student_email and student['computer'] == computer:
                    logging.info(f"Reserva encontrada: {student}")

            new_students = [s for s in lab['students'] if not (s['student_email'] == student_email and s['computer'] == computer)]
            logging.info(f"Estudiantes después de eliminar la reserva: {new_students}")

            if len(new_students) == len(lab['students']):
                logging.error("Reserva no encontrada")
                return False, 'Reserva no encontrada'

            lab['students'] = new_students
            updated = update(lab_id, lab)
            if updated:
                logging.info("Reserva eliminada exitosamente")
                return True, 'Reserva eliminada exitosamente'
            else:
                logging.error("Error al eliminar la reserva")
                return False, 'Error al eliminar la reserva'
        except Exception as e:
            logging.exception(e)
            return False, str(e)
        
    @staticmethod
    def find_by_id(lab_book_id):
        try:
            return __dbmanager__.get_by_id(lab_book_id)
        except ServerSelectionTimeoutError as e:
            logging.error(f"Database connection error: {e}")
            raise   
    @staticmethod
    def update(lab_book_id, update_data):
        return __dbmanager__.update_data(lab_book_id, update_data)
    

    @classmethod
    def get_all_filtered_by_end_time(cls, end_time):
        try:
            booking_list=[]
            results = __dbmanager__.get_by_query({"end_time": {"$gt": end_time}})
            bookings = [BookingModel(**{k: v for k, v in result.items()}) for result in results]
            for booking in bookings:
                booking_list.append(booking.to_json())
            return booking_list
        except Exception as ex:
            logging.error(f"Failed to retrieve bookings: {ex}")
            raise Exception("Failed to retrieve bookings: " + str(ex))
        
    @staticmethod
    def delete_by_id(id):
        try:
            if not ObjectId.is_valid(id):
                raise InvalidId(f"Invalid ObjectId: {id}")
            
            if __dbmanager__.collection is None:
                logging.error("Database collection is not initialized")
                raise Exception("Database collection is not initialized")
            
            logging.info(f"Attempting to delete booking with id: {id}")
            result = __dbmanager__.collection.delete_one({"_id": ObjectId(id)})
            logging.info(f"Delete result: deleted_count={result.deleted_count}")
            if result.deleted_count == 0:
                logging.info(f"No booking found with id: {id}")
                return False
            logging.info(f"Booking with id {id} successfully deleted")
            return True
        
        except InvalidId as ex:
            logging.error(f"Invalid ObjectId: {ex}")
            raise
        except Exception as ex:
            logging.error(f"Error deleting booking with id {id}: {str(ex)}", exc_info=True)
            raise Exception(f"Error deleting booking: {ex}")