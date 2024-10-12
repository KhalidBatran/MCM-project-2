import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP]) 
server = app.server

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/KhalidBatran/MCM-project-2/refs/heads/main/assets/top10s_spotify.csv')

# Ensure there are no missing years in the dataset (fill missing years with 0 popularity for line chart)
all_years = pd.DataFrame({'year': range(df['year'].min(), df['year'].max() + 1)})

# Layout of the app
app.layout = dbc.Container([
    # Header for the app
    dbc.Row([
        dbc.Col(html.H1("Spotify Data Visualizations", className="text-center")),
    ]),

    # Conclusion under the title
    dbc.Row([
        dbc.Col(html.Div([
            html.P("This interactive Spotify data visualization app provides insights into song popularity trends across various genres and artists. The scatter plot explores the relationship between song length and popularity, while the line chart highlights artist popularity over time, with the ability to filter by individual artists. The bar chart compares average popularity by genre, and users can hover to see detailed popularity trends over the years. Overall, the app offers a dynamic, engaging way to explore music trends, enabling users to easily analyze relationships between song features, genres, and artists.")
        ]), width=12)
    ]),

    # Scatter plot: Song Length vs Popularity
    dbc.Row([
        dbc.Col(html.H3("Song Length vs Popularity Scatter Plot", className="text-center")),
    ]),

    dbc.Row([
        dbc.Col(
            dcc.RangeSlider(
                id='length-slider',
                min=df['length'].min(),
                max=df['length'].max(),
                value=[df['length'].min(), df['length'].max()],
                marks={int(df['length'].min()): str(int(df['length'].min())) + 's',
                       int(df['length'].max()): str(int(df['length'].max())) + 's'},
                tooltip={"placement": "bottom", "always_visible": True},
            ),
            width=12
        ),
    ], style={"padding": "20px"}),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id='length-popularity-scatter', config={'displayModeBar': False}),
            width=12
        ),
    ]),

    # Add a horizontal line here
    html.Hr(style={"border": "2px solid #ddd"}),

    # Line chart: Artist Popularity Over Time
    dbc.Row([
        dbc.Col(html.H3("Artist Popularity Trend Over the Years", className="text-center")),
    ]),

    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='artist-dropdown',
                options=[{'label': 'All', 'value': 'All'}] + 
                        [{'label': artist, 'value': artist} for artist in sorted(df['artist'].unique())],
                value='All',  # Default value is 'All'
                clearable=False,
                style={
                    'width': '50%',
                    'margin': 'auto',
                    'textAlign': 'center'
                }
            ),
            width=12,
            className="d-flex justify-content-center"
        ),
    ], className="mb-4"),  # Add margin at the bottom

    dbc.Row([
        dbc.Col(
            dcc.Graph(id='popularity-line-chart', config={'displayModeBar': False}),
            width=12
        ),
    ]),

    # Add another horizontal line here
    html.Hr(style={"border": "2px solid #ddd"}),

    # New Bar Chart for Genre Popularity
    dbc.Row([
        dbc.Col(html.H3("Average Popularity by Genre", className="text-center")),
    ]),

    dbc.Row([
        dbc.Col(
            dcc.RangeSlider(
                id='year-slider',
                min=df['year'].min(),
                max=df['year'].max(),
                value=[df['year'].min(), df['year'].max()],
                marks={int(year): str(int(year)) for year in df['year'].unique()},
                step=None,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            width=12
        ),
    ], style={"padding": "20px"}),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id='genre-popularity-bar', config={'displayModeBar': False}),
            width=6
        ),
        dbc.Col(
            dcc.Graph(id='hover-detail-trend', config={'displayModeBar': False}),
            width=6
        ),
    ]),
])

# Callback to update the scatter plot based on the slider
@app.callback(
    Output('length-popularity-scatter', 'figure'),
    [Input('length-slider', 'value')]
)
def update_scatter_plot(length_range):
    # Filter the data based on the selected length range
    filtered_df = df[(df['length'] >= length_range[0]) & (df['length'] <= length_range[1])]
    
    # Create the scatter plot
    fig = px.scatter(filtered_df, 
                     x='length', 
                     y='popularity', 
                     color='top_genre',  # Coloring by genre
                     title='Song Length vs Popularity',
                     labels={'length': 'Song Length (seconds)', 'popularity': 'Popularity'},
                     hover_name='title',
                     hover_data=['artist', 'year', 'top_genre'])

    fig.update_layout(legend_title_text='Genre')
    
    return fig

# Callback to update the line chart based on the dropdown selection
@app.callback(
    Output('popularity-line-chart', 'figure'),
    [Input('artist-dropdown', 'value')]
)
def update_line_chart(selected_artist):
    if selected_artist == 'All':
        filtered_df = df.groupby('year').agg({'popularity': 'mean'}).reset_index()
        title = "Average Popularity of All Songs Over the Years"
    else:
        artist_df = df[df['artist'] == selected_artist]
        # Merge to ensure all years are present, filling missing years with zero
        filtered_df = pd.merge(all_years, artist_df.groupby('year').agg({'popularity': 'mean'}).reset_index(), on='year', how='left').fillna(0)
        title = f"Average Popularity of {selected_artist} Over the Years"
    
    # Create the line chart with markers for individual points
    fig = px.line(filtered_df, 
                  x='year', 
                  y='popularity', 
                  title=title,
                  labels={'year': 'Year', 'popularity': 'Average Popularity'},
                  markers=True)  # Add markers to highlight points

    return fig

# Callback for the bar chart and hover trend
@app.callback(
    [Output('genre-popularity-bar', 'figure'),
     Output('hover-detail-trend', 'figure')],
    [Input('year-slider', 'value'),
     Input('genre-popularity-bar', 'hoverData')]
)
def update_charts(year_range, hover_data):
    # Filter data by selected year range
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    # Aggregate the average popularity by genre for the selected years
    genre_popularity = filtered_df.groupby('top_genre')['popularity'].mean().reset_index()
    
    # Create the bar chart
    bar_fig = px.bar(genre_popularity, 
                     x='top_genre', 
                     y='popularity', 
                     title="Average Popularity by Genre",
                     labels={'top_genre': 'Genre', 'popularity': 'Average Popularity'})

    # Highlight the genre on hover (if any)
    if hover_data is not None:
        genre_hovered = hover_data['points'][0]['x']
        bar_fig.update_traces(marker_color=['red' if g == genre_hovered else '#636efa' for g in genre_popularity['top_genre']])
    else:
        genre_hovered = None

    # Handle hover detail trend
    if genre_hovered:
        # Filter data for the hovered genre and selected year range
        genre_trend = filtered_df[filtered_df['top_genre'] == genre_hovered].groupby('year').agg({'popularity': 'mean'}).reset_index()

        # Create a line chart showing the popularity trend for the hovered genre
        trend_fig = px.line(genre_trend, 
                            x='year', 
                            y='popularity', 
                            title=f"Popularity Trend for {genre_hovered} Over the Years",
                            labels={'year': 'Year', 'popularity': 'Average Popularity'},
                            markers=True)
        
        # Ensure the chart shows even if there's data for only one year
        if len(genre_trend) == 1:
            trend_fig.update_traces(mode='markers+lines')
    else:
        # Default empty chart when no genre is hovered
        trend_fig = go.Figure()
        trend_fig.update_layout(title="Hover over a genre to see detailed trends.")

    return bar_fig, trend_fig

if __name__ == '__main__':
    app.run(debug=True)
