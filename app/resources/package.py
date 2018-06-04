from flask_jwt_extended import jwt_required, get_jwt_identity, fresh_jwt_required
from flask_restful import Resource, reqparse

from app.models.users.user import User as UserModel
from app.models.packages.package import Package as PackageModel

parser = reqparse.RequestParser()
parser.add_argument('body',
                    type=str,
                    required=False,
                    help="Este campo no puede ser dejado en blanco."
                    )
parser.add_argument('number_list',
                    type=str,
                    required=False,
                    help="Este campo no puede ser dejado en blanco.",
                    action='append'
                    )
parser.add_argument('script',
                    type=dict,
                    required=False,
                    help="Este campo no puede ser dejado en blanco.",
                    )
parser.add_argument('campaign',
                    type=dict,
                    required=False,
                    help="Este campo no puede ser dejado en blanco.",
                    )
parser.add_argument('send_time',
                    type=str,
                    required=False,
                    help="Este campo no puede ser dejado en blanco.",
                    )
parser.add_argument('messages',
                    type=dict,
                    required=False,
                    help="Este campo no puede ser dejado en blanco.",
                    action='append',
                    )


class Package(Resource):
    @jwt_required
    def get(self, package_id):
        user_id = get_jwt_identity()
        user = UserModel.get_by_id(user_id)
        return PackageModel.get_package(package_id, user).json(), 200

    @fresh_jwt_required
    def post(self):
        data = parser.parse_args()
        user_id = get_jwt_identity()
        user = UserModel.get_by_id(user_id)
        return PackageModel.add_package(data, user).json(), 200


class Packages(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.get_by_id(user_id)
        return [package.json for package in PackageModel.get_packages(user)], 200

    @fresh_jwt_required
    def post(self, package_id):
        user_id = get_jwt_identity()
        user = UserModel.get_by_id(user_id)
        package = PackageModel.get_package(package_id, user)
        return package.send_messages()


class PackageDetail(Resource):
    @jwt_required
    def get(self, package_id):
        user_id = get_jwt_identity()
        user = UserModel.get_by_id(user_id)
        package = PackageModel.get_package(package_id, user)
        return package.get_package_data(user)
