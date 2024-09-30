import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import json
import requests

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/KhalidBatran/MCM-project-2/refs/heads/main/assets/crime_district.csv')

# Directly convert the 'Incident Date' to the 'Year' without date parsing, since it's already in year format
df['Year'] = pd.to_numeric(df['Incident Date'], errors='coerce')

# Ensure all states are included even if they are missing data for some categories
states = df['State'].unique()
categories = df['Crime Category'].unique()
years = df['Year'].unique()

# Create a new dataframe that ensures all combinations of states, categories, and years exist
full_df = pd.MultiIndex.from_product([states, categories, years], names=['State', 'Crime Category', 'Year']).to_frame(index=False)
df = pd.merge(full_df, df, on=['State', 'Crime Category', 'Year'], how='left').fillna(0)

# Load Malaysia geoJSON file
geojson_url = "https://raw.githubusercontent.com/KhalidBatran/MCM-project-2/refs/heads/main/assets/malaysia_state.geojson"
states_json = requests.get(geojson_url).json()

# Function to create the first choropleth map
def create_map(selected_state=None):
    df_grouped = df.groupby('State', as_index=False)['Reported Crimes'].sum()
    min_crimes = df_grouped['Reported Crimes'].min()
    max_crimes = df_grouped['Reported Crimes'].max()

    if selected_state and selected_state != "All":
        df_filtered = df[df['State'] == selected_state]
        df_grouped_filtered = df_filtered.groupby('State', as_index=False)['Reported Crimes'].sum()
        fig = px.choropleth(df_grouped_filtered, geojson=states_json, locations="State", color="Reported Crimes",
                            featureidkey="properties.name", template='plotly_white',
                            range_color=[min_crimes, max_crimes])
    else:
        fig = px.choropleth(df_grouped, geojson=states_json, locations="State", color="Reported Crimes",
                            featureidkey="properties.name", template='plotly_white',
                            range_color=[min_crimes, max_crimes])

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")

    return fig

# Function to create the scatter plot with animation
def create_scatter_plot():
    fig = px.scatter(df, x='Reported Crimes', y='State', animation_frame='Year', animation_group='State',
                     size='Reported Crimes', color='Crime Category', hover_name='State', facet_col='Crime Category',
                     log_x=False, size_max=45)

    # Custom layout settings for the scatter plot with gridlines
    fig.update_layout(
        xaxis=dict(showgrid=True, gridcolor='lightgray'),  # Enable and set gridline color for x-axis
        yaxis=dict(showgrid=True, gridcolor='lightgray'),  # Enable and set gridline color for y-axis
        xaxis_title='Reported Crimes',  # Label for x-axis
        yaxis_title='State',  # Label for y-axis
        plot_bgcolor="rgba(0, 0, 0, 0)",  # Transparent background
        paper_bgcolor="rgba(0, 0, 0, 0)",  # Transparent background for paper
        margin=dict(l=0, r=0, t=0, b=0)   # Adjust the margins to reduce whitespace
    )
    
    # Apply the same gridline settings to both facets (left and right sides)
    fig.update_xaxes(showgrid=True, gridcolor='lightgray', matches='x')
    fig.update_yaxes(showgrid=True, gridcolor='lightgray', matches='y')

    return fig

# Layout of the app
app.layout = dbc.Container([
    # Section for the description of the data
    dbc.Row([
        dbc.Col([
            html.H2("Crime Data Overview"),
            html.P("""
                This dataset contains information about reported crimes across various states in Malaysia. 
                The data includes the number of reported crimes by category (e.g., Assault, Property) for each state. 
                The visualizations below will help explore the geographical distribution of crimes and identify states 
                with higher crime rates.
            """),
            html.P("""
                By selecting a state from the dropdown below, you can filter the map to display crime data specific 
                to that region, or you can view the overall crime distribution across the entire country.
            """)
        ], width=12)
    ]),

    # Dropdown filter for selecting states for Figure 1 (choropleth map)
    dbc.Row([
        dbc.Col([
            html.Label("Select State:"),
            dcc.Dropdown(
                id='state-dropdown',
                options=[{'label': 'All', 'value': 'All'}] + 
                        [{'label': state, 'value': state} for state in df['State'].unique()],
                value='All',  # Default value is 'All'
                clearable=False
            )
        ], width=4),
    ]),

    # Choropleth map (Figure 1) to be rendered here
    dbc.Row([    
        dbc.Col(dcc.Graph(id='choropleth-map'), width=12)
    ]),

    # Add a separator line between Figure 1 and Figure 2
    html.Hr(),

    # Section for Figure 2 (scatter plot with animation)
    dbc.Row([
        dbc.Col(html.H2("Crime Trends Over Time"), width=12)
    ]),
    
    # Scatter plot (Figure 2) to be rendered here
    dbc.Row([
        dbc.Col(dcc.Graph(id='scatter-plot'), width=12)
    ])
])

# Callback to update the choropleth map based on the selected state
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('state-dropdown', 'value')]
)
def update_map(selected_state):
    # Update the map based on the selected state
    return create_map(selected_state)

# Callback to display the scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('scatter-plot', 'id')  # Just a placeholder input to trigger the callback
)
def update_scatter_plot(_):
    # Update the scatter plot
    return create_scatter_plot()

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
