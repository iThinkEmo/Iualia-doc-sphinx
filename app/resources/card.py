from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, fresh_jwt_required

from app import Response
from app.models.cards.constants import PARSER
from app.models.cards.errors import CardNotFoundException, TokenizationFailedException, RepeatedCardException
from app.models.users.errors import UserException
from app.models.users.user import User as UserModel
from app.models.cards.card import Card as CardModel


class Cards(Resource):
    @fresh_jwt_required
    def get(self):
        """
        Retrieves the information of all the Cards of the current user.

        :return: JSON object with all the Cards
        """
        user_id = get_jwt_identity()
        user = UserModel.get_by_id(user_id)
        return [card.json() for card in CardModel.get_user_cards(user)], 200

    @fresh_jwt_required
    def post(self):
        """
        Inserts a new Card to the current user.

        :return: JSON object with the newly created Card
        """
        try:
            data = PARSER.parse_args()
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return CardModel.add(user, data), 200
        except UserException as e:
            return Response(message=e.message).json(), 401
        except TokenizationFailedException as e:
            return Response(message=e.message).json(), 400
        except RepeatedCardException as e:
            return Response(message=e.message).json(), 400


class Card(Resource):
    @fresh_jwt_required
    def get(self, card_id):
        """
        Retrieves the information of the card with the given id in the parameters.

        :param card_id: The id of the card to be read from the user

        :return: JSON object with the requested card information
        """
        try:
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return CardModel.get(user, card_id).json(), 200
        except CardNotFoundException as e:
            return Response(message=e.message).json(), 400
        except UserException as e:
            return Response(message=e.message).json(), 401

    @fresh_jwt_required
    def put(self, card_id):
        """
        Updated the card with the given id in the parameters and the JSON body.

        :param card_id: The id of the card to be updated from the user

        :return: JSON object with all the cards, with updated data
        """
        try:
            data = PARSER.parse_args()
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return [card.json() for card in CardModel.update(user, card_id, data)], 200
        except CardNotFoundException as e:
            return Response(message=e.message).json(), 400

    @fresh_jwt_required
    def delete(self, card_id):
        """
        Deletes the card with the given id in the parameters.

        :param card_id: The id of the card to be deleted from the user

        :return: JSON object with the remaining cards
        """
        try:
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return [card.json() for card in CardModel.delete(user, card_id)], 200
        except CardNotFoundException as e:
            return Response(message=e.message).json(), 400
