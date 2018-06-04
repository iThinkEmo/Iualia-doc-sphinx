from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, fresh_jwt_required, jwt_required

from app import Response
from app.models.scripts.constants import PARSER
from app.models.scripts.errors import ScriptNotFoundException
from app.models.users.errors import UserException
from app.models.users.user import User as UserModel
from app.models.scripts.script import Script as ScriptModel


class Scripts(Resource):
    @jwt_required
    def get(self):
        """
        Retrieves the information of all the scripts of the current user.
        :return: JSON object with all the scripts
        """
        user_id = get_jwt_identity()
        user = UserModel.get_by_id(user_id)
        return [script.json() for script in ScriptModel.get_user_scripts(user)], 200

    @fresh_jwt_required
    def post(self):
        """
        Inserts a new script to the current user.
        :return: JSON object with the newly created script
        """
        try:
            data = PARSER.parse_args()
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return ScriptModel.add(user, data), 200
        except UserException as e:
            return Response(message=e.message).json(), 401


class Script(Resource):
    @jwt_required
    def get(self, script_id):
        """
        Retrieves the information of the script with the given id in the parameters.
        :param script_id: The id of the script to be read from the user
        :return: JSON object with the requested script information
        """
        try:
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return ScriptModel.get(user, script_id).json(), 200
        except ScriptNotFoundException as e:
            return Response(message=e.message).json(), 400
        except UserException as e:
            return Response(message=e.message).json(), 401

    @fresh_jwt_required
    def delete(self, script_id):
        """
        Deletes the script with the given id in the parameters.
        :param script_id: The id of the script to be deleted from the user
        :return: JSON object with the remaining scripts
        """
        try:
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return [script.json() for script in ScriptModel.delete(user, script_id)], 200
        except ScriptNotFoundException as e:
            return Response(message=e.message).json(), 400

    @fresh_jwt_required
    def put(self, script_id):
        """
        Updated the script with the given id in the parameters and the JSON body.
        :param script_id: The id of the script to be updated from the user
        :return: JSON object with all the scripts, with updated data
        """
        try:
            data = PARSER.parse_args()
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return [script.json() for script in ScriptModel.update(user, script_id, data)], 200
        except ScriptNotFoundException as e:
            return Response(message=e.message).json(), 400
