from app.models.baseModel import BaseModel
from app.models.scripts.errors import ScriptNotFoundException
from app.models.users.user import User


class Script(BaseModel):
    def __init__(self, name, body, _id=None):
        self.name = name
        self.body = body
        super().__init__(_id)

    @classmethod
    def add(cls, user: User, new_script):
        """
        Adds a new script to the given user.
        :param user: User object
        :param new_script: The new script to be added to the user
        :return: A brand new script
        """
        script = cls(**new_script)
        user.scripts.append(script)
        user.update_mongo()
        return new_script

    @staticmethod
    def get_user_scripts(user: User):
        """
        Retrieves the information of all the scripts associated to one user.
        :param user: User object
        :return: All the scripts of the current user
        """
        return user.scripts

    @staticmethod
    def get(user: User, script_id):
        """
        Retrieves the information of the script with the given id.
        :param user: User object
        :param script_id: The id of the script to be read from the user
        :return: The requested script
        """
        for script in user.scripts:
            if script.json()["_id"] == script_id:
                return script
        raise ScriptNotFoundException("El Script con el ID dado no existe")

    @staticmethod
    def update(user: User, _id, data):
        """
        Updates the information (name and/or body message) from the script with the given id.
        :param user: User object
        :param _id: The ID of the script to be updated
        :param data: Dictionary containing the information of the name and body message to be updated
        :return: All the scripts of the current user, with updated data
        """
        for script in user.scripts:
            if script.json()["_id"] == _id:
                user.scripts[user.scripts.index(script)].name = data["name"]
                user.scripts[user.scripts.index(script)].body = data["body"]
                user.update_mongo()
                return user.scripts
        raise ScriptNotFoundException("El Script con el ID dado no existe")

    @staticmethod
    def delete(user: User, _id):
        """
        Removes from the user's array of scripts the script with the given id.
        :param user: User object
        :param _id: The ID of the script to be deleted
        :return: The remaining scripts of the user
        """
        for script in user.scripts:
            if script.json()["_id"] == _id:
                user.scripts.remove(script)
                user.update_mongo()
                return user.scripts
        raise ScriptNotFoundException("El Script con el ID dado no existe")

