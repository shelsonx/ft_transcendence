from ..interfaces.usecase.base_usecase import BaseUseCase
from ..interfaces.services.http_client import IHttpClient
from ..constants.env_variables import EnvVariables
from ..constants.oauth_urls import OAuthUrls
import os


class GetMe42UseCase(BaseUseCase):

    def __init__(self, http_client: IHttpClient):
        self.http_client = http_client

    async def execute(self, access_token: str):
        me_response = self.http_client.get(
            OAuthUrls.ME_OAUTH_URL, headers={"Authorization": f"Bearer {access_token}"}
        )
        me_data = self.http_client.serialize(me_response)
        return me_data
