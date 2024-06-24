from flask_restful import reqparse


def query_parser_save():
    parser = reqparse.RequestParser()
    parser.add_argument('lab_name', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('lab_num', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('computers', type=list, required=True, help='This field cannot be blank')
    return parser