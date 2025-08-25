from typing import List

from pydantic import BaseModel, Field


class WellTrajectory(BaseModel):
    """Configuration for well trajectories in geothermal economics."""

    platform: List[float] = Field(
        ..., description="Coordinates of the platform [x, y, z]"
    )
    kick_off: List[float] = Field(..., description="Kick-off point [x, y, z]")
    targets: List[List[float]] = Field(
        ...,
        description="List of target coordinates [[x, y, z], ...], e.g., top and bottom reservoir",
    )
