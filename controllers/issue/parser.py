from flask_restful import reqparse


def query_parser_save():
    parser = reqparse.RequestParser()
    parser.add_argument('lab', type=int, required=True, help="This field cannot be blank")
    parser.add_argument('date_issue', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('person', type=list, required=True, help='This field cannot be blank')
    parser.add_argument('issue', type=list, required=True, help='This field cannot be blank')
    parser.add_argument('report_to', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('observations', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('notification_date', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('status', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('update', type=list, required=True, help='This field cannot be blank')
    return parser


