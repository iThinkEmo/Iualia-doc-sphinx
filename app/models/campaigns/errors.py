class CampaignException(Exception):
    def __init__(self, message):
        self.message = message


class CampaignNotFoundException(CampaignException):
    pass