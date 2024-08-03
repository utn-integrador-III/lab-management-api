from flask_restful import Resource
from flask import request
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import ISSUE_NOT_FOUND, ISSUE_SUCCESSFULLY_UPDATED, ISSUE_UPDATE_REQUIRED, ISSUE_ID_REQUIRED
from models.issue.model import IssueModel
from utils.auth_manager import auth_required
import logging
from datetime import datetime

class IssueByCommentsController(Resource):

    route = "/issue/mngmt"

    @auth_required(permission='read', with_args=True)
    def put(self, **kwargs):
        current_user = kwargs.get('current_user', None)
        if current_user:
            print(f"Current user: {current_user}")
        else:
            print("No user data available")

        try:
            data = request.get_json()
            issue_id = data.get('_id')

            if not issue_id:
                return ServerResponse(
                    message='ID is required',
                    status=StatusCode.BAD_REQUEST,
                    message_code=ISSUE_ID_REQUIRED
                )

            issue = IssueModel.find_by_id(issue_id)

            if not issue:
                return ServerResponse(
                    message='Issue not found',
                    status=StatusCode.NOT_FOUND,
                    message_code=ISSUE_NOT_FOUND
                )

            status = data.get('status')
            new_update = data.get('new_update')
            computers = data.get('computer', [])

            if status == 'Cancelled':
                issue['status'] = 'Cancelled'
            elif status == 'Active':
                issue['status'] = 'Active'
            elif status == 'Pending':
                pass  # No changes to status

            if new_update:
                if 'update' not in issue:
                    issue['update'] = []
                issue['update'].append({
                    'date': datetime.now().isoformat(),
                    'comment': new_update
                })
            elif not new_update:
                return ServerResponse(
                    message='No changes detected',
                    status=StatusCode.NO_CONTENT,
                    message_code= ISSUE_UPDATE_REQUIRED
                )

            if computers:
                for comp in computers:
                    for issue_comp in issue['issue']:
                        if issue_comp['computer'] == comp['computer']:
                            issue_comp['is_repaired'] = comp['is_repaired']

                if all(comp['is_repaired'] for comp in issue['issue']):
                    issue['status'] = 'Done'

            IssueModel.update(issue_id, issue)

            return ServerResponse(
                message='Issue successfully updated',
                status=StatusCode.OK,
                message_code=ISSUE_SUCCESSFULLY_UPDATED,
            )

        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
