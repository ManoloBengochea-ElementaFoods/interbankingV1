import requests
import streamlit as st

TOKEN_URL = "https://auth.interbanking.com.ar/cas/oidc/accessToken"
SCOPE = "info-financiera"


@st.cache_data(ttl=7200)
def _pedir_token(client_id, client_secret, url_servicio):
    r = requests.post(
        f"{TOKEN_URL}?scope={SCOPE}",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "service": url_servicio
        },
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        },
        timeout=30,
    )

    if not r.ok:
        raise Exception(f"Error token: {r.text}")

    return r.json()["access_token"]


def obtener_token(secrets):
    return _pedir_token(
        secrets["client_id"],
        secrets["client_secret"],
        secrets["url_servicio"],
    )