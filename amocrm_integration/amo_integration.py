import os
import requests
from amocrm.v2 import tokens,Lead
from dotenv import load_dotenv


load_dotenv(override=True)

amo_client_id=os.getenv('AMO_CLIENT_ID')
amo_client_secret=os.getenv('AMO_CLIENT_SECRET')
amo_redirect_url=os.getenv('AMO_REDIRECT_URL')
amo_subdomain=os.getenv('AMO_SUBDOMAIN')

current_directory = os.path.dirname(os.path.abspath(__file__))
keys_directory = os.path.join(current_directory, "keys")


class AmoCRM:
    def __init__(self, client_id, client_secret, subdomain, redirect_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.subdomain = subdomain
        self.redirect_url = redirect_url
        self.storage = tokens.FileTokensStorage(keys_directory)  # Use default storage if not provided
        self.default_manager = tokens.default_token_manager(
            client_id=self.client_id,
            client_secret=self.client_secret,
            subdomain=self.subdomain,
            redirect_url=self.redirect_url,
            storage=self.storage
        )

    def initialize_token(self, code, skip_error=True):
        self.default_manager.init(code=code, skip_error=skip_error)

    def refresh_tokens(self):
        with open("keys/refresh_token.txt", "r") as f:
            refresh_token = f.read().strip()

        body = {
            "client_id": amo_client_id,
            "client_secret": amo_client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "redirect_uri": amo_redirect_url
        }

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

    def get_lead_by_id(self,lead_id):
        try:
            lead = Lead.objects.get(object_id=lead_id)
            return lead
        except Exception as e:
            return False  # Return None when lead is not found






# tokens.default_token_manager(
#     client_id=amo_client_id,
#     client_secret=amo_client_secret,
#     subdomain=amo_subdomain,
#     redirect_url=amo_redirect_url,
#     storage=tokens.FileTokensStorage(keys_directory),  # by default FileTokensStorage
# )

# tokens.default_token_manager.init(code="def5020085c16e3322a3546d03b41c6e27bf0bb44238eb372531654e50730fbeaf19f0088676343d2579d046b8551a7d156ab9cc9e9a8172ba52438c7c0ed6476af0ab4749c7c8a0c9401cb8d58a8f77767d37ee74664c14e8bbfdb900212a722ecf62acbcc2d6a65f6a21be62db817d3a5e51fa78654dca2ce49c69e43f62257fe31dc4b5c031ac9e50b1e510b6a43889e1294f61bf65126a6ad078627de930435170d393cc5eff0849f7405760093041ea15620b5174863c977d3f612c58f6e763eb430368efe5687bc4384c9f53eff30fa9ac2cf2338182e29852c4761ea59d49d1673ddebeddc2b87ccd9c3d601a5de1827c2b5f95df52ae3cb339288f9ee8f0f697f7aa83ec9db0e8781a3e407dfa01ef4fea28529d3f86dbdddced6ae0502fb639b99dc78f93ff86aa3fff6901eef430aaa2f0bca94f2d9482f0b6f2eb56c17cd7cc29cc9c7160e228449a00ea5d32867c31a07baaa4a3aae744c3335520ad49cf51a6e609c00a9af8662e983457d7ffb3b774fa4bf64e894bc646012cc16f233d0c79ab65ad13debff1eb6d2cbe743ef81fdb056dd1eef31886bc8f89ed09df78ef389c459aaada1e636b1741105c17699e96a4568e48e98535e9a7de1c86ae33a3f8d64142ad7a54053093c802e9d1b4d7ffb168670258b4e9976ce3277f0860943431", skip_error=False)

# lead=Lead.objects.get(object_id=6622277)
# print(lead)
# my_amo=AmoCRM(amo_client_id,amo_client_secret,amo_subdomain,amo_redirect_url)
# print(my_amo.get_lead_by_id(6622277))
