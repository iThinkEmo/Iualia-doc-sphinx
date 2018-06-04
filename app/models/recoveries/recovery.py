import uuid

from app.models.recoveries.constants import COLLECTION
from app.common.database import Database


class Recovery(object):
    def __init__(self, user_email, _id=None):
        self.user_email = user_email
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        "recovery with id {} for user: {}".format(self._id, self.user_email)

    def save_to_mongo(self):
        Database.insert(COLLECTION, self.json())

    def remove_from_mongo(self):
        Database.remove(COLLECTION, self.json())

    @classmethod
    def get_recovery(cls, _id=None):
        """
        Fetches a list of the all the Recovery objects in the given collection
        :param _id: The specific ID of a particular collection
        :return: List of Recovery objects or one specific Recovery object
        """
        if _id is None:
            return [cls(**recovery) for recovery in Database.find(COLLECTION, {})]

        else:
            return [cls(Database.find_one(COLLECTION, {'_id': _id}))]

    @classmethod
    def get_recovery_by_email(cls, user_email):
        """
        Finds the Recovery object with the given user email
        :param user_email: user object to be updated
        :return: Recovery object
        """
        Database.find_one(COLLECTION, {'user_email': user_email})

    def json(self):
        """
        Creates a JSON object with the id and the user email
        :return: JSON object
        """
        return {
            '_id': self._id,
            'user_email': self.user_email
        }

    @classmethod
    def recover_in_db(cls, recovery_id, email):
        """
        Recovers the password in the database with a unique recovery ID
        :param recovery_id: ID to ensure a secure recuperation of the password
        :return: Boolean
        """
        recovery_in_DB = cls(**Database.find_one(COLLECTION, {'_id': recovery_id}))
        if recovery_in_DB is None:
            return False
        else:
            Database.remove(COLLECTION, {'_id': recovery_id})
            return True