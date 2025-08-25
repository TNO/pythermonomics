from pydantic import BaseModel, Field


class TechnoEconomicParameters(BaseModel):
    """
    Configuration class for geothermal system techno-economic parameters.
    This class defines the parameters required for NPV and LCOE calculations.
    """

    loadhours: int = Field(
        8766,
        description="Amount of hours in a year the production is operational (default = 24 * 365.25 = 8766)",
    )
    wellcost_scaling: float = Field(..., description="Scaling factor for well cost")
    wellcost_base: float = Field(..., description="Base cost for a well in EUR")
    well_curvfac: float = Field(
        ...,
        description="Correction factor for measured depth (MD) from piecewise linear",
    )
    wellcost_linear: float = Field(
        ..., description="Cost in EUR per meter MD (linear term)"
    )
    wellcost_cube: float = Field(
        ..., description="Cost in EUR per meter^2 MD (cubic term)"
    )
    pump_efficiency: float = Field(..., description="Pump efficiency (fraction)")
    pump_cost: float = Field(..., description="Pump cost in EUR for all wells")
    pump_life: int = Field(..., description="Pump lifetime in years")
    CAPEX_base: float = Field(
        ..., description="Base capital expenditure for heat conversion in EUR"
    )
    CAPEX_variable: float = Field(
        ..., description="Variable CAPEX in EUR per kWth installed"
    )
    CAPEX_contingency: float = Field(
        ..., description="Contingency factor applied to CAPEX and well costs"
    )
    OPEX_base: float = Field(
        ..., description="Base operational expenditure in kEUR/year"
    )
    OPEX_variable: float = Field(
        ..., description="Variable OPEX in EUR per kWth installed"
    )
    OPEX_variable_produced: float = Field(
        1.0, description="Variable OPEX in EUR cents per kWh produced"
    )
    equity_share: float = Field(
        ..., description="Fraction of equity in project financing"
    )
    loan_nyear: int = Field(..., description="Loan duration in years")
    loan_rate: float = Field(..., description="Loan interest rate")
    discount_rate: float = Field(..., description="Discount rate for equity share")
    inflation_rate: float = Field(..., description="Inflation rate")
    tax_rate: float = Field(..., description="Corporate tax rate")
    tax_depreciation_nyear: int = Field(
        ..., description="Number of years for tax depreciation"
    )
    heat_price: float = Field(..., description="Heat price in EUR cents per kWh")
    heat_price_feedin: float = Field(
        ..., description="Heat price during subsidy years in EUR cents per kWh"
    )
    electricity_price: float = Field(
        ..., description="Electricity price in EUR cents per kWh"
    )
    lifecycle_years: int = Field(..., description="Project lifetime in years")
    subsidy_years: int = Field(..., description="Number of years subsidy is applied")
