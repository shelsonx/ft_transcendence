import os
import urllib.parse
from ..constants.env_variables import EnvVariables


def build_oauth42_url() -> str:
    client_id = os.getenv(EnvVariables.OAUTH42_CLIENT_ID)
    url_redirect = os.getenv(EnvVariables.OAUTH42_REDIRECT_URI)
    url_redirect_enconded = urllib.parse.quote_plus(url_redirect)
    url_42 = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={url_redirect_enconded}&response_type=code"
    return url_42
