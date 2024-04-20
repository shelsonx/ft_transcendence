from ..interfaces.usecase.base_usecase import BaseUseCase
from ..interfaces.services.http_client import IHttpClient
import os
from ..exceptions.invalid_access_token_exception import InvalidAccessToken
from ..constants.oauth_urls import OAuthUrls


class ValidateAccessToken42UseCase(BaseUseCase):

    def __init__(self, http_client: IHttpClient):
        self.http_client = http_client

    async def execute(self, access_token):

        response = self.http_client.get(
            OAuthUrls.VALIDATE_ACCESS_TOKEN_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status != 200:
            raise InvalidAccessToken()
        response_data = self.http_client.serialize(response)
        return response_data
