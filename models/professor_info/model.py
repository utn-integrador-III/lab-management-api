import logging
from bson import ObjectId
from models.professor_info.db_queries import __dbmanager__


class ProfessorInfoModel:
    def __init__(
        self,
        professor_name=None,
        professor_email=None,
        career=None,
        subjects=None,
        _id=None,
    ):
        self.professor_name = professor_name
        self.professor_email = professor_email
        self.career = career if career else []
        self.subjects = subjects if subjects else []
        self._id = _id

    def to_dict(self):
        return {
            "professor_name": self.professor_name,
            "professor_email": self.professor_email,
            "CareerId": self.career.get("career_id") if self.career else None,
            "Career": self.career.get("career_name") if self.career else None,
            "Courses": [
                {
                    "course_id": subject.get("subject_id"),
                    "course_name": subject.get("subject_name"),
                }
                for subject in self.subjects
            ],
        }

    @classmethod
    def get_by_email(cls, professor_email):
        try:
            result = __dbmanager__.find_one({"professor_email": professor_email})
            if result:
                return cls(
                    _id=str(result.get("_id")),
                    professor_name=result.get("professor_name"),
                    professor_email=result.get("professor_email"),
                    career=result.get("career", []),
                    subjects=result.get("subject", []),
                )
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get professor by email: " + str(ex))

    @classmethod
    def convert_object_ids(cls, obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, ObjectId):
                    obj[key] = str(value)
                elif isinstance(value, list):
                    obj[key] = [cls.convert_object_ids(item) for item in value]
                elif isinstance(value, dict):
                    obj[key] = cls.convert_object_ids(value)
        return obj

    @classmethod
    def get_all(cls):
        try:
            info_db = []
            response = __dbmanager__.get_all_data()
            for info in response:
                info_db.append(info)
            return info_db
        except Exception as ex:
            raise Exception(ex)
