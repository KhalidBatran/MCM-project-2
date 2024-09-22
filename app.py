import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Navbar(
        dbc.Container(
            [
                html.A(html.Img(src="assets/MMU_Logo.png", height="40px"), href="/home", className="navbar-brand"),
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Home", href="/home", className="nav-link", id="nav-home")),
                        dbc.NavItem(dbc.NavLink("Fig1", href="/fig1", className="nav-link", id="nav-fig1")),
                        dbc.NavItem(dbc.NavLink("Fig2", href="/fig2", className="nav-link", id="nav-fig2")),
                        dbc.NavItem(dbc.NavLink("Fig3", href="/fig3", className="nav-link", id="nav-fig3")),
                    ],
                    className="ms-auto",  # Right alignment
                    navbar=True
                ),
            ],
            fluid=True,
        ),
        color="light",
        dark=False,
        className="mb-5"
    ),
    html.Div(id='page-content', style={'position': 'absolute', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)'})  # Central content
])

@app.callback(
    [Output('nav-home', 'className'),
     Output('nav-fig1', 'className'),
     Output('nav-fig2', 'className'),
     Output('nav-fig3', 'className')],
    [Input('url', 'pathname')]
)
def update_nav_active(pathname):
    base_class = 'nav-link'
    active_class = 'nav-link active'
    links = [base_class] * 4  # Default to all links not active
    if pathname == '/home':
        links[0] = active_class
    elif pathname == '/fig1':
        links[1] = active_class
    elif pathname == '/fig2':
        links[2] = active_class
    elif pathname == '/fig3':
        links[3] = active_class
    return links

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def render_page_content(pathname):
    if pathname == "/home":
        return html.Div([
            html.H1("Annual Principal Labour Force Statistics", className="text-center"),
            html.P(
                "This project uses Python to create clear and interactive charts that show important information about jobs and unemployment each year. We take complex data and make it easy to understand and explore, helping people see how many people are working, how many are looking for jobs, and the trends over time. This makes it easier for everyone to understand what's happening in the job market.",
                className="text-center"
            ),
            dbc.Button("Let's Start", color="primary", href="/fig1", className="mt-4")
        ])
    elif pathname == "/fig1":
        return html.H3("Fig1 Content", className="text-center")
    elif pathname == "/fig2":
        return html.H3("Fig2 Content", className="text-center")
    elif pathname == "/fig3":
        return html.H3("Fig3 Content", className="text-center")
    else:
        return "404 Page Not Found"  # Handling undefined routes

if __name__ == "__main__":
    app.run_server(debug=True)
