import logging

from modules import sqlmodel_utils, strava_api


def main():
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


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
