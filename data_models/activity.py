from sqlmodel import Field, SQLModel


class Activity(SQLModel):
    """
    Model for strava activities. Unused fields are left in (but commented out) for future reference.
    """

    # resource_state: int
    # athlete_id: int
    # athlete_resource_state: int
    name: str
    distance: float
    moving_time: float
    elapsed_time: float
    total_elevation_gain: float
    type: str
    # sport_type: str
    # workout_type: str
    id: int = Field(primary_key=True, nullable=False)
    start_date: str
    start_date_local: str
    timezone: str
    # utc_offset: float
    # location_city: str
    # location_state: str
    # location_country: str
    # achievement_count: float
    # kudos_count: float
    # comment_count: float
    # athlete_count: float
    # photo_count: float
    # map_id: str
    # map_summary_polyline: str
    # map_resource_state: str
    # trainer: str
    # commute: bool
    # manual: bool
    # private: bool
    # visibility: str
    # flagged: bool
    # gear_id: str
    # start_latlng: list
    # end_latlng: list
    # average_speed: float
    # max_speed: float
    # average_watts: float
    # kilojoules: float
    # device_watts: bool
    # has_heartrate: bool
    # average_heartrate: float
    # max_heartrate: float
    # heartrate_opt_out: bool
    # display_hide_heartrate_option: bool
    # elev_high: float
    # elev_low: float
    # upload_id: str
    # upload_id_str: str
    # external_id: str
    # from_accepted_tag: bool
    # pr_count: float
    # total_photo_count: float
    # has_kudoed: bool
    # suffer_score: float
