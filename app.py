from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-project-2/refs/heads/main/assets/crime_district.csv")

if __name__ == "__main__":
    app.run_server(debug=True)
