from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, fresh_jwt_required, jwt_required

from app import Response
from app.models.users.errors import UserException
from app.models.users.user import User as UserModel
from app.models.messages.message import Message as MessageModel

parser = reqparse.RequestParser()
parser.add_argument('body',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
parser.add_argument('receiver',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
parser.add_argument('status',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
parser.add_argument('carrier',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
parser.add_argument('sendTime',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )


class Messages(Resource):
    @jwt_required
    def get(self):
        """
        Retrieves the information of all the messages of a certain package.
        :return: JSON object with all the messages
        """
        user_id = get_jwt_identity()
        user = UserModel.get_by_id(user_id)
        return [message.json() for message in MessageModel.get_package_messages(user)], 200
