import logging
from typing import TYPE_CHECKING, Tuple

import numpy as np
import pandas as pd
import pywellgeo.well_data.water_properties as waterprop
from pywellgeo.well_data.names_constants import Constants

from pythermonomics.exceptions import EnergyComputationError

if TYPE_CHECKING:
    from pythermonomics.geothermal_economics import GeothermalEconomics


logger = logging.getLogger(__name__)


class EnergyCalculator:
    """
    A class to compute energy production and injection characteristics for geothermal wells.
    It processes well results and computes energy terms based on well states and production characteristics.
    """

    def __init__(self, economics_instance: "GeothermalEconomics") -> None:
        self.economics = economics_instance
        self.economics_config = self.economics.economics_config

    def compute_energy(self, cashflow: pd.DataFrame) -> Tuple[pd.DataFrame, int, int]:
        """
        Computes energy production and injection characteristics for geothermal wells.
        :param cashflow: DataFrame containing cash flow data with well results.
        :return: Tuple containing the updated cashflow DataFrame, number of production wells, and
                    number of injection wells.
        """
        if not isinstance(cashflow, pd.DataFrame):
            raise TypeError("cashflow must be a pandas DataFrame")

        try:
            wellRes = self.economics.simresults.wellRes
            if not isinstance(wellRes, pd.DataFrame):
                raise TypeError("cashflow must be a pandas DataFrame")

            wells_and_states = self.economics.simresults.wells_and_states
            if not isinstance(wells_and_states, dict):
                raise TypeError("wells_and_states must be a dictionary")
        except AttributeError as e:
            logger.error(
                "Missing simulation results in GeothermalEconomics instance",
                exc_info=True,
            )
            raise EnergyComputationError(
                "Missing simulation results in GeothermalEconomics instance."
            ) from e

        self._assign_time_columns(cashflow, wellRes)
        cashflow["injTemp"] = (
            self.economics_config.reservoir_parameters.injection_temperature
        )

        nwp, nwi, Qvols, templist = self._process_wells(
            cashflow, wellRes, wells_and_states
        )
        cashflow["avgInjP"] = self._compute_avg_injP(
            wellRes, wells_and_states, np.zeros(len(wellRes["DAYS"])), nwi
        )
        self._apply_friction_and_heatloss(Qvols, templist, wells_and_states, cashflow)
        enTm, enPr, enIn = self._compute_energy_terms(
            cashflow, wellRes, wells_and_states, templist
        )

        cashflow["enTemp"] = enTm
        cashflow["enProd"] = enPr
        cashflow["enInj"] = enIn

        self._compute_and_store_cop(cashflow)
        return cashflow, nwp, nwi

    def _assign_time_columns(
        self, cashflow: pd.DataFrame, wellRes: pd.DataFrame
    ) -> None:
        try:
            cashflow["time"] = wellRes["DAYS"]
            cashflow["year"] = wellRes["YEARS"]
            # Avoid chained assignment
            cashflow.loc[1:, "dTime"] = [
                x - y for x, y in zip(cashflow["time"].iloc[1:], cashflow["time"])
            ]
            cashflow.loc[0, "dTime"] = cashflow["time"].iloc[0]
        except KeyError as e:
            logger.error(
                "Missing expected columns in wellRes or parameters", exc_info=True
            )
            raise EnergyComputationError(
                f"Missing expected columns in wellRes or parameters: {e}"
            ) from e

    def _process_wells(
        self,
        cashflow: pd.DataFrame,
        wellRes: pd.DataFrame,
        wells_and_states: dict,
    ) -> Tuple[int, int, int, np.ndarray, list]:
        nwp: int = 0
        nwi: int = 0
        Qvols = None
        templist = []

        try:
            for w in wells_and_states.keys():
                templist.append(wellRes[("T:%s" % w)])

            for w in wells_and_states.keys():
                cashflow[f"temp_{w}"] = wellRes[f"T:{w}"]
                if wells_and_states[w] == "prod":
                    cashflow[f"wpcum_{w}"] = wellRes[f"WWPT:{w}"]
                    qf = [
                        x - y
                        for x, y in zip(
                            wellRes[f"WWPT:{w}"].iloc[1:], wellRes[f"WWPT:{w}"]
                        )
                    ]
                    qf.insert(0, wellRes[f"WWPT:{w}"].iloc[0])
                    qf = np.asarray(qf)
                    qf = (
                        qf
                        * self.economics_config.techno_eco_param.loadhours
                        / (24 * 365.25)
                    )
                    cashflow[f"wprod_{w}"] = qf
                    Qvols = cashflow[f"wprod_{w}"] / (
                        self.economics_config.techno_eco_param.loadhours * 3600
                    )
                    cashflow[f"wpRate_{w}"] = cashflow[f"wprod_{w}"] / cashflow["dTime"]
                    if not sum(wellRes[f"T:{w}"]) == 0.0:
                        cashflow[f"dTemp_{w}"] = wellRes[f"T:{w}"] - cashflow["injTemp"]
                    else:
                        cashflow[f"dTemp_{w}"] = 0.0
                    nwp += 1
                elif wells_and_states[w] == "inj":
                    cashflow[f"wicum_{w}"] = wellRes[f"WWIT:{w}"]
                    qf = [
                        x - y
                        for x, y in zip(
                            wellRes[f"WWIT:{w}"].iloc[1:], wellRes[f"WWIT:{w}"]
                        )
                    ]
                    qf.insert(0, wellRes[f"WWIT:{w}"].iloc[0])
                    qf = np.asarray(qf)
                    qf = (
                        qf
                        * self.economics_config.techno_eco_param.loadhours
                        / (24 * 365.25)
                    )
                    cashflow[f"winj_{w}"] = qf
                    cashflow[f"wiRate_{w}"] = cashflow[f"winj_{w}"] / cashflow["dTime"]
                    nwi += 1
        except KeyError as e:
            logger.error("Error processing wells: missing column", exc_info=True)
            raise EnergyComputationError(
                f"Error processing wells: missing column {e}"
            ) from e
        except ZeroDivisionError as e:
            logger.error("Division by zero while processing the wells", exc_info=True)
            raise EnergyComputationError(
                f"Division by zero while processing the wells: {e}"
            ) from e
        except Exception as e:
            logger.error("Unexpected error in _process_wells", exc_info=True)
            raise EnergyComputationError(
                f"Unexpected error in _process_wells: {e}"
            ) from e
        return nwp, nwi, Qvols, templist

    def _compute_avg_injP(
        self,
        wellRes: pd.DataFrame,
        wells_and_states: dict,
        injP: np.ndarray,
        nwi: int,
    ) -> np.ndarray:
        try:
            for w in wells_and_states.keys():
                if wells_and_states[w] == "inj":
                    injP = injP + wellRes[f"WBHP:{w}"]
            if nwi > 0:
                injP = injP / nwi
        except KeyError as e:
            logger.error("Error computing average injection pressure", exc_info=True)
            raise EnergyComputationError(
                f"Error computing average injection pressure: {e}"
            ) from e
        return injP

    def _apply_friction_and_heatloss(
        self,
        Qvols: np.ndarray,
        templist: list,
        wells_and_states: dict,
        cashflow: pd.DataFrame,
    ) -> None:
        tubedia = self.economics_config.energy_loss_parameters.well_tubing
        tuberough = self.economics_config.energy_loss_parameters.well_roughness
        salinity = self.economics_config.reservoir_parameters.salinity

        try:
            self.economics.welltrajectory.trajectoryinput.friction_all(
                Qvols, templist, salinity, tubedia, tuberough, wells_and_states
            )

            if self.economics_config.energy_loss_parameters.useheatloss:
                temploss = self.economics.welltrajectory.trajectoryinput.temploss_all(
                    Qvols, templist, salinity, wells_and_states, wellradius=tubedia*0.0254*0.5
                )
                for i, w in enumerate(wells_and_states.keys()):
                    if wells_and_states[w] == "prod":
                        cashflow[f"dTemp_{w}"] = cashflow[f"dTemp_{w}"] - temploss[i]
        except Exception as e:
            logger.error("Error applying friction/heat loss", exc_info=True)
            raise EnergyComputationError(
                f"Error applying friction/heat loss: {e}"
            ) from e

    def _compute_energy_terms(
        self,
        cashflow: pd.DataFrame,
        wellRes: pd.DataFrame,
        wells_and_states: dict,
        templist: list,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        enTm = np.zeros((len(wellRes["DAYS"])))
        enPr = np.zeros((len(wellRes["DAYS"])))
        enIn = np.zeros((len(wellRes["DAYS"])))
        try:
            for i, w in enumerate(wells_and_states.keys()):
                if wells_and_states[w] == "prod":
                    bhp = wellRes[f"WBHP:{w}"] * 1.0
                    temp = templist[i]
                    rhow = waterprop.density(
                        bhp * 1e5,
                        temp,
                        self.economics_config.reservoir_parameters.salinity * 1e-6,
                    )
                    cpw = waterprop.heatcapacity(
                        temp, self.economics_config.reservoir_parameters.salinity * 1e-6
                    )
                    Qvol = cashflow[f"wprod_{w}"]
                    dTemp = cashflow[f"dTemp_{w}"]
                    cashflow[f"enTemp_{w}"] = Qvol * rhow * cpw * dTemp * 1e-9  # GJ
                    enTm = enTm + cashflow[f"enTemp_{w}"]
                    dP = wellRes["FPR"] - wellRes[f"WBHP:{w}"]
                    dP = (
                        dP
                        + self.economics.welltrajectory.trajectoryinput.dp_frictionprod
                        + self.economics.welltrajectory.trajectoryinput.dpSyphon
                    )
                    cashflow[f"enProd_{w}"] = (Qvol * dP * 1e2 / 3600) / (
                        self.economics_config.techno_eco_param.pump_efficiency
                        * Constants.GJ2kWh
                    )  # kWh --> GJ
                    cashflow[f"dP_{w}"] = dP
                    enPr = enPr + cashflow[f"enProd_{w}"]
                elif wells_and_states[w] == "inj":
                    dP = wellRes[f"WBHP:{w}"] - wellRes["FPR"]
                    Qvol = cashflow[f"winj_{w}"]
                    dP = (
                        dP
                        + self.economics.welltrajectory.trajectoryinput.dp_frictioninj
                    )
                    cashflow[f"enInj_{w}"] = (Qvol * dP * 1e2 / 3600) / (
                        self.economics_config.techno_eco_param.pump_efficiency
                        * Constants.GJ2kWh
                    )
                    cashflow[f"dP_{w}"] = dP
                    enIn = enIn + cashflow[f"enInj_{w}"]
        except KeyError as e:
            logger.error("Error computing energy terms: missing column", exc_info=True)
            raise EnergyComputationError(
                f"Error computing energy terms: missing column {e}"
            ) from e
        except Exception as e:
            logger.error("Unexpected error in _compute_energy_terms", exc_info=True)
            raise EnergyComputationError(
                f"Unexpected error in _compute_energy_terms: {e}"
            ) from e
        return enTm, enPr, enIn

    def _compute_and_store_cop(self, cashflow: pd.DataFrame) -> None:
        try:
            cashflow["enPower[MW]"] = (
                cashflow["enTemp"]
                * Constants.GJ2kWh
                / self.economics_config.techno_eco_param.loadhours
                * 1e-3
            )
            cashflow["enPowercons[MW]"] = (
                (cashflow["enProd"] + cashflow["enInj"])
                * Constants.GJ2kWh
                / self.economics_config.techno_eco_param.loadhours
                * 1e-3
            )
            cashflow["COP"] = cashflow["enPower[MW]"] / cashflow["enPowercons[MW]"]
        except ZeroDivisionError:
            logger.error("Division by zero while computing COP", exc_info=True)
            raise EnergyComputationError("Division by zero while computing COP")
        except Exception as e:
            logger.error("Error assigning final energy columns", exc_info=True)
            raise EnergyComputationError(
                f"Error assigning final energy columns: {e}"
            ) from e
        return
