import os
import requests
from amocrm.v2 import tokens,Lead
from dotenv import load_dotenv


load_dotenv(override=True)

amo_client_id=os.getenv('AMO_CLIENT_ID')
amo_client_secret=os.getenv('AMO_CLIENT_SECRET')
amo_redirect_url=os.getenv('AMO_REDIRECT_URL')
amo_subdomain=os.getenv('AMO_SUBDOMAIN')


# class AmoCRM:
#     def __init__(self, client_id, client_secret, subdomain, redirect_url, storage=None):
#         self.client_id = client_id
#         self.client_secret = client_secret
#         self.subdomain = subdomain
#         self.redirect_url = redirect_url
#         self.storage = storage or tokens.FileTokensStorage()  # Use default storage if not provided
#         self.default_manager = tokens.default_token_manager(
#             client_id=self.client_id,
#             client_secret=self.client_secret,
#             subdomain=self.subdomain,
#             redirect_url=self.redirect_url,
#             storage=self.storage
#         )

#     def initialize_token(self, code, skip_error=True):
#         self.default_manager.init(code=code, skip_error=skip_error)


def refresh_tokens():
        # Read refresh token from file
        with open("keys/refresh_token.txt", "r") as f:
            refresh_token = f.read().strip()

        # Prepare request body
        body = {
            "client_id": amo_client_id,
            "client_secret": amo_client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "redirect_uri": amo_redirect_url
        }

        # Make POST request to refresh tokens
        response = requests.post("https://propnevmo.amocrm.ru/oauth2/access_token", json=body)

        if response.status_code == 200:
            data = response.json()
            print(data)
            access_token = data.get("access_token")
            new_refresh_token = data.get("refresh_token")

            with open("keys/refresh_token.txt", "w") as f:
                f.write(new_refresh_token)

            with open("keys/access_token.txt", "w") as f:
                f.write(access_token)

            print("Tokens refreshed successfully.")
        else:
            print("Failed to refresh tokens.")






tokens.default_token_manager(
    client_id=amo_client_id,
    client_secret=amo_client_secret,
    subdomain=amo_subdomain,
    redirect_url=amo_redirect_url,
    storage=tokens.FileTokensStorage('keys'),  # by default FileTokensStorage
)

# tokens.default_token_manager.init(code="def5020086ea21099c4b67c76f683fadb0775143184f6157cff3ca64de0d316b0a42a8a47b40b47f9b9be39f17ce8a79eaad5d8b1dd001ca4682984a95124f0c330f91093c995a6cd579c34c8a10f84feadbc5526a1d4c0d31a9d4b43cf5f46c04d4880ab196a548c3b259977ba687564ad8a30e6cdc1d77217fa9b735f04ddae62679d3e5221b2d5f2176c6d638bd52ce762066c4747c3be0579b29698ec32b2675649b9f4b34a23db5799758825c73c0eefcf605fbc0924537c1457c5d513a0c69e30214f9d4591569f8fa6abde03f26ce516513b858743b5a1d247b800e9ef7c2526fe0c62aebeb6c9b8b94716442c9c822b04b3932142cc66bb85dfb93d5bb8417c639f7b657ca2aff57f1b886cc796a62bb6d49a9f175186256b2c02f3fb2876d65d5586c24e615a4599c71383f3beb64d873f68ca4ef124dd7cda2e5f8066b66b9c38446cbb9ecea53f87c2a323f161946b11816889a59ab06573fd2caf09d6dfb2aaf0fa2c3d20dcc39e9661218ac74f209feed83241922a26edd0376e5e2dc2809acba5111d4cbc2e076a8d547faabb618f9eccce85ce5030a531f4f643936f1d064b964f42a588bf0dc6512401268d8d93d84d9c8cd7a9cc52cb820473ef6eddc34e15abe3015417ae26bde5e30ba31b31be2be8c10bc6c3066df6581c2c0074ba779", skip_error=False)

refresh_tokens()

leads=Lead.objects.get(object_id=6622277)

print(leads)
