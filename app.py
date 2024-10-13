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
df = pd.read_csv('https://raw.githubusercontent.com/KhalidBatran/MCM-project-2/refs/heads/main/assets/Cleaned%20Animal%20Shelter%20Data.csv')

if __name__ == '__main__':
    app.run(debug=True)
