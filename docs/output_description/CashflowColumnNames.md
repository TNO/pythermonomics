# **Cashflow Column Names and Units**

This page describes the meaning and units of columns in the cashflow DataFrame/CSV.

---

## **General Columns**
- **time**: Simulation time [days]  
- **year**: Simulation time in years [years]  
- **dTime**: Time step length [days]  

---

## **Aggregate Energy and Power**
- **enTemp**: Total effective energy contained in produced water [GJ]  
- **enProd**: Total pumping energy for all production wells [GJ]  
- **enInj**: Total pumping energy for all injection wells [GJ]  
- **enPower**: Total effective power produced [MW]  
- **enPowercons**: Total power consumed [MW]  
- **COP**: Coefficient of Performance [-]  

---

## **Economic Columns**
- **capex**: Total capital expenditure [euro]  
- **wellcosts**: Total well costs [euro]  
- **opex**: Operational expenditure [euro]  
- **income**: Income from heat sales [euro]  
- **elecCost**: Electricity cost [euro]  
- **ipmt**: Interest payment on the loan for the year [euro]  
- **ppmt**: Principal payment on the loan for the year [euro]  
- **depreciation**: Depreciation for tax purposes [euro]  
- **cost**: Total costs [euro]  
- **costTax**: Taxable costs [euro]  
- **grossRev**: Gross revenue [euro]  
- **grossRevTax**: Gross revenue for tax calculation [euro]  
- **tax**: Taxes paid [euro]  
- **netRev**: Net revenue [euro]  
- **discRev**: Discounted revenue [euro]  
- **npv**: Net Present Value [euro]  
- **lcoe_kWh**: Discounted energy for LCOE calculation [kWh equivalent]  
- **lcoe_costs**: Discounted costs for LCOE calculation [euro]  
- **lcoe**: Levelized Cost of Energy [-]  

---

## **Well-Related Columns (Per Well)**
These columns repeat for each well token (e.g., `INJ1`, `PRD1`):

- **temp_\<WELL\>**: Bottom-hole temperature [°C]  
- **wicum_\<WELL\>**: Unscaled cumulative injected water [m³]  
- **winj_\<WELL\>**: Injected water volume in current step [m³]  
- **wiRate_\<WELL\>**: Daily injection rate [m³/day]  
- **wpcum_\<WELL\>**: Unscaled cumulative produced water [m³]  
- **wprod_\<WELL\>**: Produced water volume in current step [m³]  
- **wpRate_\<WELL\>**: Daily production rate [m³/day]  
- **dTemp_\<WELL\>**: Temperature difference between producer and injector [°C]  
- **enInj_\<WELL\>**: Pumping energy for injection [GJ]  
- **enTemp_\<WELL\>**: Energy contained in produced water [GJ]  
- **enProd_\<WELL\>**: Pumping energy for production [GJ]  
- **dP_\<WELL\>**: Pressure difference [bar]  

---

## **Aggregate Well KPIs**
- **injTemp**: Injection temperature [°C]  
- **prodTemp**: Production temperature [°C]  
- **avgInjP**: Average injection pressure [bar]  
