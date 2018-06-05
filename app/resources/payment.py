from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, fresh_jwt_required, jwt_required

from app import Response
from app.models.payments.constants import PARSER
from app.models.payments.errors import PaymentException
from app.models.users.errors import UserException
from app.models.users.user import User as UserModel
from app.models.payments.payment import Payment as PaymentModel


class Payments(Resource):
    @fresh_jwt_required
    def post(self):
        """
        Inserts a new payment to the current user.

        :return: JSON object with the newly created payment
        """
        try:
            data = PARSER.parse_args()
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return PaymentModel.add(user, data), 200
        except UserException as e:
            return Response(message=e.message).json(), 401
        except PaymentException as e:
            return Response(message=e.message).json(), 400

    @jwt_required
    def get(self):
        """
        Retrieves the information of all the payments of the current user.

        :return: JSON object with all the payments
        """
        user_id = get_jwt_identity()
        user = UserModel.get_by_id(user_id)
        return [campaign.json() for campaign in PaymentModel.get_user_payments(user)], 200
