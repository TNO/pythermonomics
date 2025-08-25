# -*- coding: utf-8 -*-
"""
Compute costs of (multilateral) well based on well  trajectories
"""

from typing import TYPE_CHECKING

from pywellgeo.well_data.names_constants import Constants

if TYPE_CHECKING:
    from pythermonomics.geothermal_economics import GeothermalEconomics

from numpy import float64


class CostModelWell:
    """
    Cost model for wells based on well trajectories.
    This model computes the total well costs based on the cumulative AHD (Along Hole Depth)
    and the well cost parameters defined in the GeothermalEconomics instance.
    """

    def __init__(self, geothermal_economics: "GeothermalEconomics") -> None:
        """
        :param geothermal_economics: containing parameters for cubic well costs as function of AHD
        """
        self.geothermal_economics = geothermal_economics

    def compute_costs(self) -> float64:
        """
        :param compute total wells costs based on well measured depth (along hole depth)
        :return:
        """
        t = self.geothermal_economics.welltrajectory.tw

        wellcosts = 0
        for w in t.keys():
            wmd = t[w][Constants.WELLTREE].cumulative_ahd()
            wmd *= (
                self.geothermal_economics.economics_config.techno_eco_param.well_curvfac
            )
            wcost = (
                self.geothermal_economics.economics_config.techno_eco_param.wellcost_base
                + self.geothermal_economics.economics_config.techno_eco_param.wellcost_linear
                * wmd
                + self.geothermal_economics.economics_config.techno_eco_param.wellcost_cube
                * wmd**2
            )
            wcost *= (
                self.geothermal_economics.economics_config.techno_eco_param.wellcost_scaling
            )
            wellcosts = wellcosts + wcost

        return wellcosts
