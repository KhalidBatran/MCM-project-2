import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

# Initialize Dash app with external Bootstrap CSS
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# IMPORTANT: Define server to expose for Gunicorn
server = app.server

# Define your app layout and callbacks below this
# Example Layout
app.layout = html.Div([
    dbc.NavbarSimple(
        brand="Example App",
        brand_href="/",
        color="primary",
        dark=True,
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Page 1", href="/page-1")),
        ]
    ),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Example callback to handle page routing
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/page-1':
        return html.Div([
            html.H1('Page 1')
        ])
    else:
        return html.Div([
            html.H1('Home Page')
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
