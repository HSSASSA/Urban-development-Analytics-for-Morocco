# Data Dictionary - Urban Development Analytics

## Overview
This document defines all fields, metrics, and their descriptions across the four main datasets.

---

## 1. Urban Indicators Table

Comprehensive urban development metrics for analysis and policy planning.

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| **indicator_id** | INT | 1-5000 | Unique identifier for each record |
| **region** | STRING | 5 values | Moroccan region: Casablanca-Settat, Fès-Meknès, Marrakech-Safi, Rabat-Salé-Kénitra, Tanger-Tétouan-Al Hoceïma |
| **city** | STRING | City_1...City_5000 | City identifier |
| **city_type** | STRING | 4 values | Classification: Metropolitan, Urban, Peri-urban, Rural |
| **year** | INT | 2015-2023 | Fiscal year |
| **population** | INT | 10K-500K | Total population in thousands |
| **urban_area_km2** | FLOAT | 50-450 | Urban area in square kilometers |
| **population_density** | FLOAT | 100-2000 | Persons per square kilometer |
| **housing_units** | INT | 2K-20K | Total housing units available |
| **houses_with_water_access** | FLOAT | 0.6-1.0 | Proportion of houses with water access (0-1 scale) |
| **houses_with_electricity** | FLOAT | 0.75-1.0 | Proportion of houses with electricity (0-1 scale) |
| **unemployment_rate** | FLOAT | 5-30 | Unemployment rate in percentage |
| **gdp_per_capita** | FLOAT | 10K-80K | GDP per capita in DH (Moroccan Dirham) |
| **urbanization_rate** | FLOAT | 0-1 | Derived: proportion urban vs. total |
| **housing_need_index** | FLOAT | 0-100 | Derived: population / housing_units ratio |
| **infrastructure_score** | FLOAT | 0.675-1.0 | Derived: average of water + electricity access |

### Key Metrics Explained

**Urbanization Rate**: 
- Formula: `population / (population + baseline_rural)`
- High values indicate rapid urbanization

**Housing Need Index**: 
- Formula: `population / (housing_units + 1)`
- Higher values indicate housing shortage

**Infrastructure Score**: 
- Formula: `(water_access + electricity_access) / 2`
- Indicator of basic service coverage

---

## 2. Housing Table

Housing market and residential development metrics.

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| **housing_id** | INT | 1-3000 | Unique housing record ID |
| **region** | STRING | 5 values | Region classification |
| **city** | STRING | City_1...City_50 | City identifier |
| **year** | INT | 2015-2023 | Fiscal year |
| **housing_units_completed** | INT | 0-2000 | Units completed this year |
| **housing_units_planned** | INT | 0-5000 | Units planned for development |
| **affordable_housing_units** | INT | 0-1500 | Units classified as affordable |
| **price_per_sqm_dirham** | FLOAT | 5K-50K | Average price per square meter in DH |
| **vacancy_rate** | FLOAT | 5-20 | Percentage of vacant units (5-20%) |
| **household_size** | FLOAT | 3-6 | Average persons per household |
| **housing_completion_rate** | FLOAT | 0-1 | Derived: completed / planned ratio |
| **affordable_housing_ratio** | FLOAT | 0-1 | Derived: affordable / completed ratio |
| **affordability_index** | FLOAT | 0.5-2.0 | Derived: price vs. median price ratio |

### Key Metrics Explained

**Housing Completion Rate**: 
- Formula: `units_completed / (units_planned + 1)`
- Measures development project execution

**Affordable Housing Ratio**: 
- Formula: `affordable_units / (completed_units + 1)`
- Government policy compliance metric

**Affordability Index**: 
- Formula: `price_per_sqm / median_price_across_dataset`
- 1.0 = median price, < 1.0 = affordable, > 1.0 = premium

---

## 3. Infrastructure Table

Public services and infrastructure development metrics.

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| **infrastructure_id** | INT | 1-2000 | Unique infrastructure record ID |
| **region** | STRING | 5 values | Region classification |
| **service_type** | STRING | 5 values | Roads, Water System, Electricity Grid, Healthcare, Education |
| **year** | INT | 2015-2023 | Fiscal year |
| **investment_millions_dh** | FLOAT | 0-300 | Annual investment in millions of DH |
| **coverage_rate** | FLOAT | 60-100 | Percentage of population covered (%) |
| **maintenance_status** | STRING | Good/Fair/Poor | Current condition assessment |
| **projects_completed** | INT | 0-10 | Count of completed projects this year |
| **projects_ongoing** | INT | 0-8 | Count of active projects |
| **maintenance_score** | INT | 1-3 | Numeric: Poor(1), Fair(2), Good(3) |
| **total_projects** | INT | 0-18 | Derived: completed + ongoing |
| **completion_efficiency** | FLOAT | 0-1 | Derived: completed / (completed + ongoing) |

### Key Metrics Explained

**Coverage Rate**: 
- Percentage of target population with service access
- Healthcare = % with facility access
- Education = % with school enrollment
- Roads = % with paved road access

**Maintenance Score**: 
- Good (3): Excellent condition, no major repairs needed
- Fair (2): Acceptable condition, routine maintenance ongoing
- Poor (1): Significant maintenance issues, deteriorating

**Completion Efficiency**: 
- Formula: `completed / (completed + ongoing)`
- Measures project delivery velocity

---

## 4. Migration Table

Internal migration and urbanization patterns.

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| **migration_id** | INT | 1-2500 | Unique migration record ID |
| **origin_region** | STRING | 5 values | Region of migration origin |
| **destination_region** | STRING | 5 values | Region of migration destination |
| **year** | INT | 2015-2023 | Fiscal year |
| **migrants_count** | INT | 50-500 | Number of people migrated in thousands |
| **rural_to_urban_ratio** | FLOAT | 0.3-0.9 | Proportion of rural-origin migrants |
| **urban_to_urban_ratio** | FLOAT | 0.1-0.7 | Proportion of urban-origin migrants |
| **other_migration_ratio** | FLOAT | 0-0.6 | Remaining migration (unclassified) |
| **urbanization_intensity** | FLOAT | 0.3-0.9 | Derived: rural_to_urban_ratio |

### Key Metrics Explained

**Migrants Count**: 
- Reported in thousands for readability
- Multiply by 1,000 for actual count

**Migration Ratios**: 
- Always sum to 1.0 (100%)
- Indicate composition of migration flows

**Urbanization Intensity**: 
- Same as rural_to_urban_ratio but normalized
- Higher values = more rural-origin migration
- Policy indicator of urbanization pressure

---

## Derived Metrics (Calculated Fields)

### Economic Competitiveness Index (future)
```
ECI = (GDP_per_capita / region_average) * unemployment_weight
      - (unemployment_rate / national_average) * 0.3
```

### Infrastructure Readiness Score (future)
```
IRS = (water_access * 0.3 + electricity_access * 0.3 
       + healthcare_coverage * 0.2 + education_coverage * 0.2)
      * maintenance_score / 3
```

### Urbanization Pressure Index (future)
```
UPI = (population_density / regional_median) 
      * (housing_need_index / 5)
      * rural_to_urban_ratio
```

---

## Data Quality Notes

### Null Handling
- Filled using median/mean imputation by region and year
- Missing values < 1% across all fields

### Outlier Treatment
- Detected using IQR (Interquartile Range)
- Extreme outliers (> 3*IQR) flagged but retained
- Investigation required before removal

### Validation Rules
- Population > 0
- Unemployment rate: 0-50%
- Water/Electricity access: 0-100%
- Vacancy rate: 0-50%
- Coverage rates: 0-100%
- All proportions: 0.0 to 1.0

### Data Currency
- All data represents as-of December 31 of fiscal year
- 8-year historical dataset (2015-2023)
- Annual reporting frequency

---

## Metadata

| Field | Value |
|-------|-------|
| **Total Records** | ~12,500 |
| **Time Period** | 2015-2023 (9 years) |
| **Geographic Scope** | 5 Moroccan regions |
| **Update Frequency** | Annual |
| **Last Updated** | April 2024 |
| **Data Source** | Synthetic (based on ministry patterns) |

---

**Version**: 1.0  
**Prepared**: April 2024

