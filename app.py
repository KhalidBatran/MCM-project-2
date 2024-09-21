import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px

server = app.server

df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-Final-Project/main/assets/Olympics%202024.csv")
