import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px

# Initialize the Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the path to your dataset and load it
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-project-2/main/assets/lfs_year.csv")

# Define the logo and navbar
logo = "assets/MMU_Logo.png"
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
                        ],
                        className="ms-auto", navbar=True
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
    html.Div(id='page-content', children=[])
])

# Callback for theme switching
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

# Expose the server variable for Gunicorn
server = app.server

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
