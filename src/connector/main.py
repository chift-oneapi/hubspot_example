import os
import string
import random

import requests
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()


def generate_state():
    """Generates random string of letters to use for auth"""
    return "".join(random.choices(string.ascii_letters, k=15))


app = FastAPI()


@app.get("/auth")
def get_auth():
    """Start OAuth2 process."""
    state = generate_state()
    response = requests.get(
        f"{os.getenv('HUBSPOT_URL')}/oauth/authorize?"
        + f"client_id={quote(os.getenv('HUBSPOT_CLIENT_ID'))}&"
        f"scope={quote(os.getenv('HUBSPOT_SCOPE'))}&"
        f"redirect_uri={quote(os.getenv('HUBSPOT_REDIRECT_URI'))}&"
        f"state={quote(state)}"
    )
    app.state = state
    return RedirectResponse(response.url)


@app.get("/callback")
def callback(request: Request, code: str, state: str):
    """Callback endpoint for OAuth2"""
    if state != app.state:
        return JSONResponse(
            "State received is different from the one generated in first authentication step",
            400,
        )
    data = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("HUBSPOT_CLIENT_ID"),
        "client_secret": os.getenv("HUBSPOT_CLIENT_SECRET"),
        "redirect_uri": os.getenv("HUBSPOT_REDIRECT_URI"),
        "code": code,
    }
    response = requests.post(f"{os.getenv('HUBSPOT_TOKEN_URL')}", data).json()
    return JSONResponse(
        {
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
        }
    )


@app.get("/refresh-token")
def get_new_token(request: Request, refresh_token: str):
    """Retrieves a new access token and refresh token derived from provided refresh token."""
    data = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("HUBSPOT_CLIENT_ID"),
        "client_secret": os.getenv("HUBSPOT_CLIENT_SECRET"),
        "redirect_uri": os.getenv("HUBSPOT_REDIRECT_URI"),
        "refresh_token": refresh_token,
    }
    response = requests.post(f"{os.getenv('HUBSPOT_TOKEN_URL')}", data).json()
    return JSONResponse(
        {
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
        }
    )


@app.get("/contacts")
def get_contacts(request: Request, token: str):
    """Retrieves companies and individuals (i.e. clients, prospects and suppliers) from Hubspot"""
    headers = {
        "Authorization": f"Bearer {token}",
    }
    response = requests.get(
        f"{os.getenv('HUBSPOT_API_URL')}/companies", headers=headers
    )
    contacts = response.json().get("results", [])
    response = requests.get(f"{os.getenv('HUBSPOT_API_URL')}/contacts", headers=headers)
    contacts.extend(response.json().get("results", []))
    return JSONResponse(contacts)
