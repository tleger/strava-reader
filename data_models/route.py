from sqlmodel import Field, SQLModel


class Route(SQLModel, table=True):
    """
    Model for strava routes.
    """

    athlete_id: int
    description: str = Field(nullable=True)
    distance: float
    elevation_gain: float
    id: int = Field(primary_key=True, nullable=False)
    id_str: str
    map_id: str
    map_polyline: str
    name: str
    private: bool
    resource_state: int
    starred: bool
    sub_type: int
    created_at: str
    updated_at: str
    timestamp: int
    type: int
    estimated_moving_time: int
    waypoints: str
    segments: str

    def __init__(self, **data):
        super().__init__(**data)
        if "id" not in data:
            raise ValueError("Field 'id' is required")
