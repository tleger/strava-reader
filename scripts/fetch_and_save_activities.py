import logging

from modules import sqlmodel_utils, strava_api


def main():
    """
    Main function to fetch activities from the Strava API and save them to the database.

    This function:
    1. Retrieves an access token from the Strava API.
    2. Fetches activities using the access token.
    3. Saves the fetched activities to the database.
    4. Logs the success or failure of the operation.
    """
    try:
        access_token = strava_api.get_access_token()
        activities = strava_api.fetch_activities(access_token)
        if activities:
            sqlmodel_utils.save_activities_to_db(activities)
            logging.info(
                f"Successfully saved {len(activities)} activities to the database"
            )
        else:
            logging.info("No activities were found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
