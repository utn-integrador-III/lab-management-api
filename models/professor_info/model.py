from bson import ObjectId
from models.professor_info.db_queries import __dbmanager__


class ProfessorInfoModel:

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
