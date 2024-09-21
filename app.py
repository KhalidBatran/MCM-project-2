import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output  # Ensure this line is added

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
                            dbc.NavLink("Home", href="#home", active="exact"),
                            dbc.NavLink("Fig1", href="#fig1", active="exact"),
                            dbc.NavLink("Fig2", href="#fig2", active="exact"),
                            dbc.NavLink("Fig3", href="#fig3", active="exact"),
                        ], className="ms-auto", navbar=True
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

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def render_page_content(pathname):
    if pathname == "#home":
        return html.Div([html.H1('Home Page Content')])
    elif pathname == "#fig1":
        return html.Div([html.H1('Figure 1 Page Content')])
    # Continue adding elif for other pages as necessary

if __name__ == "__main__":
    app.run_server(debug=True)
