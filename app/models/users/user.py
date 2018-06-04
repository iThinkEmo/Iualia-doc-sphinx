import requests

from app import Database
from app.common.utils import Utils
from app.models.baseModel import BaseModel
from app.models.recoveries.errors import UnableToRecoverPassword
from app.models.recoveries.recovery import Recovery
from app.models.users.constants import COLLECTION
from app.models.users.errors import UserNotFoundException, UserAlreadyRegisteredError

"""
This is the user model object which will log into the api and will be able to manage its sms messages
"""


class User(BaseModel):
    def __init__(self, name, email, password, sms_cost, balance=0, user_type="pre",
                 _id=None, campaigns=list(), scripts=list(), payments=list(), packages=list(), cards=list(),
                 status=True):
        from app.models.campaigns.campaign import Campaign
        from app.models.packages.package import Package
        from app.models.scripts.script import Script
        from app.models.cards.card import Card
        from app.models.payments.payment import Payment

        self.name = name
        self.user_type = user_type
        self.campaigns = [Campaign(**campaign) for campaign in campaigns] if campaigns else campaigns
        self.email = email
        self.password = password
        self.scripts = [Script(**script) for script in scripts] if scripts else scripts
        self.payments = [Payment(**payment) for payment in payments] if payments else payments
        self.packages = [Package(**package) for package in packages] if packages else packages
        self.cards = [Card(**card) for card in cards] if cards else cards
        self.sms_cost = sms_cost
        self.balance = balance
        self.status = status
        super().__init__(_id)

    @classmethod
    def get_by_email(cls, email):
        """
        given an email it returns the  user object of the email given or raises an exception if the user is not found
        :param email: email of the user to find
        :return: user object
        """
        user = Database.find_one(COLLECTION, {"email": email})
        if user:
            return cls(**user)
        raise UserNotFoundException("El usuario con el correo dado no existe")

    @classmethod
    def register(cls, kwargs):
        """
        Registers a new user if the provided email was not found in the existing collection; also creates a new password
        :param kwargs: key word arguments that contain the new user information
        :return: user object
        """
        email = kwargs['email']
        user = User.get_by_email(email)
        if user is None:
            new_user = cls(**kwargs)
            new_user.password = Utils.hash_password(new_user.password)
            new_user.save_to_mongo()
            return new_user
        raise UserAlreadyRegisteredError("El Usuario ya existe")

    def change_user_type(self):
        """
        Changes the type of payment of the user from Prepago to Pospago and viceversa
        :return: user object
        """
        user_type = self.user_type
        if user_type == "pre":
            user_type = "pos"
        else:
            user_type = "pre"
        self.user_type = user_type
        self.update_mongo()
        return self

    def change_user_status(self):
        """
        Changes the status of the user's account (Active / Not Active)
        :return: user object
        """
        self.status = not self.status
        self.update_mongo()
        return self

    def change_user_balance(self, new_balance):
        """
        Updates the balance to the user given a new balance that can be positive or negative
        :param new_balance: balance to be updated to the user
        :return: user object
        """
        self.balance += new_balance
        self.update_mongo()
        return self

    def send_recovery_message(self):
        """
        Sends an email to the given user with the instructions to change their password
        :param self: User
        :return: POST method requesting an email to be sent to the user
        """
        recovery = Recovery(user_email=self.email)
        recovery.save_to_mongo()
        return requests.post(
            "https://api.mailgun.net/v3/sandbox6b23254da94c47f2b75358b425dd997a.mailgun.org/messages",
            auth=("api", "key-f96e4370f78e79e03e3dd6b9abe2ce10"),  # cambiar a eniroment var en produccion
            data={"from": "Databunker <postmaster@sandbox6b23254da94c47f2b75358b425dd997a.mailgun.org>",
                  # cambiar a eniroment var en produccion
                  "to": "{} <{}>".format(self.name, self.email),
                  "subject": "Recuperación de contraseña",
                  "text": "Para reestablecer la contraseña, entre de favor en el siguiente enlace: "
                          "iualia.mx/recuperarconstrasenia/{}".format(
                      recovery._id)})

    def set_password(self, password):
        """
        Creates a new password for the user and updates the previous one
        :param password: password to be updated
        :return: none
        """
        self.password = Utils.hash_password(password)

    @staticmethod
    def recover_password(recovery_id, email, password):
        """
        Updates the password of the user with the given email to the database, provided a recovery ID
        :param recovery_id: token to ensure a safe recovery
        :param email: email of the user to be found
        :param password: password to be updated
        :return: user object
        """
        if Recovery.recover_in_db(recovery_id, email):
            user = User.get_by_email(email)
            user.set_password(password)
            user.update_mongo()
            return user
        else:
            raise UnableToRecoverPassword("No se pudo hacer la recuperación de la contraseña")

    @classmethod
    def get_by_id(cls, _id):
        user = Database.find_one(COLLECTION, {'_id': _id})
        if user:
            return cls(**user)
        raise UserNotFoundException("El usuario con el token / id dado no existe.")

    def delete_from_mongo(self):
        Database.remove(COLLECTION, {"_id": self._id})

    def update_mongo(self, exclude=None):
        Database.update(COLLECTION, {"_id": self._id}, self.json(exclude, date_to_string=False))

    def save_to_mongo(self, exclude=None):

        Database.insert(COLLECTION, self.json(exclude, date_to_string=False))
