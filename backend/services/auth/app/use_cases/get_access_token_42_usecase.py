from ..dtos.access_token_42 import AccessToken42
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..interfaces.services.http_client import IHttpClient
from ..constants.env_variables import EnvVariables
from ..constants.oauth_urls import OAuthUrls
import os


class GetAccessToken42UseCase(BaseUseCase):

    def __init__(self, http_client: IHttpClient):
        self.http_client = http_client

    async def execute(self, code: str) -> AccessToken42:
        client_id = os.environ.get(EnvVariables.OAUTH42_CLIENT_ID)
        secret_id = os.environ.get(EnvVariables.OAUTH42_SECRET_KEY)
        url_redirect = os.environ.get(EnvVariables.OAUTH42_REDIRECT_URI)
        data = {
            "client_id": client_id,
            "client_secret": secret_id,
            "redirect_uri": url_redirect.rstrip("/"),
            "grant_type": "authorization_code",
            "code": code,
        }
        response = self.http_client.post(
            OAuthUrls.TOKEN_URL,
            data=data,
            headers={"Content-type": "application/x-www-form-urlencoded"},
        )
        response_data = self.http_client.serialize(response)
        return AccessToken42.from_dict(response_data)
