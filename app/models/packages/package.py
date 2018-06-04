import datetime

from flask_jwt_extended import get_jwt_identity

from app.models.baseModel import BaseModel
from app.models.messages.message import Message
from app.models.packages.errors import PackageNotFoundError, NotEnoughBalanceToSendPackageError
from app.models.users.user import User


class Package(BaseModel):
    def __init__(self, body=None, campaign=None, number_list=list(), script=None, messages=list(), send_time=None,
                 _id=None, created_date=None):
        self.body = body
        self.number_list = number_list
        self.script = script
        self.messages = [Message(**message) for message in messages] if messages else messages
        self.send_time = send_time
        self.campaign = campaign
        self.created_date = created_date if created_date else datetime.datetime.now()
        super().__init__(_id)

    def prepare_messages(self):
        user_id = get_jwt_identity()
        messages = list()
        default_body = ""
        if self.script:
            default_body = self.script.body
        else:
            default_body = self.body

        if self.campaign:
            [messages.append(Message(default_body, phone_number, send_time=self.send_time, user_id=user_id, package_id=self._id)) for
             phone_number in self.campaign.numbers]

        [messages.append(Message(default_body, phone_number, send_time=self.send_time, user_id=user_id, package_id=self._id)) for
         phone_number in self.number_list]

        for message in self.messages:
            if message.body == '' or message.body is None:
                message.body = default_body
            messages.append(message)
        return messages

    def get_package_data(self, user: User):
        messages_sent = self.prepare_messages()
        count_messages = len(messages_sent)
        json = self.json()
        json['messages_sent'] = [message.json() for message in messages_sent]
        json['count_messages'] = count_messages
        json['messages_cost'] = count_messages * user.sms_cost

        return json

    def send_messages(self):
        user_id = get_jwt_identity()
        user = User.get_by_id(user_id)
        messages_to_send = self.prepare_messages()
        total_cost = len(messages_to_send)* user.sms_cost
        if total_cost < user.balance and user.user_type == "pre":
            raise NotEnoughBalanceToSendPackageError(f"El usuario cuenta con {user.balance} y se necesita {total_cost}")
        [message.send() for message in messages_to_send]
        user.balance -= (messages_to_send * user.sms_cost)
        user.update_mongo()
        return messages_to_send

    @classmethod
    def add_package(cls, data, user: User):
        package = cls(**data)
        user.packages.append(package)
        user.update_mongo()
        return package

    @classmethod
    def get_package(cls, package_id, user: User):
        for package in user.packages:
            if package.json().get("_id") == package_id:
                return package

        raise PackageNotFoundError("El paquete de mensajes enviados con el id dado no ha sido encontrado")

    @classmethod
    def get_packages(cls, user):
        return user.packages
