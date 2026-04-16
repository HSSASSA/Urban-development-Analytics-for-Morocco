# Build and Deploy Instructions

## Local Development

### Option 1: Traditional Python Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run pipeline
python run_pipeline.py

# Start dashboard
python dashboards/dashboard.py
```

### Option 2: Docker Setup

```bash
# Build image
docker build -t urban-analytics:1.0 .

# Run pipeline in container
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  urban-analytics:1.0 \
  python run_pipeline.py

# Run dashboard (expose port 8050)
docker run -d \
  -p 8050:8050 \
  -v $(pwd)/data:/app/data \
  urban-analytics:1.0 \
  python dashboards/dashboard.py
```

## Database Access

### SQLite Direct Access
```bash
sqlite3 ./data/warehouse/urban_analytics.db

# Example queries
SELECT COUNT(*) FROM urban_indicators;
SELECT region, AVG(population) as avg_pop FROM urban_indicators GROUP BY region;
```

### Python REPL
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('./data/warehouse/urban_analytics.db')
df = pd.read_sql('SELECT * FROM urban_indicators LIMIT 10', conn)
print(df)
conn.close()
```

## Performance Tuning

### Enable Query Caching
```python
# In config.yaml
caching:
  enabled: true
  ttl: 3600  # 1 hour
```

### Use Polars for Large Datasets
```python
import polars as pl

df = pl.read_csv('./data/processed/urban_indicators.csv')
# Polars is 3-10x faster than Pandas
```

## Production Deployment

### Cloud Platforms

**AWS**:
- RDS for PostgreSQL database
- Lambda for scheduled pipelines
- QuickSight for dashboards
- S3 for data storage

**Azure**:
- Azure SQL Database
- Logic Apps for scheduling
- Power BI for visualization
- Blob Storage for files

**Google Cloud**:
- Cloud SQL
- Cloud Functions for ETL
- Data Studio for dashboards
- Cloud Storage

---

**Version**: 1.0

