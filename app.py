import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Load the dataset from the GitHub raw link
data_url = "https://raw.githubusercontent.com/KhalidBatran/MCM-project-2/refs/heads/main/assets/crime_district.csv"
df = pd.read_csv(data_url)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Crime Data Dashboard"), width=12)
    ]),
    
    # Checkboxes for Assault and Property
    dbc.Row([
        dbc.Col([
            html.Label("Filter by Crime Category"),
            dcc.Checklist(
                id='category-filter',
                options=[
                    {'label': 'Assault', 'value': 'Assault'},
                    {'label': 'Property', 'value': 'Property'}
                ],
                value=['Assault', 'Property'],  # Default to both selected
                inline=True
            )
        ], width=6),
    ]),
    
    # Sunburst chart will be displayed here
    dbc.Row([
        dbc.Col(dcc.Graph(id='sunburst-chart'), width=12)
    ])
])

# Callback to update the chart based on the selected crime categories
@app.callback(
    Output('sunburst-chart', 'figure'),
    Input('category-filter', 'value')
)
def update_chart(selected_categories):
    # Filter the dataframe based on selected categories
    filtered_df = df[df['Crime Category'].isin(selected_categories)]
    
    # Create the sunburst chart
    fig = px.sunburst(filtered_df, path=['State', 'Crime Category'], values='Reported Crimes',
                      color='Reported Crimes', hover_data=['Crime Type'],
                      title="Crime Distribution by State and Category")
    
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
