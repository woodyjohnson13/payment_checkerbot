import jwt

# Your JWT token
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImIyNzQ4ZDIzMTZhZjljYmZkNzA0ZjA0YWVhZmQ1NDY1MjFjNmM5ZDllYWU3MDlhNjQ1M2IyNTMxODFhMzhlYjAwMWJlODM0OWFjYjk3NzNmIn0.eyJhdWQiOiJhZjdkYzJiZS02ZjA3LTQxMjktODU3MS03NDc0ZmQxODYwMzUiLCJqdGkiOiJiMjc0OGQyMzE2YWY5Y2JmZDcwNGYwNGFlYWZkNTQ2NTIxYzZjOWQ5ZWFlNzA5YTY0NTNiMjUzMTgxYTM4ZWIwMDFiZTgzNDlhY2I5NzczZiIsImlhdCI6MTcxMjQ5NjM1MywibmJmIjoxNzEyNDk2MzUzLCJleHAiOjE3MTI1ODI3NTMsInN1YiI6IjE1NDAyNjEiLCJncmFudF90eXBlIjoiIiwiYWNjb3VudF9pZCI6MTUwMjUzNTEsImJhc2VfZG9tYWluIjoiYW1vY3JtLnJ1IiwidmVyc2lvbiI6Miwic2NvcGVzIjpbInB1c2hfbm90aWZpY2F0aW9ucyIsImZpbGVzIiwiY3JtIiwiZmlsZXNfZGVsZXRlIiwibm90aWZpY2F0aW9ucyJdLCJoYXNoX3V1aWQiOiJmYTQ4YjlkYi0xNGY5LTQ5ZmUtOTUyMi1mZTQyMGYyZGQ0ZjMifQ.jtyJB5QcxUPvFhalwQ-EzPLzYn8G_pmbilOmD7nRbOXXgQEk1USIQGMXxbdUoSz_QIJ4DfI5hFMlhLcRxe4j999VSnNzz0BH4xe7IZTmoQoD2cGIRqLjzO_1ggDDe2Lwuvy1gZiklciBApwdrWjDLCnVEgcEqhVpJzCAmauSNQ0RNaGDTQn2F1qUTA8i37KL_jpWDbSXz8FL2J7yiBiOPrq66ZVCdQc4-bRXxSGUNNoWkAtq8YuavsT7gUg-xfdgtmeIQSD1Kby9XAJQUH4Ymv42fYdGTAKZV7q9WZAQ2TqMSHrFXc98YbQDMu0EiGawW8Q9nGlyJ_BNdbBRHN_AXQ"

try:
    # Decode the token
    decoded_token = jwt.decode(token, algorithms=["RS256"], options={"verify_signature": False})

    # Print the decoded token
    print(decoded_token)
except jwt.InvalidTokenError as e:
    print("Error decoding token:", e)