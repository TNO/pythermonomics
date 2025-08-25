import logging
import os
from typing import List, Tuple

import numpy as np

logger = logging.getLogger(__name__)


class DeviationFileReader:
    """
    Reads deviation files for wells and extracts well name and coordinates.
    """

    def __init__(self, filename: str):
        logger.debug(f"Initializing DeviationFileReader for file: {filename}")
        self.deviation_file = filename
        self.well_name, self.deviation_data = self.read_deviation_file()
        logger.debug(
            f"Read well name: {self.well_name}, deviation data shape: {self.deviation_data.shape}"
        )

    def read_deviation_file(self) -> Tuple[str, List[float]]:
        """
        Reads the deviation file and returns a tuple with a well name in string format
        and the coordinate pair (X, Y, TVDMSL, MDMSL) as a row of a np.array.

        The deviation file format is expected to be, where the end of the file is marked by -999:
        WELLNAME: 'INJ1'
        #       X           Y      TVDMSL       MDMSL
          2553.32     2277.76        0.00        0.00
          2553.28     2277.94        5.00        5.00
        ...
          2485.83     5155.36     2854.80     5973.30
        -999
        """
        if not os.path.exists(self.deviation_file):
            logger.error(f"Deviation file {self.deviation_file} does not exist.")
            raise FileNotFoundError(
                f"Deviation file {self.deviation_file} does not exist."
            )
        with open(self.deviation_file, "r") as file:
            lines = file.readlines()
        logger.debug(f"Read {len(lines)} lines from deviation file")
        well_data: List[float, float, float, float] = []
        well_name = None
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line == "-999":
                logger.debug("End-of-file marker '-999' found, stopping read")
                break
            if line.startswith("WELLNAME:"):
                well_name = line.split(":")[1].strip().strip("'")
                logger.debug(f"Found well name: {well_name}")
            else:
                parts = line.split()
                if len(parts) == 4:
                    try:
                        coords = [float(part) for part in parts]
                        well_data.append(coords)
                        logger.debug(f"Added coordinates: {coords}")
                    except ValueError:
                        logger.error(f"Invalid coordinate data in line: {line}")
                        raise ValueError(f"Invalid coordinate data in line: {line}")
                else:
                    logger.error(f"Invalid line format: {line}")
                    raise ValueError(f"Invalid line format: {line}")
        if not well_data:
            logger.error("No valid well data found in the deviation file.")
            raise ValueError("No valid well data found in the deviation file.")
        logger.debug(f"Returning well name: {well_name}, data points: {len(well_data)}")
        return well_name, np.array(well_data)
