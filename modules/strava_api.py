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
        response = httpx.post(auth_endpoint, data=payload)
        response.raise_for_status()
        return response.json()["access_token"]
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to get access token: {e}")
        raise


def get_authenticated_athlete(access_token: str) -> dict:
    """Fetch the authenticated athlete from Strava."""
    athlete_endpoint = "https://www.strava.com/api/v3/athlete"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        res = httpx.get(athlete_endpoint, headers=headers)
        res.raise_for_status()
        return res.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to fetch authenticated athlete: {e}")
        raise


def fetch_data(
    endpoint: str, headers: dict[str, str], params: dict[str, int]
) -> list[dict]:
    """Fetch paginated data from a given endpoint."""
    page = 1
    results = []

    while True:
        logging.info(f"Fetching page {page}")
        try:
            response = httpx.get(
                endpoint, headers=headers, params={**params, "page": page}, timeout=60
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
            logging.error(f"Failed to fetch data: {e}")
            break

    return results


def fetch_activities(access_token: str) -> list[dict]:
    """Fetch all activities from Strava."""
    activities_endpoint = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    return fetch_data(activities_endpoint, headers, {"per_page": 200})


def fetch_athlete_routes(access_token: str) -> list[dict]:
    """Fetch all athlete's routes from Strava."""
    athlete = get_authenticated_athlete(access_token)
    athlete_routes_endpoint = (
        f"https://www.strava.com/api/v3/athletes/{athlete['id']}/routes"
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    routes = fetch_data(athlete_routes_endpoint, headers, {"per_page": 200})

    routes_detail_endpoint = "https://www.strava.com/api/v3/routes/"
    detailed_routes = []
    for route in routes:
        route_id = route["id"]
        try:
            route_detail_response = httpx.get(
                f"{routes_detail_endpoint}{route_id}", headers=headers, timeout=60
            )
            route_detail_response.raise_for_status()
            detailed_routes.append(route_detail_response.json())
        except httpx.RequestError as e:
            logging.error(f"An error occurred while requesting route details: {e}")
        except httpx.HTTPStatusError as e:
            logging.error(f"Failed to fetch route details: {e}")

    return detailed_routes
