from flask_restful import reqparse

def bookingcomputer_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str, required=True, help="Este campo no puede estar en blanco")
    parser.add_argument('student_email', type=str, required=True, help="Este campo no puede estar en blanco")
    parser.add_argument('computer', type=str, required=True, help="Este campo no puede estar en blanco")
    return parser
