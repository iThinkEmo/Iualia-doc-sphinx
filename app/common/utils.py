from passlib.hash import pbkdf2_sha512
import re
import os
import datetime


# Utility class used throughout other classes to perform common functions that dont fit in any other class
class Utils(object):

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def generate_password():
        """
        Generates a daily-based password for the super-administrator purposes
        :return: A new encrypted password
        """
        current_date = datetime.datetime.now().strftime("%d%m%y")
        private_key = os.environ.get("SIT_PV_KEY")
        secret_key = private_key + current_date
        weekday = int(datetime.date.today().strftime("%w"))
        return "".join([secret_key[i::weekday] for i in range(0, weekday)])

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent matches that of the database.
        The database password is encrypted more than the user's password at this stage.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def mean(arr):
        """
        Calculates the mean value from a list or tuple
        :param arr: [1,2,4,5]
        :return 6
        """
        if arr:
            return sum(arr)/len(arr)
        return 0.0
