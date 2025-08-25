import logging
from typing import Dict

import yaml
from pydantic import BaseModel, Field

from pythermonomics.config.energy_loss_parameters import EnergyLossParameters
from pythermonomics.config.reservoir_simulation_parameters import (
    ReservoirSimulationParameters,
)
from pythermonomics.config.techno_economic_config import TechnoEconomicParameters
from pythermonomics.config.well_trajectories_config import WellTrajectory

logger = logging.getLogger(__name__)


class GeothermalEconomicsConfig(BaseModel):
    """
    Configuration class for geothermal NPV calculations.
    This class loads settings from a YAML file and provides access to the parameters
    required for NPV and LCOE computations.
    """

    techno_eco_param: TechnoEconomicParameters = Field(
        ...,
        description="General cost parameters (CAPEX/OPEX, heat prices, etc.) for the geothermal system",
        alias="techno_economic_parameters",
    )
    reservoir_parameters: ReservoirSimulationParameters | None = Field(
        default=None,
        description="reservoir specific input",
        alias="reservoir_simulation_parameters",
    )
    energy_loss_parameters: EnergyLossParameters | None = Field(
        default=None,
        description="Energy loss specific parameters",
        alias="energy_loss_parameters",
    )
    well_trajectories: Dict[str, WellTrajectory] | None = Field(
        default=None, description="Dictionary of well trajectories keyed by well name"
    )

    @classmethod
    def load_from_file(cls, config_file: str) -> "GeothermalEconomicsConfig":
        with open(config_file, "r") as f:
            settings = yaml.safe_load(f)
        return cls(**settings)
