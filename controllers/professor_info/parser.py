from flask_restful import reqparse
import json


def query_parser_save():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "professor_email", type=str, required=True, help="This field cannot be blank"
    )
    parser.add_argument(
        "professor_name", type=str, required=True, help="This field cannot be blank"
    )
    parser.add_argument(
        "career",
        type=lambda x: json.loads(x),
        required=True,
        help="This field cannot be blank",
    )
    parser.add_argument(
        "subject",
        type=lambda x: json.loads(x),
        required=False,
        help="This field can be an array",
    )
    return parser
