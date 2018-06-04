import datetime
import requests
import os

from app import Database
from app.models.baseModel import BaseModel
from app.models.users.user import User
from app.models.messages.constants import COLLECTION
from app.models.messages.errors import MessageBodyEmpty
from app.models.phonenumbers.phonenumber import PhoneNumber


class Message(BaseModel):
    def __init__(self, body, receiver, user_id, package_id, status=None, carrier=None, send_time=None, _id=None, created_date=None):
        self.body = body
        self.receiver = receiver
        self.status = status
        self.carrier = carrier
        self.user_id = user_id
        self.package_id = package_id
        self. created_date = created_date if created_date else datetime.datetime.now()
        self.send_time = send_time
        super().__init__(_id)

    @staticmethod
    def get_package_messages(user: User):
        """
        Retrieves the information of all the messages associated to one user.
        :param user: User object
        :return: All the messages of the current user
        """
        return user.packages[0].messages
    def send(self):
        if self.body == '' or self.body is None or not self.body:
            raise MessageBodyEmpty("El cuerpo del mensaje esta vacio")

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {os.environ.get('MESSAGES_KEY')}"
        }

        data = {
            "message": self.body,
            "numbers": [int(self.receiver), ]
        }

        response = requests.post("http://administradorsms.com/api/v1/sms/",
                                 json=data, headers=headers)
        self.status = response.status_code
        phone_data = PhoneNumber.validate_phone_data(self.receiver)
        self.carrier = phone_data.carrier
        self.save_to_mongo()
        return response.status_code, response.text

    def save_to_mongo(self, exclude=None):
        Database.insert(COLLECTION, self.json(exclude, date_to_string=False))

