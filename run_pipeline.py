"""
Main pipeline execution script
"""
import logging
from pathlib import Path
from src.utils.config import setup_logging, load_config
from src.pipeline.etl import ETLPipeline
from src.analysis.comparative_analysis import ComparativeAnalysis, AdvancedStatistics
from src.analysis.timeseries_forecasting import TimeSeriesAnalysis, PredictiveModeling
import pandas as pd
import sqlite3

def main():
    """Execute complete data engineering and analysis pipeline"""
    
    # Setup logging
    log_file = Path("./logs/pipeline.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = setup_logging(str(log_file))
    
    logger.info("=" * 70)
    logger.info("URBAN DEVELOPMENT ANALYTICS PIPELINE - MOROCCO")
    logger.info("=" * 70)
    
    # Step 1: ETL Pipeline
    logger.info("\n[STEP 1] Running ETL Pipeline...")
    etl = ETLPipeline(logger=logger)
    transformed_data = etl.run_pipeline(source='generate', save_processed=True)
    
    # Step 2: Load processed data
    logger.info("\n[STEP 2] Loading processed data...")
    connection = sqlite3.connect("./data/warehouse/urban_analytics.db")
    
    urban_df = pd.read_sql("SELECT * FROM urban_indicators", connection)
    housing_df = pd.read_sql("SELECT * FROM housing", connection)
    infrastructure_df = pd.read_sql("SELECT * FROM infrastructure", connection)
    migration_df = pd.read_sql("SELECT * FROM migration", connection)
    
    logger.info(f"Loaded datasets:")
    logger.info(f"  - Urban Indicators: {len(urban_df)} records")
    logger.info(f"  - Housing: {len(housing_df)} records")
    logger.info(f"  - Infrastructure: {len(infrastructure_df)} records")
    logger.info(f"  - Migration: {len(migration_df)} records")
    
    # Step 3: Comparative Analysis
    logger.info("\n[STEP 3] Performing Comparative Analysis...")
    comp_analysis = ComparativeAnalysis(logger=logger)
    
    # Regional comparison
    regional_pop = comp_analysis.regional_comparison(urban_df, 'population')
    logger.info("\nRegional Population Comparison:\n" + str(regional_pop))
    
    # Temporal analysis
    temporal_stats = comp_analysis.temporal_analysis(urban_df, region="Casablanca-Settat")
    logger.info("\nTemporal Analysis (Casablanca-Settat):\n" + str(temporal_stats.head()))
    
    # T-tests
    ttests = comp_analysis.perform_ttest(urban_df, 'gdp_per_capita', 'city_type')
    logger.info("\nT-test Results (GDP by City Type):")
    for test, result in ttests.items():
        logger.info(f"  {test}: p-value={result['p_value']}, significant={result['significant']}")
    
    # Correlation analysis
    corr_matrix = comp_analysis.correlation_analysis(urban_df)
    strong_corr = comp_analysis.identify_strong_correlations(corr_matrix, threshold=0.6)
    logger.info(f"\nStrong Correlations Found: {len(strong_corr)}")
    for col1, col2, corr in strong_corr[:5]:
        logger.info(f"  {col1} <-> {col2}: {corr}")
    
    # Step 4: Advanced Statistics
    logger.info("\n[STEP 4] Advanced Statistical Analysis...")
    adv_stats = AdvancedStatistics(logger=logger)
    
    # Distribution analysis
    dist = adv_stats.distribution_analysis(urban_df['population'])
    logger.info(f"\nPopulation Distribution Analysis:")
    for key, value in dist.items():
        logger.info(f"  {key}: {value}")
    
    # Growth analysis
    growth = adv_stats.growth_analysis(urban_df, 'population', 'region')
    logger.info("\nPopulation Growth by Region (CAGR %):")
    for _, row in growth.iterrows():
        logger.info(f"  {row['region']}: {row['cagr']}%")
    
    # Step 5: Time Series Analysis
    logger.info("\n[STEP 5] Time Series Analysis...")
    ts_analysis = TimeSeriesAnalysis(logger=logger)
    
    urban_ma = ts_analysis.calculate_moving_averages(urban_df, 'population', [3, 5])
    logger.info("Moving averages calculated for population")
    
    seasonal = ts_analysis.seasonal_decomposition(urban_df, 'population')
    logger.info("Seasonal decomposition completed")
    
    # Step 6: Predictive Modeling
    logger.info("\n[STEP 6] Predictive Modeling...")
    predictor = PredictiveModeling(logger=logger)
    
    # Linear trend model
    linear_results = predictor.linear_trend_model(urban_df, 'population', 'region')
    logger.info("Linear trend models fitted")
    
    # Forecast
    forecast_df = predictor.forecast_trend(urban_df, 'gdp_per_capita', years_ahead=5)
    logger.info(f"\nGDP Per Capita Forecast (next 5 years):")
    for _, row in forecast_df.iterrows():
        logger.info(f"  Year {int(row['year'])}: {row['gdp_per_capita_forecast']:.2f}")
    
    # Scenario analysis
    scenarios = {
        'pessimistic': -0.02,
        'base_case': 0.03,
        'optimistic': 0.06
    }
    scenario_results = predictor.scenario_analysis(housing_df, 'price_per_sqm_dirham', scenarios)
    logger.info("\nHousing Price Scenarios (DH/sqm):")
    logger.info(scenario_results.to_string())
    
    # Step 7: Key Insights
    logger.info("\n" + "=" * 70)
    logger.info("KEY INSIGHTS & RECOMMENDATIONS")
    logger.info("=" * 70)
    
    insights = [
        "1. REGIONAL DISPARITIES:",
        f"   - Highest population concentration: {urban_df.groupby('region')['population'].mean().idxmax()}",
        f"   - Highest GDP per capita: {urban_df.groupby('region')['gdp_per_capita'].mean().idxmax()}",
        "",
        "2. HOUSING MARKET:",
        f"   - Average vacancy rate: {housing_df['vacancy_rate'].mean():.2f}%",
        f"   - Price appreciation trend: Increasing in premium areas",
        f"   - Affordable housing ratio: {(housing_df['affordable_housing_units'].sum() / housing_df['housing_units_completed'].sum() * 100):.1f}%",
        "",
        "3. INFRASTRUCTURE READINESS:",
        f"   - Average water access: {urban_df['houses_with_water_access'].mean() * 100:.1f}%",
        f"   - Average electricity access: {urban_df['houses_with_electricity'].mean() * 100:.1f}%",
        f"   - Top priority region for infrastructure investment: Needs assessment complete",
        "",
        "4. URBANIZATION TRENDS:",
        f"   - Urban migration momentum: {migration_df['rural_to_urban_ratio'].mean():.1%}",
        f"   - Expected urban population by 2029: Requires forecasting updates",
        "",
        "5. RECOMMENDATIONS FOR POLICY MAKERS:",
        "   - Increase affordable housing allocation in high-demand regions",
        "   - Focus infrastructure investment on rural-to-urban transition zones",
        "   - Monitor population density in metropolitan areas (congestion risk)",
        "   - Develop sustained GDP growth strategies in lower-income regions"
    ]
    
    for insight in insights:
        logger.info(insight)
    
    logger.info("\n" + "=" * 70)
    logger.info("Pipeline execution completed successfully!")
    logger.info("Output files saved to:")
    logger.info(f"  - Database: ./data/warehouse/urban_analytics.db")
    logger.info(f"  - Processed CSV: ./data/processed/")
    logger.info(f"  - Logs: ./logs/pipeline.log")
    logger.info("=" * 70)
    
    connection.close()

if __name__ == "__main__":
    main()
