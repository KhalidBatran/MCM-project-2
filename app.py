import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px

# Initialize the Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the path to your dataset
data_path = "/assets/lfs_year.csv"

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-project-2/main/assets/lfs_year.csv")

# Define the logo (assuming you have a relative path to the logo image in your assets folder)
logo = "/assets/MMU_Logo.png"  # Change the path to your actual logo path

# Define the navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(html.Img(src=logo, height="30px"), width="auto"),
                    dbc.Col(dbc.NavbarBrand("OpenDOSM", className="ms-2"), width="auto"),
                    dbc.Nav(
                        [
                            dbc.NavLink("Home", href="#", active="exact"),
                            dbc.NavLink("Fig1", href="#", active="exact"),
                            dbc.NavLink("Fig2", href="#", active="exact"),
                            dbc.NavLink("Fig3", href="#", active="exact"),
                        ], className="ms-auto", navbar=True
                    ),
                    dbc.Col(
                        [
                            dbc.Button("Light", color="primary", className="me-1", id="btn-light"),
                            dbc.Button("Dark", color="secondary", id="btn-dark"),
                        ],
                        width="auto"
                    ),
                ],
                align="center",
                className="g-0",
            ),
        ],
        fluid=True,
    ),
    color="dark",
    dark=True,
)

# Define the layout of your app
app.layout = html.Div([
    navbar,
    # Placeholder for page content
    html.Div(id='page-content', children=[])
])

# Callback to switch themes
@app.callback(
    Output('page-content', 'children'),
    [Input('btn-light', 'n_clicks'), Input('btn-dark', 'n_clicks')]
)
def switch_theme(btn_light, btn_dark):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-light' in changed_id:
        return html.Div("Light theme content")
    elif 'btn-dark' in changed_id:
        return html.Div("Dark theme content")

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
