import os
import requests

from app import Database
from app.models.baseModel import BaseModel
from app.models.phonenumbers.constants import COLLECTION
from app.models.phonenumbers.errors import NumberifyAcessTokenNotFound


class PhoneNumber(BaseModel):
    # el _id es el numero del telefono
    def __init__(self, _id, country_name=None, location=None, carrier=None, line_type=None):
        super().__init__(_id)
        self.country_name = country_name
        self.location = location
        self.carrier = carrier
        self.line_type = line_type

    def get_phone_data(self):
        """
        searched for the data in the numberify api and saves it to our DB
        :return: the object updated
        """
        numberify_access_token = os.environ.get("NUMBERIFY_ACCESS_TOKEN")
        if numberify_access_token is None:
            raise NumberifyAcessTokenNotFound("el token para de numberify no existe, notificar al administrador")
        response = requests.post(
            f"http://apilayer.net/api/validate?access_key={numberify_access_token}&number={self._id}&country_code=MX&format=1")

        json_data = response.json()
        self.location = json_data['location']
        self.carrier = json_data['carrier']
        self.country_name = json_data['country_name']
        self.line_type = json_data['line_type']
        self.save_to_mongo(COLLECTION)
        return self

    @classmethod
    def validate_phone_data(cls, phone_number):
        """
        given a phone number it checks if it is in our db or not, if not it saves it
        :param phone_number: number to search for
        :return: phone_object with all the data needed
        """
        phone_object = cls.get_by_id(phone_number)
        if phone_object:
            return phone_object
        else:
            phone_object = cls(phone_number)
            phone_object.get_phone_data()
        return phone_object

    def save_to_mongo(self, exclude=None):
        Database.insert(COLLECTION, self.json(exclude, date_to_string=False))

    @classmethod
    def get_by_id(cls, _id):
        user = Database.find_one(COLLECTION, {'_id': _id})
        if user:
            return cls(**user)
