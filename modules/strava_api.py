import logging
import os

from dotenv import load_dotenv
import httpx

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# load environment variables from .env file
load_dotenv(".env")

# retrieve secrets from environment variables
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")


def get_access_token() -> str:
    """Fetch a new access token using the refresh token."""
    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "refresh_token": STRAVA_REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    auth_endpoint = "https://www.strava.com/oauth/token"
    try:
        res = httpx.post(auth_endpoint, data=payload)
        res.raise_for_status()
        return res.json()["access_token"]
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to get access token: {e}")
        raise


def fetch_activities(access_token: str) -> list[dict]:
    """Fetch all activities from Strava."""
    activities_endpoint = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    page = 1
    results = []

    while True:
        logging.info(f"Fetching page {page}")
        try:
            response = httpx.get(
                activities_endpoint,
                headers=headers,
                params={"per_page": 200, "page": page},
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()

            if not data:
                break  # No more data to fetch

            results.extend(data)
            page += 1

        except httpx.RequestError as e:
            logging.error(f"An error occurred while requesting data: {e}")
            break
        except httpx.HTTPStatusError as e:
            logging.error(f"Failed to fetch activities: {e}")
            break

    return results
