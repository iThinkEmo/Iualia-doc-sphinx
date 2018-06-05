from app.models.baseModel import BaseModel
from app.models.campaigns.errors import CampaignNotFoundException
from app.models.users.user import User


class Campaign(BaseModel):
    def __init__(self, name, numbers=list(), _id=None):
        super().__init__(_id)
        self.name = name
        self.numbers = numbers

    @classmethod
    def add(cls, user: User, new_campaign):
        """
        Adds a new campaign to the given user.

        :param user: User object
        :param new_campaign: The new campaign to be added to the user

        :return: A brand new campaign
        """
        campaign = cls(**new_campaign)
        user.campaigns.append(campaign)
        user.update_mongo()
        return new_campaign

    @staticmethod
    def get(user: User, campaign_id):
        """
        Retrieves the information of the campaign with the given id.

        :param user: User object
        :param campaign_id: The id of the campaign to be read from the user

        :return: The requested campaign
        """
        for campaign in user.campaigns:
            if campaign.json()["_id"] == campaign_id:
                return campaign
        raise CampaignNotFoundException("La campaña con el ID dado no existe")

    @staticmethod
    def delete(user: User, _id):
        """
        Removes from the user's array of campaigns the campaign with the given id.

        :param user: User object
        :param _id: The ID of the campaign to be deleted

        :return: The remaining campaigns of the user
        """
        for campaign in user.campaigns:
            if campaign.json()["_id"] == _id:
                user.campaigns.remove(campaign)
                user.update_mongo()
                return user.campaigns
        raise CampaignNotFoundException("La campaña con el ID dado no existe")

    @staticmethod
    def update(user: User, _id, data):
        """
        Updates the information (name and/or numbers) from the campaign with the given id.

        :param user: User object
        :param _id: The ID of the campaign to be updated
        :param data: Dictionary containing the information of the name and numbers to be updated

        :return: All the campaigns of the current user, with updated data
        """
        for campaign in user.campaigns:
            if campaign.json()["_id"] == _id:
                user.campaigns[user.campaigns.index(campaign)].numbers = data["numbers"]
                user.campaigns[user.campaigns.index(campaign)].name = data["name"]
                user.update_mongo()
                return user.campaigns
        raise CampaignNotFoundException("La campaña con el ID dado no existe")

    @staticmethod
    def get_user_campaigns(user: User):
        """
        Retrieves the information of all the campaigns associated to one user.

        :param user: User object

        :return: All the campaigns of the current user
        """
        return user.campaigns
