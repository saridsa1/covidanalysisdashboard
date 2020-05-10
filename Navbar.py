import dash_bootstrap_components as dbc
import dash_html_components as html


# top navbar

def create_navbar(appref):
    navbar_layout = dbc.Navbar([
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row([
                dbc.Col(html.Img(src=appref.get_asset_url("logo.png"), height="60px", style={'stroke': '#508caf'})),
                dbc.Col(dbc.NavbarBrand("COVID-19", className="ml-2",
                                        style={'fontSize': '2em', 'fontWeight': '900', 'color': '#508caf'})),
            ], align="center", no_gutters=True),
            href='#'),

        dbc.NavbarToggler(id="navbar-toggler", className="ml-auto"),

        dbc.Collapse(
            dbc.Row([
                dbc.NavLink("Map", href='#'),
                dbc.NavLink("Timeline", href='#timeline', external_link=True),
                dbc.NavLink("Progression", href='#progression', external_link=True)
            ], no_gutters=True, className="ml-auto flex-nowrap mt-3 mt-md-0", align="center"),
            id="navbar-collapse", navbar=True),

    ], sticky="top", className='mb-4 bg-white', style={'WebkitBoxShadow': '0px 5px 5px 0px rgba(100, 100, 100, 0.1)', })

    return navbar_layout
