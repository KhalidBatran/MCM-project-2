import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
client_id = 'your_client_id'
client_secret = 'your_client_secret'
redirect_uri = 'https://mcm-project-2.onrender.com/callback/'  # Replace with your actual deployed app URL
scope = 'user-top-read'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Fetch the user's top tracks
results = sp.current_user_top_tracks(limit=10)

# Create a DataFrame from the top tracks data
tracks = []
for track in results['items']:
    track_data = {
        'Track Name': track['name'],
        'Artist': track['artists'][0]['name'],
        'Album': track['album']['name'],
        'Popularity': track['popularity'],
        'Track ID': track['id']
    }
    tracks.append(track_data)

df = pd.DataFrame(tracks)

# Fetch the audio features for the top tracks
track_ids = df['Track ID'].tolist()
audio_features = sp.audio_features(track_ids)

# Create a DataFrame for audio features
audio_df = pd.DataFrame(audio_features)
audio_df['Track Name'] = df['Track Name']

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Function to create a bar chart for top tracks by popularity
def create_bar_chart():
    fig = px.bar(df, x='Track Name', y='Popularity', color='Artist',
                 title='Top Tracks by Popularity', labels={'Popularity': 'Popularity'})
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_x=0.5
    )
    return fig

# Function to create a scatter plot for audio features
def create_scatter_plot():
    fig = px.scatter(audio_df, x='danceability', y='energy', size='loudness', color='tempo',
                     hover_name='Track Name', title='Audio Features of Top Tracks')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_x=0.5
    )
    return fig

# Layout for the Dash app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Spotify Music Data Overview"),
            html.P("This dashboard displays the top 10 tracks from a Spotify user, including their popularity "
                   "and audio features such as danceability, energy, and loudness."),
        ], width=12)
    ]),

    dbc.Row([    
        dbc.Col(dcc.Graph(id='bar-chart'), width=12)
    ]),

    html.Hr(),

    dbc.Row([    
        dbc.Col(dcc.Graph(id='scatter-plot'), width=12)
    ]),
])

# Callback to update the bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    Input('bar-chart', 'id')
)
def update_bar_chart(_):
    return create_bar_chart()

# Callback to update the scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('scatter-plot', 'id')
)
def update_scatter_plot(_):
    return create_scatter_plot()

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
