# TechnoEconomicParameters

**Module:** `pythermonomics.config.techno_economics_config`

Defines system techno-economic parameters for NPV and LCOE calculations.

## Purpose

- Stores all techno-economic parameters (loadhours, pump_efficiency, CAPEX_base, OPEX_base, etc.).
- Used for all financial calculations.

## Main Fields

- `loadhours`: Operational hours per year
- `wellcost_scaling`: Scaling factor for well cost
- `pump_efficiency`: Pump efficiency
- `CAPEX_base`: Base CAPEX for heat conversion
- `OPEX_base`: Base OPEX per year
- `equity_share`: Project equity fraction
- `loan_nyear`: Loan duration (years)
- `loan_rate`: Loan interest rate
- `discount_rate`: Discount rate for equity share
- `heat_price`: Heat price (EURct/kWh)
- ...and more (see source for full list)

## Usage

```python
from pythermonomics.config.techno_economics_config import TechnoEconomicParameters

techno_eco_params = TechnoEconomicParameters(
    loadhours=6000,
    pump_efficiency=0.6,
    # ...other parameters...
)
```