from typing import Dict

from numpy import ndarray
from pandas import DataFrame


class BaseWellResults:
    def __init__(self):
        self.wellRes: DataFrame = None
        self.wells_and_states: Dict[str, str] = None
        self.WXYZ: Dict[str, ndarray] = None
