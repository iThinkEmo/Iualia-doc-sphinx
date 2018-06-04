from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app.blacklist import BLACKLIST
from app.common.database import Database
from app.common.response import Response
from app.resources.user import (UserLogin,
                                User,
                                ChangeUserType,
                                ChangeUserStatus,
                                ChangeUserBalance,
                                UserLogout,
                                ForgotPassword)
from app.resources.campaign import Campaigns, Campaign
from app.resources.script import Scripts, Script
from app.resources.card import Cards, Card
from app.resources.package import Package, Packages, PackageDetail
from app.resources.payment import Payments
from app.resources.message import Messages
from app.resources.refresh import RefreshToken
from config import config


def create_app(config_name):
    app = Flask(__name__)
    api = Api(app)
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        return decrypted_token['jti'] in BLACKLIST

    @jwt.expired_token_loader
    def expired_token_callback():
        return jsonify(Response(message="El token de acceso ha expirado, inicie sesión nuevamente").json()), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify(Response(message='el token no es valido:').json()), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return jsonify(Response(message="es necesario un token de accesso para continuar").json()), 401

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback():
        return jsonify(Response(message="Esta operación requiere un token nuevo, incia sesión otra vez").json())

    @jwt.revoked_token_loader
    def revoked_token_loader():
        return jsonify(Response(message="El token ha sido revocado y yo no es válido"))

    app.config.from_object(config[config_name])
    # Register our blueprints
    from .default import default as default_blueprint
    app.register_blueprint(default_blueprint)

    api.add_resource(UserLogin, '/login')
    api.add_resource(User, '/user', '/user/<string:param>')
    api.add_resource(ChangeUserType, '/user/change_user_type')
    api.add_resource(ChangeUserStatus, '/user/change_status')
    api.add_resource(ChangeUserBalance, '/user/change_balance')
    api.add_resource(Campaigns, '/user/campaigns')
    api.add_resource(Campaign, '/user/campaign/<string:campaign_id>')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(RefreshToken, '/refresh')
    api.add_resource(ForgotPassword, '/user/forgot_password')

    api.add_resource(Scripts, '/user/scripts')
    api.add_resource(Script, '/user/script/<string:script_id>')

    api.add_resource(Cards, '/user/cards')
    api.add_resource(Card, '/user/card/<string:card_id>')

    api.add_resource(Package, '/user/packages')

    api.add_resource(Messages, '/user/messages')

    api.add_resource(Payments, '/user/payments')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    @app.before_first_request
    def init_db():
        Database.initialize()

    return app
