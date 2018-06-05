from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, fresh_jwt_required, jwt_required

from app import Response
from app.models.campaigns.constants import PARSER
from app.models.campaigns.errors import CampaignNotFoundException
from app.models.users.errors import UserException
from app.models.users.user import User as UserModel
from app.models.campaigns.campaign import Campaign as CampaignModel


class Campaigns(Resource):
    @jwt_required
    def get(self):
        """
        Retrieves the information of all the campaigns of the current user.

        :return: JSON object with all the campaigns
        """
        user_id = get_jwt_identity()
        user = UserModel.get_by_id(user_id)
        return [campaign.json() for campaign in CampaignModel.get_user_campaigns(user)], 200

    @fresh_jwt_required
    def post(self):
        """
        Inserts a new campaign to the current user.

        :return: JSON object with the newly created campaign
        """
        try:
            data = PARSER.parse_args()
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return CampaignModel.add(user, data), 200
        except UserException as e:
            return Response(message=e.message).json(), 401


class Campaign(Resource):
    @jwt_required
    def get(self, campaign_id):
        """
        Retrieves the information of the campaign with the given id in the parameters.

        :param campaign_id: The id of the campaign to be read from the user

        :return: JSON object with the requested campaign information
        """
        try:
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return CampaignModel.get(user, campaign_id).json(), 200
        except CampaignNotFoundException as e:
            return Response(message=e.message).json(), 400
        except UserException as e:
            return Response(message=e.message).json(), 401

    @fresh_jwt_required
    def delete(self, campaign_id):
        """
        Deletes the campaign with the given id in the parameters.

        :param campaign_id: The id of the campaign to be deleted from the user

        :return: JSON object with the remaining campaigns
        """
        try:
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return [campaign.json() for campaign in CampaignModel.delete(user, campaign_id)], 200
        except CampaignNotFoundException as e:
            return Response(message=e.message).json(), 400

    @fresh_jwt_required
    def put(self, campaign_id):
        """
        Updated the campaign with the given id in the parameters and the JSON body.

        :param campaign_id: The id of the campaign to be updated from the user

        :return: JSON object with all the campaigns, with updated data
        """
        try:
            data = PARSER.parse_args()
            user_id = get_jwt_identity()
            user = UserModel.get_by_id(user_id)
            return [campaign.json() for campaign in CampaignModel.update(user, campaign_id, data)], 200
        except CampaignNotFoundException as e:
            return Response(message=e.message).json(), 400
