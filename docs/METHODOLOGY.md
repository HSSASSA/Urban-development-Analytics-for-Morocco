# Analysis Methodology & Formulas

## 1. Comparative Analysis Methods

### Regional Comparison

**Purpose**: Understand performance variations across Morocco's regions

**Methodology**:
```
For each region R and metric M:
  Mean(M) = SUM(M values in R) / COUNT(records in R)
  SD(M) = SQRT(SUM((M - Mean)²) / (n-1))  # Standard Deviation
  Min(M) = MINIMUM(M values in R)
  Max(M) = MAXIMUM(M values in R)
  Quartile_1 = 25th percentile
  Median = 50th percentile
  Quartile_3 = 75th percentile
```

**Interpretation**:
- High SD relative to mean = inconsistent performance
- Wide min-max range = significant disparities
- Median vs mean gap = presence of outliers

### Temporal Trend Analysis

**Purpose**: Identify how metrics change over time

**Approach**:
```
For each year Y:
  Aggregate metric by year
  Plot time series
  Identify trend direction (↑ increasing, ↓ decreasing, → flat)
  Calculate year-over-year change
```

**YoY Change**:
```
YoY_Change% = ((Value_Year2 - Value_Year1) / Value_Year1) × 100
```

### Statistical T-Test

**Purpose**: Determine if differences between groups are statistically significant

**Hypothesis**:
- H₀ (Null): No difference between groups
- H₁ (Alt): Groups are different

**Two-Sample T-Test**:
```
t = (Mean_Group1 - Mean_Group2) / SE

where:
  SE = SQRT((SD₁²/n₁) + (SD₂²/n₂))  # Standard Error

Degree of Freedom (df) = n₁ + n₂ - 2
p-value = Probability of observing result if H₀ true
```

**Decision Rule**:
- p-value < 0.05 → Significant difference (reject H₀)
- p-value ≥ 0.05 → No significant difference (fail to reject H₀)

**Example**:
```
Test: Does urban city type have different GDP than rural?
H₀: Mean_GDP_Urban = Mean_GDP_Rural
Result: p = 0.002 (< 0.05) → Significant difference ✓
```

### Correlation Analysis

**Purpose**: Discover relationships between variables

**Pearson Correlation Coefficient**:
```
r = SUM((X - Mean_X)(Y - Mean_Y)) / SQRT(SUM((X - Mean_X)²) × SUM((Y - Mean_Y)²))

Range: -1.0 to +1.0
  r = +1.0:  Perfect positive correlation
  r = 0.0:   No correlation
  r = -1.0:  Perfect negative correlation
```

**Interpretation Guide**:
| Coefficient | Strength | Data Points |
|-------------|----------|-------------|
| 0.9 to 1.0 | Very Strong | GDP↔Infrastructure |
| 0.7 to 0.9 | Strong | Population↔Housing |
| 0.5 to 0.7 | Moderate | Density↔Unemployment |
| 0.3 to 0.5 | Weak | - |
| 0.0 to 0.3 | Very Weak | - |

---

## 2. Growth Analysis

### Compound Annual Growth Rate (CAGR)

**Formula**:
```
CAGR = ((End Value / Beginning Value)^(1/Years)) - 1
```

**Key Points**:
- Smooths volatility over multiple years
- Assumes consistent geometric growth
- Standard metric for long-term trends

**Example**:
```
Population 2015: 100,000
Population 2023: 135,000
Years: 8

CAGR = ((135,000 / 100,000)^(1/8)) - 1
     = (1.35)^0.125 - 1
     = 1.0387 - 1
     = 0.0387 or 3.87% annually
```

### Absolute Change
```
Absolute_Change = End Value - Beginning Value
Percent_Change = (Absolute_Change / Beginning Value) × 100
```

---

## 3. Distribution Analysis

### Normality Assessment

**Shapiro-Wilk Test** (for n < 5000):
- Tests if data follows normal (bell curve) distribution
- p-value < 0.05 → Data is NOT normally distributed
- p-value ≥ 0.05 → Data MAY be normally distributed

### Distribution Characteristics

**Skewness**:
```
Skewness = E[(X - Mean)³] / SD³

Interpretation:
  > 0 (right-skewed):  Tail extends right, most values left
  = 0 (symmetric):     Perfectly balanced (ideal)
  < 0 (left-skewed):   Tail extends left, most values right
```

**Kurtosis**:
```
Kurtosis = E[(X - Mean)⁴] / SD⁴ - 3

Interpretation:
  > 0 (leptokurtic):   Heavy tails, more outliers
  = 0 (mesokurtic):    Normal distribution tails
  < 0 (platykurtic):   Light tails, fewer outliers
```

---

## 4. Time Series Decomposition

**Purpose**: Separate underlying patterns in temporal data

**Components**:
```
Time Series (Y) = Trend (T) + Seasonal (S) + Residual (R)

Trend:      Long-term direction
Seasonal:   Repeating patterns (yearly cycles)
Residual:   Random fluctuations
```

**Coefficient of Variation**:
```
CV = Standard Deviation / Mean

High CV (>0.5) = High volatility, inconsistent
Low CV (<0.2)  = Stable, predictable
```

---

## 5. Predictive Modeling

### Linear Regression

**Formula**:
```
ŷ = b₀ + b₁x

where:
  ŷ = predicted value
  b₀ = intercept (starting point)
  b₁ = slope (rate of change)
  x = predictor variable (e.g., year)
```

**Model Fit Evaluation**:

**R² Score** (Coefficient of Determination):
```
R² = 1 - (SS_residual / SS_total)

Range: 0 to 1
  0.9-1.0: Excellent fit (90%+ variance explained)
  0.7-0.9: Good fit
  0.5-0.7: Acceptable fit
  <0.5:    Poor fit, model needs improvement
```

**Mean Absolute Error (MAE)**:
```
MAE = SUM(|Actual - Predicted|) / n

Units: Same as predicted variable
Interpretation: Average prediction error in units
```

**Root Mean Squared Error (RMSE)**:
```
RMSE = SQRT(SUM((Actual - Predicted)²) / n)

Penalizes larger errors more heavily than MAE
Better for assessing worst-case predictions
```

**Example**:
```
Predicting next year's population:
Model: ŷ = 50,000 + 2,500 × year
R² = 0.92 → Model explains 92% of population variance
MAE = 1,200 → Average prediction error ±1,200 people
```

### Random Forest Regression

**Concept**: Ensemble of decision trees voting on predictions

**Advantages**:
- Captures non-linear relationships
- Handles multiple features naturally
- Less prone to overfitting than single tree

**Key Parameters**:
- `n_estimators`: Number of trees (100+)
- `max_depth`: Tree depth limit (prevents overfitting)
- `test_size`: Training/test split ratio (80/20)

**Feature Importance**:
```
For each feature:
  Importance = SUM(decrease in impurity when feature is used)
  Normalized to sum to 1.0
  
Higher importance → Feature more influential in predictions
```

---

## 6. Scenario Analysis

**Purpose**: Model potential futures under different assumptions

**Methodology**:
```
For each scenario S with growth rate G:

Year 0 (Current): Value₀
Year 1: Value₁ = Value₀ × (1 + G)
Year 2: Value₂ = Value₁ × (1 + G) = Value₀ × (1 + G)²
Year N: ValueN = Value₀ × (1 + G)^N
```

**Standard Scenarios**:
| Scenario | Growth Rate | Justification |
|----------|---|---|
| Pessimistic | -2% | Economic contraction, loss of investment |
| Base Case | +3% | Historical average growth |
| Optimistic | +6% | Policy success, increased investment |

**Example - Housing Prices**:
```
Current price: 100,000 DH/sqm

Pessimistic (-3%):
  Year 5: 100,000 × (0.97)^5 = 85,873 DH/sqm

Base Case (+2%):
  Year 5: 100,000 × (1.02)^5 = 110,408 DH/sqm

Optimistic (+5%):
  Year 5: 100,000 × (1.05)^5 = 127,628 DH/sqm
```

---

## 7. Data Quality Validation

### Outlier Detection

**IQR Method** (Interquartile Range):
```
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1

Lower Limit = Q1 - 1.5 × IQR
Upper Limit = Q3 + 1.5 × IQR

Outliers: Values outside [Lower, Upper] range
```

**Z-Score Method**:
```
Z-Score = (X - Mean) / Standard Deviation

Threshold: |Z| > 3.0
  |Z| > 3.0: Extreme outlier (0.3% expected in normal data)
  |Z| > 2.0: Outlier (5% expected)
```

### Data Completeness

**Null Ratio**:
```
Null_Ratio = COUNT(NULL values) / COUNT(total values)

Acceptable: < 5%
Concerning: 5-10%
Critical: > 10%
```

---

## 8. Key Performance Indicators (KPIs) Definitions

### Urbanization Rate
```
Urbanization_Rate = (Urban Population / Total Population)

Calculation:
  Urban = Classified as "Metropolitan" or "Urban"
  Rural = Classified as "Rural" or "Peri-urban"
  
Range: 0-1 (0% to 100%)
```

### Housing Need Index
```
Housing_Need = Population / Housing Units

Interpretation:
  < 1: Surplus housing (depopulation risk)
  1-2: Balanced market
  > 2: Housing shortage (affordability crisis)
```

### Infrastructure Score
```
Infrastructure_Score = (Water Access + Electricity Access) / 2

Range: 0-1 (0% to 100%)
Weights could be adjusted based on policy priorities
```

### Economic Efficiency
```
Efficiency = GDP Per Capita / (Unemployment Rate + 1)

Higher values indicate better economic health
Reduces impact of unemployment on assessment
```

---

## 9. Policy-Relevant Insights Calculation

### Regional Disparity Index
```
Disparity = (Max Regional Mean - Min Regional Mean) / National Mean

Range: 0-1
  < 0.2: Low disparity (equity)
  0.2-0.4: Moderate disparity
  > 0.4: High disparity (policy intervention needed)
```

### Infrastructure Investment Priority
```
Priority_Score = (Coverage_Gap * Weight) + (Maintenance_Needs * Weight)

Coverage_Gap = (100 - Current_Coverage) / 100
Maintenance_Needs = (1 - Maintenance_Score/3)

Regions ranked by Priority_Score (descending)
```

---

**Version**: 1.0  
**Last Updated**: April 2024  
**Author**: Data Engineering Team

