import logging
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Tuple

import numpy as np
import numpy_financial as npf
import pandas as pd
from numpy import float64
from pandas.core.frame import DataFrame
from pywellgeo.well_data.names_constants import Constants

from pythermonomics.exceptions import NpvComputationError
from pythermonomics.npv_model.unit_maps import UNIT_MAP, WELL_PREFIX_UNIT

if TYPE_CHECKING:
    from pythermonomics.geothermal_economics import GeothermalEconomics

logger = logging.getLogger(__name__)


class EconomicsCalculator:
    """
    A class to compute the Net Present Value (NPV) and Levelized Cost of Energy (LCOE) for geothermal projects.
    The class initializes the techno-economic parameters and other settings from the setting file.
    It computes the NPV and LCOE for the geothermal project based on the energy balance and financial metrics.
    """

    def __init__(self, economics_instance: "GeothermalEconomics") -> None:
        """
        Initializes the techno-economic parameters and other settings from the setting file.
        :param economics_instance: An instance of GeothermalEconomics containing parameters for NPV and LCOE calculations.
        """
        self.economics = economics_instance
        self.param = self.economics.economics_config.techno_eco_param

    def compute_economics(
        self,
    ) -> Tuple[float64, float64, DataFrame, DataFrame, Dict[str, str], DataFrame]:
        """
        Computes the Net Present Value (NPV) and Levelized Cost of Energy (LCOE) for the geothermal project.
        :return: A tuple containing the NPV, LCOE, cashflow DataFrame, well results DataFrame, and well states dictionary.
        """
        cashflow, capex, opex = self._init_dataframes(self.economics.simresults.wellRes)
        cashflow, nwp, nwi = self.economics.energy_calculator.compute_energy(cashflow)
        installedkW = self._get_installed_kw(cashflow)
        capextotal = self._calculate_capex(capex, cashflow, installedkW, nwi)
        self._calculate_opex(opex, cashflow, installedkW, nwp)
        equity, loan = self._calculate_equity_loan(capextotal)
        cashflow = self._calculate_income(cashflow)
        cashflow = self._calculate_costs(cashflow, capextotal, equity, loan)
        lcoe = self._calculate_lcoe(cashflow, equity)
        npv = cashflow["npv"].values[-1]
        self._set_lcoe_attributes(cashflow)
        _set_units_attrs(cashflow)
        well_names = list(self.economics.simresults.wells_and_states.keys())
        cashflow = _add_units_and_rename(
            cashflow,
            well_tokens=well_names,
            unit_map_exact=UNIT_MAP,
            well_prefix_unit=WELL_PREFIX_UNIT,
            prefer_series_attrs=True,
            mode="replace",
            inplace=False,
        )
        cashflow, well_results = _split_dataframe(cashflow, well_names)
        return (
            npv,
            lcoe,
            cashflow,
            self.economics.simresults.wellRes,
            self.economics.simresults.wells_and_states,
            well_results,
        )

    def _init_dataframes(
        self, wellRes: DataFrame
    ) -> Tuple[DataFrame, DataFrame, DataFrame]:
        try:
            cashflow = pd.DataFrame(
                0.0, np.arange(len(wellRes)), columns=["time", "year", "dTime"]
            )
            capex = pd.DataFrame(
                0.0,
                np.arange(len(wellRes)),
                columns=[
                    "year",
                    "wells",
                    "pumps",
                    "separator",
                    "contigency",
                    "insurance",
                    "total",
                    "cumulative",
                ],
            )
            opex = pd.DataFrame(
                0.0,
                np.arange(len(wellRes)),
                columns=["year", "fixed", "variable", "total"],
            )
            capex["year"] = wellRes["YEARS"]
            opex["year"] = wellRes["YEARS"]
            return cashflow, capex, opex
        except KeyError as e:
            logger.error(
                "Missing expected columns in wellRes for dataframe initialization",
                exc_info=True,
            )
            raise NpvComputationError(
                f"Missing expected columns in wellRes: {e}"
            ) from e

    def _get_installed_kw(self, cashflow: DataFrame) -> pd.Series:
        try:
            return cashflow["enTemp"] * Constants.GJ2kWh / self.param.loadhours
        except KeyError as e:
            logger.error(
                "Missing 'enTemp' in cashflow for installed kW calculation",
                exc_info=True,
            )
            raise NpvComputationError(f"Missing 'enTemp' in cashflow: {e}") from e

    def _calculate_capex(
        self, capex: DataFrame, cashflow: DataFrame, installedkW: DataFrame, nwi: int
    ) -> Tuple[float]:
        try:
            wellcosts = self.economics.wellcostmodel.compute_costs()
            capexother = (
                self.param.CAPEX_base + self.param.CAPEX_variable * installedkW.iloc[0]
            )
            capex.loc[0, "total"] = (capexother + wellcosts) * (
                1 + self.param.CAPEX_contingency
            ) + nwi * self.param.pump_cost
            cashflow["capex"] = capex["total"]
            cashflow["wellcosts"] = wellcosts
            return capex.loc[0, "total"]
        except (KeyError, AttributeError, IndexError) as e:
            logger.error("Error calculating CAPEX", exc_info=True)
            raise NpvComputationError(f"Error calculating CAPEX: {e}") from e

    def _calculate_opex(
        self, opex: DataFrame, cashflow: DataFrame, installedkW: pd.Series, nwp: int
    ) -> None:
        try:
            inflate = (1 + self.param.inflation_rate) ** cashflow["year"]
            years_pump_change = range(
                self.param.pump_life,
                int(cashflow.index[-1]) + 1,
                self.param.pump_life,
            )
            opex["fixed"] += (
                opex["year"].isin(years_pump_change) * nwp * self.param.pump_cost
            )
            opex["fixed"] += self.param.OPEX_base
            opex["variable"] = (
                installedkW * self.param.OPEX_variable
                + cashflow["enTemp"].iloc[-1]
                * Constants.GJ2kWh
                * 0.01
                * self.param.OPEX_variable_produced
            )
            opex["total"] = (opex["fixed"] + opex["variable"]) * inflate
            cashflow["opex"] = opex["total"]
        except (KeyError, AttributeError, IndexError) as e:
            logger.error("Error calculating OPEX", exc_info=True)
            raise NpvComputationError(f"Error calculating OPEX: {e}") from e

    def _calculate_equity_loan(self, capextotal: float) -> Tuple[float, float]:
        try:
            equity = capextotal * self.param.equity_share
            loan = capextotal - equity
            return equity, loan
        except AttributeError as e:
            logger.error("Error calculating equity/loan", exc_info=True)
            raise NpvComputationError(f"Error calculating equity/loan: {e}") from e

    def _calculate_income(self, cashflow: DataFrame) -> DataFrame:
        try:
            heat_price = np.where(
                cashflow["year"]
                >= self.economics.economics_config.techno_eco_param.subsidy_years + 1.0,
                self.param.heat_price,
                self.param.heat_price_feedin,
            )
            cashflow["income"] = (
                cashflow["enTemp"] * Constants.GJ2kWh * 0.01 * heat_price
            )
            return cashflow
        except (KeyError, AttributeError) as e:
            logger.error("Error calculating income", exc_info=True)
            raise NpvComputationError(f"Error calculating income: {e}") from e

    def _calculate_costs(
        self,
        cashflow: DataFrame,
        capextotal: float,
        equity: float,
        loan: float,
    ) -> DataFrame:
        try:
            cashflow["elecCost"] = (
                (cashflow["enInj"] + cashflow["enProd"])
                * Constants.GJ2kWh
                * 0.01
                * self.param.electricity_price
                * ((1 + self.param.inflation_rate) ** cashflow["year"])
            )
            cashflow["ipmt"] = np.where(
                cashflow["year"] <= self.param.loan_nyear,
                -npf.ipmt(
                    self.param.loan_rate,
                    cashflow["year"],
                    self.param.loan_nyear,
                    loan,
                ),
                0,
            )
            cashflow["ppmt"] = np.where(
                cashflow["year"] <= self.param.loan_nyear,
                -npf.ppmt(
                    self.param.loan_rate,
                    cashflow["year"],
                    self.param.loan_nyear,
                    loan,
                ),
                0,
            )
            cashflow["depreciation"] = np.where(
                cashflow["year"] <= self.param.tax_depreciation_nyear,
                capextotal / self.param.tax_depreciation_nyear,
                0,
            )
            cashflow["cost"] = (
                cashflow["elecCost"]
                + cashflow["opex"]
                + cashflow["ipmt"]
                + cashflow["ppmt"]
                + np.where(cashflow["year"] == 1, equity, 0)
            )
            cashflow["costTax"] = (
                cashflow["elecCost"]
                + cashflow["opex"]
                + cashflow["ipmt"]
                + cashflow["depreciation"]
            )
            cashflow["grossRev"] = cashflow["income"] - cashflow["cost"]
            cashflow["grossRevTax"] = cashflow["income"] - cashflow["costTax"]
            cashflow["tax"] = (
                np.maximum(cashflow["grossRevTax"], 0) * self.param.tax_rate
            )
            cashflow["netRev"] = cashflow["grossRev"] - cashflow["tax"]
            cashflow["discRev"] = (
                cashflow["netRev"] / (1 + self.param.discount_rate) ** cashflow["year"]
            )
            cashflow["npv"] = cashflow["discRev"].cumsum()
            return cashflow
        except (KeyError, AttributeError) as e:
            logger.error("Error calculating costs", exc_info=True)
            raise NpvComputationError(f"Error calculating costs: {e}") from e

    def _calculate_lcoe(self, cashflow: DataFrame, equity: float) -> float64:
        try:
            cashflow["lcoe_kWh"] = (cashflow["enTemp"] * Constants.GJ2kWh) * (
                1 - self.param.tax_rate
            )
            discountedenergy = npf.npv(self.param.discount_rate, cashflow["lcoe_kWh"])
            cashflow["lcoe_costs"] = (
                cashflow["elecCost"]
                + cashflow["opex"]
                + cashflow["ipmt"]
                + cashflow["ppmt"]
                - cashflow["costTax"] * self.param.tax_rate
            )
            discountedcosts = (
                npf.npv(self.param.discount_rate, cashflow["lcoe_costs"]) + equity
            )
            lcoe = 100 * discountedcosts / discountedenergy
            return lcoe
        except (KeyError, AttributeError, ZeroDivisionError) as e:
            logger.error("Error calculating LCOE", exc_info=True)
            raise NpvComputationError(f"Error calculating LCOE: {e}") from e

    def _set_lcoe_attributes(self, cashflow: DataFrame) -> None:
        try:
            self.economics.cop = cashflow["enTemp"].sum() / (
                cashflow["enProd"].sum() + cashflow["enInj"].sum()
            )
            self.economics.power = (
                cashflow["enTemp"].sum()
                * Constants.GJ2kWh
                * 1e-3
                / (len(cashflow) * self.param.loadhours)
            )
        except (KeyError, AttributeError, ZeroDivisionError) as e:
            logger.error("Error setting LCOE attributes", exc_info=True)
            raise NpvComputationError(f"Error setting LCOE attributes: {e}") from e


def _split_dataframe(
    cashflow: DataFrame, well_tokens: List[str], keep_first: int = 4
) -> None:
    """
    Split dataframe into field and techno-economic results and well-name related quantities
    """
    tokens = [t.upper() for t in well_tokens]
    cols = [str(c).upper() for c in cashflow.columns]
    is_well = [any(tok in col for tok in tokens) for col in cols]

    base_cols = cashflow.columns[:keep_first].tolist()
    well_cols = [
        c for c, flag in zip(cashflow.columns, is_well) if c not in base_cols and flag
    ]
    econ_cols = [
        c
        for c, flag in zip(cashflow.columns, is_well)
        if c not in base_cols and not flag
    ]

    df_pure_well_reated = cashflow[base_cols + well_cols].copy()
    df_economic = cashflow[base_cols + econ_cols].copy()
    return df_economic, df_pure_well_reated


def _set_units_attrs(cashflow: DataFrame) -> None:
    """Set Series.attrs['unit'] for the columns you already know."""
    for col, unit in UNIT_MAP.items():
        if col in cashflow.columns:
            try:
                cashflow[col].attrs["unit"] = unit
            except Exception:
                # As a fallback, keep supporting your previous .unit attribute too
                try:
                    setattr(cashflow[col], "unit", unit)
                except Exception:
                    pass


def _split_name_unit(colname: str) -> tuple[str, Optional[str]]:
    """
    Split 'name[unit]' into ('name', 'unit'), or ('name', None) if no trailing [unit].
    No regex: looks for the last '[' and requires a closing ']' at the end.
    """
    name = str(colname)
    if name.endswith("]"):
        i = name.rfind("[")
        if i != -1:
            base = name[:i]
            unit = name[i + 1 : -1]
            if base and unit:
                return base, unit
    return name, None


def _contains_any_token(
    s: str, tokens: Iterable[str], case_insensitive: bool = True
) -> bool:
    if case_insensitive:
        s = s.lower()
        tokens = [t.lower() for t in tokens]
    return any(t in s for t in tokens)


def _infer_unit_for_column_base(
    base: str,
    well_tokens: Iterable[str],
    unit_map_exact: Dict[str, str],
    well_prefix_unit: Dict[str, str],
    case_insensitive: bool = True,
) -> Optional[str]:
    """
    Resolve unit for a column *base* (without trailing [unit]) using:
      1) exact-name map (UNIT_MAP),
      2) well prefix + token presence (WELL_PREFIX_UNIT).
    """
    if base in unit_map_exact:
        return unit_map_exact[base]
    if _contains_any_token(base, well_tokens, case_insensitive=case_insensitive):
        for prefix, unit in well_prefix_unit.items():
            if base.startswith(prefix):
                return unit
    return None


def _add_units_and_rename(
    df: pd.DataFrame,
    well_tokens: Iterable[str],
    unit_map_exact: Dict[str, str] = UNIT_MAP,
    well_prefix_unit: Dict[str, str] = WELL_PREFIX_UNIT,
    prefer_series_attrs: bool = True,
    mode: str = "replace",  # "append" | "replace" | "skip"
    inplace: bool = False,
) -> pd.DataFrame:
    """
    - Sets df[col].attrs['unit'] where resolvable.
    - Renames columns to 'name[unit]' idempotently.
    - 'mode':
        * append: add [unit] if missing; keep existing if present.
        * replace: enforce computed unit, overwrite existing [..].
        * skip: never touch columns that already end with [..].
    """
    if mode not in {"append", "replace", "skip"}:
        raise ValueError("mode must be one of {'append','replace','skip'}")

    rename = {}
    for col in df.columns:
        base, existing_unit = _split_name_unit(col)

        # Prefer unit already set on Series (if requested)
        unit = None
        if prefer_series_attrs and base in df.columns:
            try:
                unit = df[base].attrs.get("unit")
            except Exception:
                unit = None

        # If not from attrs, infer from maps (exact/well-prefix/extra)
        if not unit:
            unit = _infer_unit_for_column_base(
                base=base,
                well_tokens=well_tokens,
                unit_map_exact=unit_map_exact,
                well_prefix_unit=well_prefix_unit,
            )

        # Store on attrs if found
        if unit and base in df.columns:
            try:
                df[base].attrs["unit"] = unit
            except Exception:
                pass  # attrs are best-effort metadata

        # Decide new column name
        new_name = col
        if unit:
            if existing_unit is None:
                if mode in {"append", "replace"}:
                    new_name = f"{base}[{unit}]"
            else:
                if mode == "replace" and existing_unit != unit:
                    new_name = f"{base}[{unit}]"
                # append/skip: keep as-is

        if new_name != col:
            rename[col] = new_name

    if inplace:
        df.rename(columns=rename, inplace=True)
        return df
    else:
        return df.rename(columns=rename)
