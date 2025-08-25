from pydantic import BaseModel, Field


class ReservoirSimulationParameters(BaseModel):
    """
    Reservoir simulation config class
    """

    injection_temperature: float = Field(
        ..., description="Injection temperature in degrees Celsius"
    )
    salinity: float = Field(
        ...,
        description="Salinity in parts per million (ppm), used to determine brine heat capacity",
    )
    production_temperature: float | None = Field(
        default=None, description="Production temperature in degrees Celsius"
    )
    injection_BHP: float | None = Field(
        default=None,
        description="Bottom-hole pressure at reservoir level for injection in bar",
    )
    production_BHP: float | None = Field(
        default=None,
        description="Bottom-hole pressure at reservoir level for production in bar",
    )
    flowrate: float | None = Field(
        default=None, description="Flowrate in cubic meters per hour (m³/h)"
    )
