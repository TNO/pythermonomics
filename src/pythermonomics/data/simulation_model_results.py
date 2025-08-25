import logging
import os
from typing import Dict

import numpy as np
from numpy import ndarray
from pandas import DataFrame

from pythermonomics.data.base_well_results import BaseWellResults
from pythermonomics.data.read_deviation_file import DeviationFileReader
from pythermonomics.data.read_sim_data_from_csv import SimulationDataReader

logger = logging.getLogger(__name__)

# Need to enforce a max. size for the deviation records to avoid memory issues due to recursive calls in WellTreeTNO.from_xyz
MAX_SIZE_DEVIATION_RECORD = 100


class SimulationModelResults(BaseWellResults):
    """
    Read simulation results from summary file (CSV) and well-paths from deviation files.
    """

    def __init__(
        self,
        summary_file: str,
        path_deviation_files: str,
    ) -> None:
        """
        :param summary_file: Path to the summary file (CSV) containing simulation results.
        :param path_deviation_files: Path to the directory containing deviation files for wells.
        """
        super().__init__()
        if not os.path.exists(summary_file):
            raise FileNotFoundError(f"Summary file {summary_file} does not exist.")

        if not os.path.exists(path_deviation_files):
            raise FileNotFoundError(
                f"Path to deviation files {path_deviation_files} does not exist."
            )
        if not os.listdir(path_deviation_files):
            raise FileNotFoundError(
                f"No deviation files found in path {path_deviation_files}."
            )
        if len(os.listdir(path_deviation_files)) < 2:
            raise ValueError(
                f"At least two deviation files are required in path {path_deviation_files}."
            )
        self.deck: str = summary_file
        self.path_deviation_files: str = path_deviation_files

        sim_reader = SimulationDataReader(
            summary_file, add_single_temperature_column=True
        )
        self.wellRes: DataFrame = sim_reader.get_relevant_simulation_results()
        self.wellRes = self.wellRes[self.wellRes["YEARS"] >= 1.0]
        self.wells_and_states = sim_reader.WELL_STATES

        self.WXYZ: Dict[str, ndarray] = {}
        for w in sim_reader.WELL_NAMES:
            # Read well coordinates from deviation file using DeviationFileReader
            # Assumption: Deviation files are named as <well_name>.dev
            self.WXYZ[w] = DeviationFileReader(
                os.path.join(path_deviation_files, f"{w}.dev")
            ).deviation_data

        # Subsample the WXYZ data to avoid memory issues
        for w in self.WXYZ:
            if len(self.WXYZ[w]) > MAX_SIZE_DEVIATION_RECORD:
                indices = np.linspace(
                    0, len(self.WXYZ[w]) - 1, MAX_SIZE_DEVIATION_RECORD, dtype=int
                )
                self.WXYZ[w] = self.WXYZ[w][indices]
        self.wellRes = self.wellRes.reset_index(drop=True)
