import dash_bootstrap_components as dbc
import dash_html_components as html

footer_section = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4('Data Source', className='mb-4', id='about'),
            html.Span("The data is primarily sourced from "),
            html.Span('University of Maryland ', style={'fontWeight': '700', 'fontFamily': 'campaign,sans-serif'}),
            html.P(" "),
        ], className='col-12 col-md-8 col-xl-9'),
    ], className='m-4', align="center", style={'height': '30vh'}),
], fluid=True, id='footer_section', className='border-top bg-white', style={'borderColor': '#666666'})
