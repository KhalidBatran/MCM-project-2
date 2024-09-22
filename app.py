import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# Loading the data
df = pd.read_csv("https://raw.githubusercontent.com/KhalidBatran/MCM-project-2/refs/heads/main/assets/Olympics%202024.csv")

# Prepare the data for the figures
medal_counts = df.pivot_table(index='Country Code', columns='Medal Type', values='Athlete Name', 
                              aggfunc='count', fill_value=0).reset_index()
medal_counts.columns = ['Country Code', 'Bronze Medal', 'Gold Medal', 'Silver Medal']

medal_summary = df.groupby(['Country Code', 'Medal Date'])['Medal Type'].count().reset_index(name='Total Medals')

athlete_medals = df.groupby(['Gender', 'Athlete Name', 'Medal Type']).size().reset_index(name='Count')

# Figures
def get_fig1():
    fig = px.bar(
        medal_counts, 
        x='Country Code', 
        y=['Gold Medal', 'Silver Medal', 'Bronze Medal'],
        title="Medals Distribution Across Different Countries in Olympics 2024",
        labels={"value": "Number of Medals", "variable": "Medal Type"},
        color_discrete_map={
            'Gold Medal': 'gold',
            'Silver Medal': 'silver',
            'Bronze Medal': '#cd7f32'
        },
        barmode='group'
    )
    return fig

def get_fig2():
    fig = px.scatter(
        medal_summary,
        x='Country Code',
        y='Total Medals',
        size='Total Medals',
        animation_frame='Medal Date',
        title='Medal Distribution by Country Over Time',
        labels={'Total Medals': 'Number of Medals'},
        size_max=60
    )
    return fig

def get_fig3():
    fig = px.treemap(
        athlete_medals,
        path=['Gender', 'Medal Type', 'Athlete Name'],
        values='Count',
        color='Medal Type',
        color_discrete_map={"Gold Medal": "gold", "Silver Medal": "silver", "Bronze Medal": "#cd7f32"},
        title="Medal Distribution Among Athletes Categorized by Gender"
    )
    return fig

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Navbar(
        dbc.Container(
            [
                html.A(html.Img(src="assets/MMU_Logo.png", height="25px"), href="/home", className="navbar-brand"),
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Home", href="/home", className="nav-link", id="nav-home")),
                        dbc.NavItem(dbc.NavLink("Olympics Medal Distribution", href="/fig1", className="nav-link", id="nav-fig1")),
                        dbc.NavItem(dbc.NavLink("Country Medal Trends", href="/fig2", className="nav-link", id="nav-fig2")),
                        dbc.NavItem(dbc.NavLink("Athlete Performance", href="/fig3", className="nav-link", id="nav-fig3")),
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
            html.H1("Welcome to the Olympics 2024 Dashboard", className="text-center"),
            html.P("Explore various insights into the Olympics 2024 through interactive visualizations.", className="text-center"),
            dbc.Button("Explore", color="primary", href="/fig1", className="mt-4")
        ])
    elif pathname == "/fig1":
        return html.Div(dcc.Graph(figure=get_fig1()), id='fig1-container', className='figure1')  # Apply figure1 style
    elif pathname == "/fig2":
        return html.Div(dcc.Graph(figure=get_fig2()), id='fig2-container', className='figure2')  # Apply figure2 style
    elif pathname == "/fig3":
        return html.Div(dcc.Graph(figure=get_fig3()), id='fig3-container', className='figure3')  # Apply figure3 style
    else:
        return "404 Page Not Found"  # Handling undefined routes

if __name__ == "__main__":
    app.run_server(debug=True)
