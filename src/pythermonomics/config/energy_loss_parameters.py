from pydantic import BaseModel, Field


class EnergyLossParameters(BaseModel):
    """
    Energy loss related config class
    """

    well_roughness: float = Field(..., description="Well roughness in milli-inch")
    well_tubing: float = Field(..., description="Production tubing diameter in inches")
    useheatloss: bool | None = Field(
        default=False, description="Flag to enable or disable heat loss calculations"
    )
    tsurface: float | None = Field(
        default=None, description="Surface temperature in degrees Celsius"
    )
    tgrad: float | None = Field(
        default=None, description="Geothermal gradient in degrees Celsius per meter"
    )
