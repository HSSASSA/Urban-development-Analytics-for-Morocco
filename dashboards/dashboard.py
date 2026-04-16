"""
Interactive Plotly Dashboard for Urban Development Analytics
"""
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3
from pathlib import Path

# Load data
db_path = "./data/warehouse/urban_analytics.db"
if Path(db_path).exists():
    connection = sqlite3.connect(db_path)
    urban_df = pd.read_sql("SELECT * FROM urban_indicators", connection)
    housing_df = pd.read_sql("SELECT * FROM housing", connection)
    infrastructure_df = pd.read_sql("SELECT * FROM infrastructure", connection)
    migration_df = pd.read_sql("SELECT * FROM migration", connection)
    connection.close()
else:
    urban_df = pd.DataFrame()
    housing_df = pd.DataFrame()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Urban Development Analytics - Morocco"

# Define colors
colors = {
    'background': "#235D71",
    'text': '#0f3460',
    'primary': '#16213e',
    'secondary': "#e44d66"
}

# App layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1("Urban Development Analytics Dashboard - Morocco", 
            style={'textAlign': 'center', 'color': 'white', 'marginBottom': 30, 'marginTop': 20}),
    
    html.Div([
        html.Div([
            html.Label("Select Region:", style={'color': 'white', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': 'All Regions', 'value': 'ALL'}] + 
                        [{'label': region, 'value': region} for region in urban_df['region'].unique()],
                value='ALL',
                style={'width': '100%'}
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.Label("Select Year Range:", style={'color': 'white', 'fontWeight': 'bold'}),
            dcc.RangeSlider(
                id='year-slider',
                min=int(urban_df['year'].min()),
                max=int(urban_df['year'].max()),
                value=[int(urban_df['year'].min()), int(urban_df['year'].max())],
                marks={str(year): str(year) for year in range(int(urban_df['year'].min()), int(urban_df['year'].max()) + 1)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ], style={'width': '65%', 'display': 'inline-block'}),
    ], style={'marginBottom': 30, 'padding': 20, 'backgroundColor': colors['primary'], 'borderRadius': 10}),
    
    # KPI Cards
    html.Div([
        html.Div([
            html.H3("Average Population", style={'color': 'white'}),
            html.P(id='avg-population', style={'color': colors['secondary'], 'fontSize': 24, 'fontWeight': 'bold'})
        ], style={'flex': '1', 'backgroundColor': colors['primary'], 'padding': 20, 'borderRadius': 10, 'margin': 10}),
        
        html.Div([
            html.H3("Avg Urban Density", style={'color': 'white'}),
            html.P(id='avg-density', style={'color': colors['secondary'], 'fontSize': 24, 'fontWeight': 'bold'})
        ], style={'flex': '1', 'backgroundColor': colors['primary'], 'padding': 20, 'borderRadius': 10, 'margin': 10}),
        
        html.Div([
            html.H3("Water Access %", style={'color': 'white'}),
            html.P(id='water-access', style={'color': colors['secondary'], 'fontSize': 24, 'fontWeight': 'bold'})
        ], style={'flex': '1', 'backgroundColor': colors['primary'], 'padding': 20, 'borderRadius': 10, 'margin': 10}),
        
        html.Div([
            html.H3("Avg Unemployment %", style={'color': 'white'}),
            html.P(id='unemployment', style={'color': colors['secondary'], 'fontSize': 24, 'fontWeight': 'bold'})
        ], style={'flex': '1', 'backgroundColor': colors['primary'], 'padding': 20, 'borderRadius': 10, 'margin': 10}),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': 30}),
    
    # Charts Row 1
    html.Div([
        html.Div([
            dcc.Graph(id='population-trend')
        ], style={'width': '49%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            dcc.Graph(id='gdp-distribution')
        ], style={'width': '49%', 'display': 'inline-block'}),
    ]),
    
    # Charts Row 2
    html.Div([
        html.Div([
            dcc.Graph(id='housing-market')
        ], style={'width': '49%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            dcc.Graph(id='infrastructure-status')
        ], style={'width': '49%', 'display': 'inline-block'}),
    ]),
    
    # Charts Row 3
    html.Div([
        html.Div([
            dcc.Graph(id='migration-patterns')
        ], style={'width': '49%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            dcc.Graph(id='regional-comparison')
        ], style={'width': '49%', 'display': 'inline-block'}),
    ]),
    
])

# Callbacks for KPI updates
@app.callback(
    [Output('avg-population', 'children'),
     Output('avg-density', 'children'),
     Output('water-access', 'children'),
     Output('unemployment', 'children')],
    [Input('region-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_kpis(selected_region, year_range):
    filtered_df = urban_df.copy()
    
    if selected_region != 'ALL':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
    
    avg_pop = f"{filtered_df['population'].mean():,.0f}"
    avg_density = f"{filtered_df['population_density'].mean():,.0f}"
    water = f"{filtered_df['houses_with_water_access'].mean() * 100:.1f}%"
    unemp = f"{filtered_df['unemployment_rate'].mean():.1f}%"
    
    return avg_pop, avg_density, water, unemp

# Callbacks for charts
@app.callback(
    Output('population-trend', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_population_chart(selected_region, year_range):
    filtered_df = urban_df.copy()
    
    if selected_region != 'ALL':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
    
    grouped = filtered_df.groupby('year')['population'].mean().reset_index()
    
    fig = px.line(grouped, x='year', y='population', 
                  title='Population Trend Over Time',
                  labels={'population': 'Population', 'year': 'Year'})
    fig.update_layout(template='plotly_dark')
    
    return fig

@app.callback(
    Output('gdp-distribution', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_gdp_chart(selected_region, year_range):
    filtered_df = urban_df.copy()
    
    if selected_region != 'ALL':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
    
    fig = px.box(filtered_df, y='gdp_per_capita', x='city_type',
                 title='GDP Per Capita Distribution by City Type',
                 labels={'gdp_per_capita': 'GDP Per Capita (DH)', 'city_type': 'City Type'})
    fig.update_layout(template='plotly_dark')
    
    return fig

@app.callback(
    Output('housing-market', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_housing_chart(selected_region, year_range):
    if housing_df.empty:
        return {}
    
    filtered_df = housing_df.copy()
    filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
    
    grouped = filtered_df.groupby('year')[['housing_units_completed', 'affordable_housing_units']].sum().reset_index()
    
    fig = px.bar(grouped, x='year', y=['housing_units_completed', 'affordable_housing_units'],
                 title='Housing Units Completed vs Affordable',
                 labels={'value': 'Units', 'year': 'Year'},
                 barmode='group')
    fig.update_layout(template='plotly_dark')
    
    return fig

@app.callback(
    Output('infrastructure-status', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_infrastructure_chart(selected_region, year_range):
    if infrastructure_df.empty:
        return {}
    
    filtered_df = infrastructure_df.copy()
    filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
    
    service_summary = filtered_df.groupby('service_type')['coverage_rate'].mean().reset_index()
    
    fig = px.bar(service_summary, x='service_type', y='coverage_rate',
                 title='Average Infrastructure Coverage by Service Type',
                 labels={'coverage_rate': 'Coverage Rate (%)', 'service_type': 'Service Type'})
    fig.update_layout(template='plotly_dark')
    
    return fig

@app.callback(
    Output('migration-patterns', 'figure'),
    [Input('year-slider', 'value')]
)
def update_migration_chart(year_range):
    if migration_df.empty:
        return {}
    
    filtered_df = migration_df.copy()
    filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
    
    migration_summary = filtered_df[['origin_region', 'destination_region', 'migrants_count']].groupby(
        ['origin_region', 'destination_region']).sum().reset_index()
    
    fig = px.sunburst(migration_summary, 
                      path=['origin_region', 'destination_region'],
                      values='migrants_count',
                      title='Internal Migration Flows')
    fig.update_layout(template='plotly_dark')
    
    return fig

@app.callback(
    Output('regional-comparison', 'figure'),
    [Input('year-slider', 'value')]
)
def update_regional_comparison(year_range):
    filtered_df = urban_df.copy()
    filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
    
    regional_stats = filtered_df.groupby('region').agg({
        'population': 'mean',
        'gdp_per_capita': 'mean',
        'unemployment_rate': 'mean'
    }).reset_index()
    
    fig = px.scatter(regional_stats, x='gdp_per_capita', y='population', 
                     size='unemployment_rate', hover_name='region',
                     title='Regional Comparison: GDP vs Population vs Unemployment',
                     labels={'gdp_per_capita': 'GDP Per Capita (DH)', 'population': 'Population'})
    fig.update_layout(template='plotly_dark')
    
    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8050)
