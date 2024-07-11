from flask_restful import reqparse


def query_parser_post():
    parser = reqparse.RequestParser()
    parser.add_argument('professor', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('professor_email', type=str, required=True, help='This field cannot be blank')  
    parser.add_argument('career', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('subject', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('lab', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('end_time', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('start_time', type=str, required=True, help='This field cannot be blank')
    return parser