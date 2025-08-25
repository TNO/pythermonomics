import logging
import os
import re
from collections import defaultdict
from enum import StrEnum
from typing import Dict, List

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class WellState(StrEnum):
    PRODUCTION = "prod"
    INJECTION = "inj"
    SHUT_IN = "shut"


WELL_STATE_KEYWORDS = "WSTAT"
BOTTOM_HOLE_PRESSURE = "WBHP"


def WELL_WATER_RATE(well_type: str) -> str:
    return f"WW{well_type.upper()}R"


def WATER_TEMPERATURE(well_type: str) -> str:
    return f"WT{well_type.upper()}CHEA"


def WELL_WATER_TOTAL(well_type: str) -> str:
    return f"WW{well_type.upper()}T"


PRODUCER_KEYWORDS = [
    WELL_WATER_RATE("P"),
    BOTTOM_HOLE_PRESSURE,
    WATER_TEMPERATURE("P"),
    WELL_WATER_TOTAL("P"),
    WELL_STATE_KEYWORDS,
]

INJECTOR_KEYWORDS = [
    WELL_WATER_RATE("I"),
    BOTTOM_HOLE_PRESSURE,
    WATER_TEMPERATURE("I"),
    WELL_WATER_TOTAL("I"),
    WELL_STATE_KEYWORDS,
]

REQUIRED_OPM_WELL_KEYWORDS = sorted(
    list(set().union(set(PRODUCER_KEYWORDS), set(INJECTOR_KEYWORDS)))
)
REQUIRED_OPM_KEYWORDS = ["DATES", "YEARS", "FPR"] + REQUIRED_OPM_WELL_KEYWORDS

TEMPERATURE_MAP = {
    WellState.INJECTION: WATER_TEMPERATURE("I"),
    WellState.PRODUCTION: WATER_TEMPERATURE("P"),
}
WELL_STATE_MAP = {
    1.0: WellState.PRODUCTION,
    2.0: WellState.INJECTION,
    3.0: WellState.SHUT_IN,
}

DAYS_PER_YEAR = 365.0
RATIO_RESDATA_TO_OPM = 365.25 / 365.0
MISSING_COLUMNS = [
    "DAYS",
]


class SimulationDataReader:
    """Class to read OPM/Eclipse simulation data from CSV files."""

    def __init__(
        self, csv_file: str, add_single_temperature_column: bool = False
    ) -> None:
        """
        :param csv_file: Path to the CSV file containing simulation data.
        :param add_single_temperature_column: If True, adds a single temperature column for the well
        """
        logger.debug(f"Initializing SimulationDataReader for file: {csv_file}")
        self.csv_file: str = csv_file
        self.add_temperature_column: bool = add_single_temperature_column
        self.data: pd.DataFrame = self.read_data()
        logger.debug(f"Read data shape: {self.data.shape}")
        self.verify_keys_are_present()
        self.validate_well_keywords()
        self.rescale_years_for_acccount_leap_years()
        self.add_missing_columns()
        self.data = self.filter_out_whole_years()
        logger.debug(f"Filtered data shape: {self.data.shape}")
        self.REQUIRED_KEYS: list = self.get_required_columns_from_df()
        logger.debug(f"Required columns: {self.REQUIRED_KEYS}")
        self.WELL_NAMES: List[str] = self.extract_well_names_from_csv()
        logger.debug(f"Extracted well names: {self.WELL_NAMES}")
        self.WELL_STATES: Dict[str, WellState] = (
            self.extract_well_states_final_timestep()
        )
        logger.debug(f"Final well states: {self.WELL_STATES}")
        if self.add_temperature_column:
            self.add_single_temperature_column()
        return

    def read_data(self) -> pd.DataFrame:
        """
        Read data from the CSV file.
        Returns:
            pd.DataFrame: DataFrame containing the simulation data.
        """
        if not os.path.exists(self.csv_file):
            logger.error(f"CSV file {self.csv_file} does not exist.")
            raise FileNotFoundError(f"CSV file {self.csv_file} does not exist.")
        df = pd.read_csv(self.csv_file)
        logger.debug(f"Loaded DataFrame with columns: {df.columns.tolist()}")
        return df

    def verify_keys_are_present(self) -> None:
        """
        Verify that all required keys are present in the DataFrame.
        Raises:
            KeyError: If any required keys are missing.
        """
        logger.debug("Verifying required keys are present in data")
        missing_keys = [
            key
            for key in REQUIRED_OPM_KEYWORDS
            if not any(col.startswith(key) for col in self.data.columns)
        ]
        if missing_keys:
            logger.error(f"Missing keys in data: {missing_keys}")
            raise KeyError(f"Missing keys in data: {', '.join(missing_keys)}")
        logger.debug("All required keys are present")
        return

    def get_relevant_simulation_results(self) -> pd.DataFrame:
        """
        Extract relevant simulation results from the DataFrame.
        Returns:
            pd.DataFrame: DataFrame containing only the relevant simulation results.
        """
        logger.debug("Extracting relevant simulation results")
        return self.data[self.REQUIRED_KEYS].copy()

    def get_required_columns_from_df(self) -> List[str]:
        """
        Determine the required columns from the DataFrame based on predefined keywords.
        Returns:
            List[str]: List of required column names.
        """
        logger.debug("Determining required columns from DataFrame")
        required_columns: List[str] = []
        for key in REQUIRED_OPM_KEYWORDS:
            if key in self.data.columns:
                required_columns.append(key)
            else:
                pattern = re.compile(rf"^{re.escape(key)}:.+")
                matches = [col for col in self.data.columns if pattern.match(col)]
                required_columns.extend(matches)
        required_columns.extend(MISSING_COLUMNS)
        logger.debug(f"Required columns determined: {required_columns}")
        return required_columns

    def validate_well_keywords(self) -> None:
        """
        Validate that each well has all required keywords.
        """
        logger.debug("Validating well keywords for each well")
        wells = defaultdict(set)
        for col in self.data.columns:
            if ":" in col:
                keyword, well = col.split(":", 1)
                if keyword in REQUIRED_OPM_WELL_KEYWORDS:
                    wells[well].add(keyword)
        missing = {
            well: [kw for kw in REQUIRED_OPM_WELL_KEYWORDS if kw not in kws]
            for well, kws in wells.items()
            if any(kw not in kws for kw in REQUIRED_OPM_WELL_KEYWORDS)
        }
        if missing:
            logger.error(f"Missing keywords per well: {missing}")
            raise KeyError(f"Missing keywords per well: {missing}")
        logger.debug("All wells have required keywords")
        return

    def add_missing_columns(self) -> None:
        """
        Add missing columns to the DataFrame, specifically DAYS based on YEARS.
        """
        logger.debug("Adding missing columns to data")
        self.data["DAYS"] = self.data["YEARS"] * DAYS_PER_YEAR
        logger.debug("Added DAYS column")
        return

    def rescale_years_for_acccount_leap_years(self) -> None:
        """
        Rescale the YEARS column to account for leap years.
        """
        logger.debug("Rescaling YEARS to account for leap years")
        self.data["YEARS"] = self.data["YEARS"] * RATIO_RESDATA_TO_OPM
        logger.debug("Rescaled YEARS column")
        return

    def filter_out_whole_years(self) -> pd.DataFrame:
        """
        Filter out whole years from the data based on the YEARS column.
        Returns:
            pd.DataFrame: DataFrame with whole years filtered out.
        """
        logger.debug("Filtering out whole years from data")
        years_array = np.array(self.data["YEARS"])
        integer_years = np.floor(years_array).astype(int)
        unique_years = np.unique(integer_years)
        closest_indices = np.array(len(unique_years) * [0], dtype=int)
        logger.debug(f"Unique years found: {unique_years}")

        for count, year in enumerate(unique_years):
            # Compute distance to the next integer
            distances = years_array - year
            # Prefer positive distances (just above the integer)
            positive_mask = distances > 0
            if np.any(positive_mask):
                # Among positive distances, choose the smallest
                best_idx = np.argmin(distances[positive_mask])
                selected_value = years_array[positive_mask][best_idx]
            else:
                # If no positive distances, choose the closest overall
                best_idx = np.argmin(np.abs(distances))
                selected_value = years_array[best_idx]
            closest_indices[count] = np.where(years_array == selected_value)[0][0]
            logger.debug(f"Year {year}: selected index {closest_indices[count]}")

        filtered = self.data.copy().iloc[closest_indices].reset_index(drop=True)

        # Clip YEARS and DAYS to closests integer values
        filtered["YEARS"] = unique_years
        filtered["DAYS"] = filtered["YEARS"] * DAYS_PER_YEAR

        logger.debug(
            f"Filtered data shape after whole year selection: {filtered.shape}"
        )
        return filtered

    def extract_well_names_from_csv(self) -> List[str]:
        """
        Extract well names from the DataFrame columns.
        Returns:
            List[str]: Sorted list of unique well names.
        """
        logger.debug("Extracting well names from CSV columns")
        well_names = set()
        for col in self.data.columns:
            if ":" in col:
                keyword, well_name = col.split(":", 1)
                if keyword in REQUIRED_OPM_WELL_KEYWORDS:
                    if well_name not in well_names:
                        well_names.add(well_name)
        logger.debug(f"Well names extracted: {well_names}")
        return sorted(list(well_names))

    def extract_well_states_final_timestep(self) -> Dict[str, WellState]:
        logger.debug("Extracting well states at final timestep")
        return self.extract_well_states_at_timestep(timestep=-1)

    def extract_well_states_at_timestep(self, timestep: int) -> Dict[str, WellState]:
        """
        Extract well states at a specific timestep.

        :param timestep: Timestep index to extract well states from.

        Returns:
            Dict[str, WellState]: Dictionary mapping well names to their states.
        """
        well_states = {}
        wstat_cols = self.data.filter(like=WELL_STATE_KEYWORDS, axis=1)
        if wstat_cols.empty:
            logger.error("No well state columns found in data.")
            raise KeyError("No well state columns found in data.")
        for col in wstat_cols:
            _, well_name = col.split(":", 1)
            if well_name not in well_states:
                final_value = self.data[col].iloc[timestep]
                well_states[well_name] = WELL_STATE_MAP.get(
                    final_value, WellState.SHUT_IN
                )
                logger.debug(f"Well {well_name}: state {well_states[well_name]}")
        return well_states

    def add_single_temperature_column(self) -> None:
        """
        Add a column with temperature for each well irrelevant of the state.
        This is useful for cases where temperature is needed for all wells regardless of their state.
        The column will be named T:<well_name> and will contain the temperature from the respective
        WATER_TEMPERATURE keyword for the well's state.
        """
        logger.debug("Adding single temperature column for each well")
        for well_name, state in self.WELL_STATES.items():
            source_col = f"{TEMPERATURE_MAP[state.value]}:{well_name}"
            target_col = f"T:{well_name}"
            if source_col in self.data.columns:
                self.data[target_col] = self.data[source_col]
                self.REQUIRED_KEYS.append(f"T:{well_name}")
                logger.debug(f"Added temperature column {target_col} from {source_col}")
            else:
                logger.error(
                    f"Missing temperature column: {source_col} for well {well_name}"
                )
                raise KeyError(
                    f"Missing temperature column: {source_col} for well {well_name}"
                )
        return
