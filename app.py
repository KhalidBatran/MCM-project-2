import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

logo = "assets/MMU_Logo.png"

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(html.Img(src=logo, height="30px"), width="auto", style={"paddingLeft": "20px"}),  # Add padding
                    dbc.Col(
                        dbc.Nav(
                            [
                                dbc.NavLink("Home", href="#home", className="nav-link"),
                                dbc.NavLink("Fig1", href="#fig1", className="nav-link"),
                                dbc.NavLink("Fig2", href="#fig2", className="nav-link"),
                                dbc.NavLink("Fig3", href="#fig3", className="nav-link"),
                            ],
                            className="ms-2", navbar=True
                        ),
                        width="auto"
                    ),
                ],
                align="center",
                className="g-0"
            ),
        ],
        fluid=True,
    ),
    color="dark",
    dark=True,
    style={"fontSize": "16px", "fontFamily": "Arial, sans-serif"}  # Adjust the font here
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

# Custom CSS for active nav elements
app.clientside_callback(
    """
    function(href) {
        const links = document.querySelectorAll('.nav-link');
        links.forEach(link => {
            if (link.href === window.location.href) {
                link.style.backgroundColor = '#404040';  // Adjusted grey color
                link.style.borderRadius = '15px';
                link.style.color = 'white';
                link.style.padding = '5px 10px';
            } else {
                link.style.backgroundColor = '';
                link.style.color = 'white';
                link.style.borderRadius = '';
                link.style.padding = '';
            }
        });
    }
    """,
    Output('url', 'data-dummy'),  # Output does not matter as we don't use it
    [Input('url', 'href')]
)

if __name__ == "__main__":
    app.run_server(debug=True)
