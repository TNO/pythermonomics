import copy
import logging
from typing import Dict, Optional, Tuple

from numpy import float64
from pandas.core.frame import DataFrame
from pywellgeo.well_data.dc1dwell import Dc1dwell
from pywellgeo.well_data.names_constants import Constants
from pywellgeo.welltrajectory.trajectory import Trajectory

from pythermonomics.config.geothermal_economics_config import GeothermalEconomicsConfig
from pythermonomics.data.base_well_results import BaseWellResults
from pythermonomics.data.simulation_model_results import SimulationModelResults
from pythermonomics.data.well_results import WellResults
from pythermonomics.energy_model.energy_calculator import EnergyCalculator
from pythermonomics.exceptions import (
    EnergyComputationError,
    LcoeComputationError,
    NpvComputationError,
)
from pythermonomics.npv_model.costmodel_well import CostModelWell
from pythermonomics.npv_model.economics_calculator import EconomicsCalculator

logger = logging.getLogger(__name__)


class GeothermalEconomics:
    """
    A class to compute the Net Present Value (NPV) and Levelized Cost of Energy (LCOE) for geothermal projects.

    The class initializes the techno-economic parameters and other settings from the setting file.
    It computes the NPV and LCOE for the geothermal project based on the energy balance and financial metrics.

    after creating an instance of the class, the function compute_economics() can be called to compute the NPV and LCOE.

    """

    def __init__(
        self,
        economics_config: GeothermalEconomicsConfig,
        simresults: Optional[BaseWellResults] = None,
        welltrajectory: Optional[Trajectory] = None,
        costmodel: Optional[CostModelWell] = None,
        verbose: Optional[bool] = False,
    ) -> None:
        """
        Initializes the techno-economic parameters and other settings from the setting file.

        Parameters
        ----------
        economics_config : GeothermalEconomicsConfig
            Configuration file for running geothermal economics (npv, lcoe, etc.)
        simresults : BaseWellResults, optional
            Parsed results from either flow simulation of semi-analytical equations
        welltrajectory : sTrajectorytr, optional
            Well trajectory object containing each well in the system used for calculating energy and npv
        costmodel : CostModelWell, optional
            Costmodel used to calculate the cost of each well (default is CostModelWell)
        verbose : bool, optional
            Determines the amount of logging to the console (True means debugging info).
        """
        try:
            self.economics_config = economics_config
            self.simresults = simresults
            self.welltrajectory = welltrajectory

            if costmodel is None:
                self.wellcostmodel = CostModelWell(self)
            else:
                self.wellcostmodel = costmodel

            self.verbose = verbose
            self.energy_calculator = EnergyCalculator(self)
            self.economics_calculator = EconomicsCalculator(self)
        except (KeyError, AttributeError, FileNotFoundError, ValueError) as e:
            logger.error("Error initializing GeothermalEconomics", exc_info=True)
            raise LcoeComputationError(
                f"Error initializing GeothermalEconomics: {e}"
            ) from e

    @classmethod
    def from_trajectory(
        cls, settingfile: str, trajectoryfile: str
    ) -> "GeothermalEconomics":
        """
        creates an instance of the geothermal_economics class from a settingsfile and dc1dwell object
        :param settingfile: path to the setting file
        :param trajectoryfile: path to the well trajectory file (default is None).
        :return: instance of the geothermal_economics class
        """
        try:
            economics_config = cls._load_config(settingfile)
            simresults = cls._create_simresults(economics_config)
            welltrajectory = cls._create_trajectory(
                trajectoryfile, economics_config, simresults
            )
            return cls(
                economics_config=economics_config,
                simresults=simresults,
                welltrajectory=welltrajectory,
            )
        except (KeyError, AttributeError, FileNotFoundError, ValueError) as e:
            logger.error(
                "Error initializing GeothermalEconomics from well trajectory file",
                exc_info=True,
            )
            raise LcoeComputationError(
                f"Error initializing GeothermalEconomics from well trajectory file: {e}"
            ) from e

    @classmethod
    def from_config_only(cls, settingfile: str) -> "GeothermalEconomics":
        """
        creates an instance of the geothermal_economics class from a settingsfile
        :param settingfile: path to the setting file
        :return: instance of the geothermal_economics class
        """
        try:
            economics_config = cls._load_config(settingfile)
            simresults = cls._create_simresults(economics_config)
            welltrajectory = cls._create_trajectory(None, economics_config, simresults)
            return cls(
                economics_config=economics_config,
                simresults=simresults,
                welltrajectory=welltrajectory,
            )
        except (KeyError, AttributeError, FileNotFoundError, ValueError) as e:
            logger.error(
                "Error initializing GeothermalEconomics from well trajectory file",
                exc_info=True,
            )
            raise LcoeComputationError(
                f"Error initializing GeothermalEconomics from well trajectory file: {e}"
            ) from e

    @classmethod
    def from_summary_deviation_file(
        cls,
        settingfile: str,
        summary_file: str,
        deviation_files_dir: str,
    ) -> "GeothermalEconomics":
        """
        creates an instance of the geothermal_economics class from a settingsfile and deviation file
        :param settingfile: path to the setting file
        :param summary_file: path to the simulation (summary) data in csv format
        :param deviation_files_dir: path to the directory containing all the deviation files of the wells
        :return: instance of the geothermal_economics class
        """
        try:
            economics_config = cls._load_config(settingfile)
            simresults = SimulationModelResults(
                summary_file=summary_file,
                path_deviation_files=deviation_files_dir,
            )
            welltrajectory = cls._create_trajectory(None, economics_config, simresults)
            return cls(
                economics_config=economics_config,
                simresults=simresults,
                welltrajectory=welltrajectory,
            )
        except (KeyError, AttributeError, FileNotFoundError, ValueError) as e:
            logger.error(
                "Error initializing GeothermalEconomics from summary and deviation file",
                exc_info=True,
            )
            raise LcoeComputationError(
                f"Error initializing GeothermalEconomics from summary and deviation file: {e}"
            ) from e

    @classmethod
    def from_dc1d(
        cls, settingfile: str, trajectoryfile: str, dc1dwell: Dc1dwell
    ) -> "GeothermalEconomics":
        """
        creates an instance of the geothermal_economics class from a settingsfile and dc1dwell object
        :param settingfile: path to the setting file
        :param trajectoryfile: path to the well trajectory file (default is None).
        :param dc1dwell: dc1dwell config file
        :return: instance of the geothermal_economics class
        """
        try:
            economics_config = cls._load_config(settingfile)
            economics_config.reservoir_parameters.injection_temperature = dc1dwell.temp[
                0
            ]
            economics_config.reservoir_parameters.salinity = dc1dwell.salinity[0]
            economics_config.energy_loss_parameters.well_tubing = (
                dc1dwell.rw[0] * Constants.SI_INCH * 2
            )  # convert
            economics_config.energy_loss_parameters.well_roughness = dc1dwell.roughness
            economics_config.reservoir_parameters.production_temperature = (
                dc1dwell.temp[1]
            )
            economics_config.reservoir_parameters.injection_BHP = dc1dwell.dpres + 200
            economics_config.reservoir_parameters.production_BHP = 200
            economics_config.reservoir_parameters.flowrate = dc1dwell.qvol * 3600

            simresults = cls._create_simresults(economics_config)
            welltrajectory = cls._create_trajectory(
                trajectoryfile, economics_config, simresults, dc1dwell
            )
            return cls(
                economics_config=economics_config,
                simresults=simresults,
                welltrajectory=welltrajectory,
            )
        except (KeyError, AttributeError, FileNotFoundError, ValueError) as e:
            logger.error(
                "Error initializing GeothermalEconomics from dc1d", exc_info=True
            )
            raise LcoeComputationError(
                f"Error initializing GeothermalEconomics from dc1d: {e}"
            ) from e

    @classmethod
    def copy(self):
        try:
            return copy.deepcopy(self)
        except Exception as e:
            logger.error("Error copying GeothermalEconomics instance", exc_info=True)
            raise LcoeComputationError(
                f"Error copying GeothermalEconomics instance: {e}"
            ) from e

    def compute_economics(
        self,
    ) -> Tuple[float64, float64, DataFrame, DataFrame, Dict[str, str], DataFrame]:
        try:
            return self.economics_calculator.compute_economics()
        except NpvComputationError as e:
            logger.error("Error computing NPV", exc_info=True)
            raise NpvComputationError(f"Error computing NPV: {e}") from e
        except Exception as e:
            logger.error("Unexpected error in compute_economics", exc_info=True)
            raise LcoeComputationError(
                f"Unexpected error in compute_economics: {e}"
            ) from e

    def compute_energy(self, cashflow):
        try:
            return self.energy_calculator.compute_energy(cashflow)
        except EnergyComputationError as e:
            logger.error("Error computing energy", exc_info=True)
            raise EnergyComputationError(f"Error computing energy: {e}") from e
        except Exception as e:
            logger.error("Unexpected error in compute_energy", exc_info=True)
            raise LcoeComputationError(
                f"Unexpected error in compute_energy: {e}"
            ) from e

    @staticmethod
    def _load_config(settingfile: str) -> GeothermalEconomicsConfig:
        return GeothermalEconomicsConfig.load_from_file(settingfile)

    @staticmethod
    def _create_simresults(economics_config: GeothermalEconomicsConfig) -> WellResults:
        return WellResults(
            well_trajectories=economics_config.well_trajectories,
            reservoir_parameters=economics_config.reservoir_parameters,
            parameters=economics_config.techno_eco_param,
            nyear=economics_config.techno_eco_param.lifecycle_years,
        )

    @staticmethod
    def _create_trajectory(
        trajectoryfile: Optional[str],
        economics_config: GeothermalEconomicsConfig,
        simresults: WellResults,
        dc1dwell: Optional[Dc1dwell] = None,
    ) -> Trajectory:
        return Trajectory(
            trajectoryfile=trajectoryfile,
            options=economics_config,
            simresults=simresults,
            trajectoryinstance=dc1dwell,
        )
