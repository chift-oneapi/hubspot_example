# Hubspot Connector Example

This repository is a quick comparison of the code needed to achieve a simple use case with a Hubspot integration.
One is done using the requests library, illustrating how a developer would go about it and the other one is done using
the platform [Chift](https://www.chift.eu).

# How to start the connector app

Creating your `.env` file:
```shell
HUBSPOT_CLIENT_ID=<hubspot_client_id>
HUBSPOT_CLIENT_SECRET=<hubspot_client_secret>
HUBSPOT_SCOPE=oauth crm.objects.contacts.read crm.objects.companies.read
HUBSPOT_REDIRECT_URI=http://localhost:8000/callback

HUBSPOT_URL=https://app.hubspot.com
HUBSPOT_TOKEN_URL=https://api.hubapi.com/oauth/v1/token
HUBSPOT_API_URL=https://api.hubapi.com/crm/v3/objects
```

```shell
uv sync
uv run fastapi src/connector/main.py
```

It should now be accessible through your browser.

Starting the OAuth2 flow can be done through accessing the following URL:

```
http://localhost:8000/auth
```

Supported calls:
```shell
curl http://localhost:8000/contacts
curl http://localhost:8000/refresh-token?token=<your_refresh_token>
```

# Using the unified api script

## Creating your .env

```shell
CHIFT_CLIENT_ID=<chift_client_id>
CHIFT_CLIENT_SECRET=<chift_client_secret>
CHIFT_ACCOUNT_ID=<chift_client_account_id>
CHIFT_URL=https://api.chift.eu
CHIFT_CONSUMER_ID=<your_consumer_id>
```

## Executing the code

```shell
uv run python src/unified_api/main.py
```