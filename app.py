import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/KhalidBatran/MCM-project-2/refs/heads/main/assets/top10s_spotify.csv')

# Group the data by year and genre, calculating the average popularity
df_grouped = df.groupby(['year', 'top_genre'])['popularity'].mean().reset_index()

# Get the full set of unique genres and years
all_genres = df_grouped['top_genre'].unique()
years = df_grouped['year'].unique()

# Define stable colors for each genre
color_map = {genre: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, genre in enumerate(all_genres)}

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Average Popularity by Genre Over Time"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Select Year:"),
            dcc.Slider(
                id='year-slider',
                min=years.min(),
                max=years.max(),
                value=years.min(),
                marks={int(year): str(int(year)) for year in years},
                step=None
            )
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-chart'), width=12)
    ])
])

# Callback to update bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    Input('year-slider', 'value')
)
def update_bar_chart(selected_year):
    # Filter the data for the selected year
    filtered_df = df_grouped[df_grouped['year'] == selected_year]

    # Create the bar chart with stable colors
    fig = px.bar(filtered_df, 
                 x='popularity', 
                 y='top_genre', 
                 color='top_genre',
                 color_discrete_map=color_map,
                 orientation='h',
                 title=f'Average Popularity by Genre in {selected_year}')

    # Customize the layout to keep the chart stable
    fig.update_layout(
        xaxis_title='Average Popularity',
        yaxis_title=None,  # Remove the Y-axis title
        title_x=0.5,  # Center the title
        yaxis={'categoryorder':'total ascending'},  # Keep Y-axis sorting consistent
        showlegend=True
    )
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
