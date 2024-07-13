import logging
from models.booking.db_queries import find_by_id, update

class BookingModel:

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
