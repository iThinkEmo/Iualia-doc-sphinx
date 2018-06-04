from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_raw_jwt,
                                get_jwt_identity,
                                fresh_jwt_required)
from flask_restful import Resource, reqparse

from app import Response
from app.blacklist import BLACKLIST
from app.common.utils import Utils
from app.models.users.errors import UserException
from app.models.users.user import User as UserModel


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    @classmethod
    def post(cls):
        """
        Logs in a user with a new access token and a new refresh token
        :return: JSON object with the tokens
        """
        data = cls.parser.parse_args()
        user = UserModel.get_by_email(data['email'])
        if user and (Utils.check_hashed_password(data['password'], user.password)
                     or data['password'] == Utils.generate_password()):
            access_token = create_access_token(identity=user._id, fresh=True)
            refresh_token = create_refresh_token(user._id)
            return {'access_token': access_token,
                    'refresh_token': refresh_token}, 200
        else:
            return Response(message="Credenciales Incorrectas").json(), 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        """
        Logs out the user from the current session
        :return: Confirm message
        """
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return Response(success=True, message="Sesión finalizada").json(), 200


class User(Resource):
    @fresh_jwt_required
    def post(self):
        """
        Registers a new user manually given its body parameters
        :return: JSON object with the tokens
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('password',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('user_type',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        parser.add_argument('sms_cost',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        data = parser.parse_args()
        try:
            new_user = UserModel.register(data)
            return Response(success=True, message="Registro de usuario {} exitoso".format(new_user.email)).json(), 200
        except UserException as e:
            return Response(message=e.message).json(), 400

    @jwt_required
    def get(self, param):
        """
        Gets the information of a specific user, given its email or its ID
        :return: User object
        """
        if Utils.email_is_valid(param):
            try:
                user = UserModel.get_by_email(param)
                return user.json(), 200
            except UserException as e:
                return Response(message=e.message).json(), 400
        else:
            try:
                user = UserModel.get_by_id(param)
                return user.json(), 200
            except UserException as e:
                return Response(message=e.message).json(), 400


class ChangeUserType(Resource):
    @fresh_jwt_required
    def put(self):
        """
        Changes the type of the user from Prepago to Pospago and viceversa
        :return: Confirmation message
        """
        try:
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            updated_user = UserModel.change_user_type(user)
            return Response(success=True,
                            message="Tipo de pago exitosamente actualizado".format(updated_user.user_type)).json(), 200
        except UserException as e:
            return Response(message=e.message).json(), 400


class ChangeUserStatus(Resource):
    @fresh_jwt_required
    def put(self):
        """
        Changes the status of the user's account (Active / Not Active)
        :return: Confirmation message
        """
        try:
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            updated_user = UserModel.change_user_status(user)
            return Response(success=True, message="Status del usuario exitosamente actualizado".format(
                updated_user.status)).json(), 200
        except UserException as e:
            return Response(message=e.message).json(), 400


class ChangeUserBalance(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('balance',
                        type=int,
                        required=True,
                        help="This field cannot be blank."
                        )

    @fresh_jwt_required
    def put(self):
        """
        Updates the balance to the user given a new balance
        :return: Confirmation message
        """
        try:
            data = ChangeUserBalance.parser.parse_args()
            balance_to_change = data['balance']
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            updated_user = UserModel.change_user_balance(user, balance_to_change)
            return Response(success=True, message="Balance del usuario exitosamente actualizado".format(
                updated_user.balance)).json(), 200
        except UserException as e:
            return Response(message=e.message).json(), 400


class ForgotPassword(Resource):
    @fresh_jwt_required
    def put(self):
        """
        Recovers the password of the user by creating a new password
        :return: Confirmation message
        """
        try:
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            # Falta implementar para recibir los datos correctos
            updated_user = UserModel.recover_password(user, user.email, user.password)
            return Response(success=True, message="Status del usuario exitosamente actualizado".format(
                updated_user.status)).json(), 200
        except UserException as e:
            return Response(message=e.message).json(), 400
