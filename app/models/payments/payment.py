import os
import requests
import json

from app.models.baseModel import BaseModel
from app.models.payments.constants import CURRENCY, PAYMENT_COUNTRY, URL, URL_CHARGE, HEADERS
from app.models.payments.errors import PaymentFailedException
from app.models.users.user import User


class Payment(BaseModel):
    def __init__(self, status, payment_method, amount, date, id_card, etomin_number=None, id_reference=None, _id=None):
        self.status = status
        self.payment_method = payment_method
        self.amount = amount
        self.etomin_number = etomin_number
        self.date = date
        self.id_reference = id_reference
        self.id_card = id_card
        super().__init__(_id)

    @classmethod
    def add(cls, user: User, new_payment):
        """
        Adds a new payment to the given user.
        :param user: User object
        :param new_payment: The new payment to be added to the user
        :return: A brand new payment
        """

        new_payment["status"] = "PENDIENTE"
        etomin_number = ""
        for card in user.cards:
            if card.json()["_id"] == new_payment["id_card"]:
                etomin_number = user.cards[user.cards.index(card)].token
        payment = cls(**new_payment)
        params = {
            "public_key": os.environ.get("ETOMIN_PB_KEY"),
            "transaction": {
                "payer": {
                    "email": user.email
                },
                "order": {
                    "external_reference": payment._id
                },
                "payment": {
                    "amount": new_payment.get("amount"),
                    "payment_method": new_payment.get("payment_method"),
                    "currency": CURRENCY,
                    "payment_country": PAYMENT_COUNTRY,
                    "token": etomin_number
                },
                "payment_pending": False,
                "device_session_id": ""
            },
            "test": True
        }

        auth = requests.get(URL)
        if auth.status_code == 200:
            obj = json.loads(auth.text)
            params["transaction"]["device_session_id"] = obj["session_id"]
            charge = requests.post(URL_CHARGE, params={}, data=json.dumps(params), headers=HEADERS)
            obj_charge = json.loads(charge.text)
            if obj_charge.get("error") == '0':
                payment.status = "APROBADO"
                payment.id_reference = obj_charge.get("authorization_code")
                payment.etomin_number = obj_charge.get("card_token")
                new_payment["status"] = "APROBADO"
                user.change_user_balance(-new_payment.get("amount"))
                user.payments.append(payment)
                user.update_mongo()
                return new_payment
            else:
                payment.status = "RECHAZADO"
                payment.etomin_number = etomin_number
                user.payments.append(payment)
                user.update_mongo()
                raise PaymentFailedException(obj_charge.get("message"))

    @staticmethod
    def get_user_payments(user: User):
        """
        Retrieves the information of all the payments associated to one user.
        :param user: User object
        :return: All the payments of the current user
        """
        # user.payments = []
        # user.update_mongo()
        return user.payments
