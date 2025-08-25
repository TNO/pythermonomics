# Net Present Value and LCOE Equations

This page documents the main equations used in the geothermal economics calculations, as implemented in `EconomicsCalculator.compute_economics()`.

---

## Net Present Value (NPV)

The Net Present Value (NPV) is the sum of all discounted net revenues over the project lifetime:

$$
\mathrm{NPV} = \sum_{t=0}^{N} \mathrm{DR}(t) = \sum_{t=0}^{N} \frac{\mathrm{NR}(t)}{(1 + r)^{t}}
$$

where:

- $\mathrm{DR}(t)$ is the discounted revenue for each year $t$
- $\mathrm{NR}(t)$ is the net revenue in year $t$
- $r$ is the discount rate
- $t$ is the year index

### Net Revenue

Net revenue is calculated as:

$$
\mathrm{NR}(t) = \mathrm{GR}(t) - \mathrm{T}(t)
$$

where:

- the gross revenue is calculated as $\mathrm{GR}(t) = \mathrm{I}(t) - \mathrm{C}(t)$
- the tax is calculated as $\mathrm{T}(t) = \max(\mathrm{TGR}(t), 0) \cdot \mathrm{T_r}$
- $\mathrm{T_r}$ is the tax rate
- and the taxable gross revenue is calculated as $\mathrm{TGR}(t) = \mathrm{I}(t) - \mathrm{C_{tax}}(t)$

---

## Income

The income is based on the produced energy and the heat price (with possible subsidy):

$$
\mathrm{I}(t) = \mathrm{E_{p,w}}(t) \cdot \mathrm{HP}(t)
$$

where:

- $\mathrm{E_{p,w}}(t)$ is the total effective energy contained in produced water
- $\mathrm{HP}(t)$ is either the feed-in price or the regular price, depending on the subsidy period

---

## Costs

### Total costs

Total costs are the sum of electricity cost, OPEX, loan payments, and equity:

$$
\mathrm{C}(t) = \mathrm{C_{elec}}(t) + \mathrm{C_{opex}}(t) + \mathrm{IP}(t) + \mathrm{PP}(t) + \mathrm{Eq}
$$

where:

- Electricity costs, $\mathrm{C_{elec}}(t)$, are defined below
- Operational costs, $\mathrm{C_{opex}}(t)$, are defined below

and interest $\mathrm{IP}(t)$ and principal $\mathrm{PP}(t)$ payments are calculated using standard annuity formulas (based on the size of the loan $L$, the loan rate $L_{rate}$, and number of loan years $L_{year}$).

and equity is defined as

$$ 
\mathrm{Eq} = \mathrm{C_{capex,tot}} \cdot \mathrm{Eq}_{\text{share}}
$$

where $\mathrm{C_{capex,tot}}$ is the total CAPEX costs and $\mathrm{Eq}_{\text{share}}$ is the equity share (%) and the loan is defined as

$$ 
\mathrm{L} = \mathrm{C_{capex,tot}} - \mathrm{Eq}
$$

Taxable costs include depreciation:

$$
\mathrm{C_{tax}}(t) = \mathrm{C_{elec}}(t) + \mathrm{C_{opex}}(t) + \mathrm{IP}(t) + \mathrm{D}(t)
$$

### Capital Expenditure (CAPEX)

The CAPEX is calculated in steps:

$$
\mathrm{C_{capex,o}} = \mathrm{C_{capex,b}} + \mathrm{C_{capex,v}} \cdot \mathrm{P_{i}}(0)
$$

where:

- $\mathrm{C_{capex,b}}$ is the base capital expenditure for the project,
- $\mathrm{C_{capex,v}}$ is the variable capital expenditure per installed kW,
- $\mathrm{P_{i}}(0)$ is the installed power capacity at the start of the project.

The total CAPEX including well costs, contingency, and pump costs is:

$$
\mathrm{C_{capex,tot}} = \left( \mathrm{C_{capex,o}} + \mathrm{C_{wells}} \right) \cdot (1 + \mathrm{C_{capex,c}}) + N_{\text{wi}} \cdot \mathrm{C_{pump}}
$$

where:

- $\mathrm{C_{wells}}$ is the total cost of all wells,
- $\mathrm{C_{capex,c}}$ is the contingency fraction,
- $N_{\text{wi}}$ is the number of injection wells,
- $\mathrm{C_{pump}}$ is the cost per pump.

The CAPEX is assigned to the first year in the cashflow.

### Electricity Cost

$$
\mathrm{C_{elec}}(t) = (\mathrm{E_{c,inj}}(t) + \mathrm{E_{c,prd}}(t))   \cdot \mathrm{EP} \cdot (1 + \mathrm{i_r})^{t}
$$

where:

- $\mathrm{E_{c,inj}}(t)$ is the energy required to operate the injection pump per well [GJ]
- $\mathrm{E_{c,prd}}(t)$ is the energy required to operate the production pump per well [GJ] 
- $\mathrm{i_r}$ is the inflation rate

---

## Depreciation

Depreciation is linear over the depreciation period:

$$
\mathrm{D}(t) =
\begin{cases}
\frac{\mathrm{C_{capex,tot}}}{\mathrm{D_{years}}} & \text{if } t \leq \mathrm{D_{years}} \\
0 & \text{otherwise}
\end{cases}
$$

---

## Fully Expanded NPV Equation

$$
\mathrm{NPV} = \sum_{t=0}^{N} \frac{\mathrm{I}(t) - \mathrm{T}(t) - \mathrm{C}(t)}{(1+r)^{t}} = \sum_{t=0}^{N} \frac{\mathrm{I}(t) - \mathrm{T}(t) - \big(\mathrm{C_{elec}}(t) + \mathrm{C_{opex}}(t) + \mathrm{IP}(t) + \mathrm{PP}(t) + \mathrm{Eq} \big)}{(1+r)^{t}}
$$

---

## Levelized Cost of Energy (LCOE)

The LCOE is the ratio of discounted costs to discounted energy output:

$$
\mathrm{LCOE} = 100 \cdot
\frac{
\sum_{t=0}^{N} \frac{\mathrm{C_{elec}}(t) + \mathrm{C_{opex}}(t) + \mathrm{IP}(t) + \mathrm{PP}(t) - \mathrm{C_{tax}}(t) \cdot \mathrm{T_r} + \mathrm{Eq}}{(1 + r)^{t}}}
{
\sum_{t=0}^{N} \frac{(\mathrm{E_{p,w}}(t) ) \cdot (1 - \mathrm{T_r})}{(1 + r)^{t}}}
$$

---

For further details, see the [EconomicsCalculator](../api/npv_model/EconomicsCalculator.md) API documentation.

---