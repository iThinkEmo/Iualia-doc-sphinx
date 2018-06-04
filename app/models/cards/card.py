import requests
import json

from app.models.baseModel import BaseModel
from app.models.cards.constants import URL_TOKEN, URL, HEADERS
from app.models.cards.errors import CardNotFoundException, TokenizationFailedException, RepeatedCardException
from app.models.users.user import User


class Card(BaseModel):
    def __init__(self, number, name, type, token, month, year, _id=None):
        super().__init__(_id)
        self.number = number
        self.name = name
        self.type = type
        self.token = token
        self.month = month
        self.year = year

    @classmethod
    def add(cls, user: User, new_card):
        """
        Adds a new card to the given user, and uses Etomin API to tokenise it.
        :param user: User object
        :param new_card: The new card to be added to the user
        :return: A brand new card
        """

        card_info = {
            "card": {
                "cardholder": new_card.get("name"),
                "number": new_card.get("number"),
                "cvv": new_card.get("cvv"),
                "expirationDate": new_card.get("month")+"/"+new_card.get("year")
            }
        }

        auth = requests.get(URL)
        if auth.status_code == 200:
            token = requests.post(URL_TOKEN, params={}, data=json.dumps(card_info), headers=HEADERS)
            obj_token = json.loads(token.text)
            if cls.is_card_repeated(user, obj_token["token"]):
                raise RepeatedCardException("Esta tarjeta ya ha sido añadida previamente.")
            new_card["number"] = obj_token["card"]
            new_card["token"] = obj_token["token"]
            new_card.pop("cvv")
            card = cls(**new_card)
            user.cards.append(card)
            user.update_mongo()
            return new_card
        raise TokenizationFailedException("No fue posible tokenizar la tarjeta. Contacte al administrador.")

    @staticmethod
    def is_card_repeated(user: User, etomin_token):
        """
        Looks for a repeated card in the user array of cards.
        :param user: User object
        :param etomin_token: The tokenised card provided by etomin which must not be present in any other user card
        :return: Status of repeated card (True/False)
        """
        for card in user.cards:
            if card.json()["token"] == etomin_token:
                return True
        return False
    
    @staticmethod
    def get_user_cards(user: User):
        """
        Retrieves the information of all the cards associated to one user.
        :param user: User object
        :return: All the cards of the current user
        """
        return user.cards

    @staticmethod
    def get(user: User, card_id):
        """
        Retrieves the information of the card with the given id.
        :param user: User object
        :param card_id: The id of the card to be read from the user
        :return: The requested card
        """
        for card in user.cards:
            if card.json()["_id"] == card_id:
                return card
        raise CardNotFoundException("La tarjeta con el ID dado no existe")

    @staticmethod
    def update(user: User, _id, data):
        """
        Updates the information (number, name, type, and/or token) from the card with the given id.
        :param user: User object
        :param _id: The ID of the card to be updated
        :param data: Dictionary containing the information of the number, name, type, and token to be updated
        :return: All the cards of the current user, with updated data
        """
        for card in user.cards:
            if card.json()["_id"] == _id:
                user.cards[user.cards.index(card)].number = data["number"]
                user.cards[user.cards.index(card)].name = data["name"]
                user.cards[user.cards.index(card)].type = data["type"]
                user.cards[user.cards.index(card)].token = data["token"]
                user.cards[user.cards.index(card)].month = data["month"]
                user.cards[user.cards.index(card)].year = data["year"]
                user.update_mongo()
                return user.cards
        raise CardNotFoundException("La tarjeta con el ID dado no existe")

    @staticmethod
    def delete(user: User, _id):
        """
        Removes from the user's array of cards the card with the given id.
        :param user: User object
        :param _id: The ID of the card to be deleted
        :return: The remaining cards of the user
        """
        for card in user.cards:
            if card.json()["_id"] == _id:
                user.cards.remove(card)
                user.update_mongo()
                return user.cards
        raise CardNotFoundException("La tarjeta con el ID dado no existe")

