from typing import Dict, Tuple

import numpy as np
import pandas as pd

from pythermonomics.config.reservoir_simulation_parameters import (
    ReservoirSimulationParameters,
)
from pythermonomics.config.techno_economic_config import TechnoEconomicParameters
from pythermonomics.config.well_trajectories_config import WellTrajectory
from pythermonomics.data.base_well_results import BaseWellResults


class WellResults(BaseWellResults):
    """
    Reads simulated well paths and production characteristics over time
    from provided configuration data.
    """

    def __init__(
        self,
        well_trajectories: Dict[str, WellTrajectory],
        reservoir_parameters: ReservoirSimulationParameters,
        parameters: TechnoEconomicParameters,
        nyear: int,
    ) -> None:
        """
        :param wells: Dictionary of well names and their properties.
        :param reservoir_parameters: Reservoir parameters including well coordinates.
        :param parameters: Parameters for the simulation.
        :param nyear: Number of years for the simulation.
        """
        super().__init__()
        if not well_trajectories or len(well_trajectories) < 2:
            raise ValueError("At least two wells must be provided.")
        if nyear < 1:
            raise ValueError("nyear must be >= 1.")
        self.well_trajectories = well_trajectories
        self.res_params = reservoir_parameters
        self.techno_eco_params = parameters
        self.nyear = nyear

        (
            self.wellRes,
            self.wells_and_states,
            self.WXYZ,
        ) = self.read_wellpaths_production()
        self.wellRes = self.wellRes.reset_index(drop=True)

    def read_wellpaths_production(
        self,
    ) -> Tuple[pd.DataFrame, Dict[str, str], Dict[str, np.ndarray]]:
        """
        Reads well paths and production characteristics from the configuration data.
        Returns a DataFrame with well results, a dictionary of well states, and a dictionary of
        well coordinates.
        """
        WXYZ, wells_and_states = self.read_well_path_and_types()
        summ_days = np.arange(self.nyear + 1) * 365.0

        wellRes = pd.DataFrame(np.nan, np.arange(len(summ_days)), columns=["DAYS"])
        wellRes["DAYS"] = summ_days
        wellRes["YEARS"] = wellRes["DAYS"] / 365.0
        wellRes = wellRes[wellRes["YEARS"] >= 1.0]
        qyear = self.res_params.flowrate * 24 * 365

        for w, state in wells_and_states.items():
            if w not in self.well_trajectories:
                raise KeyError(f"Missing coordinates for well {w}")
            if state == "prod":
                temp = self.res_params.production_temperature
                swq = "WWPT:%s"
                bhp = self.res_params.production_BHP
            else:
                temp = self.res_params.injection_temperature
                swq = "WWIT:%s"
                bhp = self.res_params.injection_BHP
            for ind_day in wellRes.index:
                wellRes.loc[ind_day, f"T:{w}"] = temp
                wellRes.loc[ind_day, swq % w] = ind_day * qyear
                wellRes.loc[ind_day, f"WBHP:{w}"] = bhp
                wellRes.loc[ind_day, "FPR"] = 0.5 * (
                    self.res_params.injection_BHP + self.res_params.production_BHP
                )
        return wellRes, wells_and_states, WXYZ

    def read_well_path_and_types(
        self,
    ) -> Tuple[Dict[str, np.ndarray], Dict[str, str]]:
        """
        Reads well coordinates and types from the reservoir parameters.
        Returns a dictionary of well coordinates and a dictionary of well states.
        """
        wkeys = list(self.well_trajectories.keys())
        if len(wkeys) < 2:
            raise ValueError("At least two wells must be provided.")
        wells_and_states: Dict[str, str] = {wkeys[0]: "inj", wkeys[1]: "prod"}

        WXYZ: Dict[str, np.ndarray] = {}
        for w in wells_and_states:
            if w not in self.well_trajectories:
                raise KeyError(f"Missing coordinates for well {w}")
            well_trajectory = np.array(
                [
                    self.well_trajectories[w].platform,
                    self.well_trajectories[w].kick_off,
                    self.well_trajectories[w].targets[0],
                    self.well_trajectories[w].targets[1],
                ],
                dtype="float",
            )
            WXYZ[w] = well_trajectory
        return WXYZ, wells_and_states
