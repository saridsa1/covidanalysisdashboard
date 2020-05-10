import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

pickled_data_source = "C:\AzureProjects\COVID19\data\pickled_data_source"

df = pd.read_pickle(pickled_data_source)


def get_hover_text(df):
    county_name_text = "<b>{}</b><br>Calculated NPI score: {}<br>Social distancing index: {}<br>Imported COVID cases: {}<br>"
    return [county_name_text.format(ctname, npiscore, socdisind, covidcases) for
            ctname, npiscore, socdisind, covidcases in
            zip(df['state'], df['npi_score'], df['Social distancing index'], df['Imported COVID cases'])]


def getmap_fig(df):
    z_min = df['npi_score'].min()
    z_max = df['npi_score'].max()

    hover_text = get_hover_text(df)

    fig = go.Figure(go.Choroplethmapbox(geojson=counties,
                                        locations=df['CTFIPS'],
                                        z=df['npi_score'],
                                        colorscale="Viridis",
                                        zmin=z_min,
                                        zmax=z_max,
                                        marker_line_width=0,
                                        text=hover_text,
                                        hoverinfo='text'
                                        ))

    fig.update_layout(
        hovermode='closest',
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        clickmode='event',
        autosize=True,
        mapbox=dict(
            accesstoken='pk.eyJ1IjoiY2hrMjgxNyIsImEiOiJjazg0bzFpOTkxa3JqM2twZzF1bndjZTJiIn0.5ATp6O0t0VwjN0CiTVyqBw',
            center={"lat": 37.0902, "lon": -95.7129},
            zoom=3.5,
        )
    )
    return fig


rendered_map = getmap_fig(df)

# link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300&display=swap" rel="stylesheet"
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP,
                                      'https://use.fontawesome.com/releases/v5.11.2/css/all.css',
                                      {
                                          'href': 'https://fonts.googleapis.com/icon?family=Material+Icons',
                                          'rel': 'stylesheet'
                                      },
                                      {
                                          'href': 'https://fonts.googleapis.com/css2?family=Open+Sans:wght@400&display=swap',
                                          'rel': 'stylesheet'
                                      },
                                      {
                                          'href': 'https://gist.githubusercontent.com/saridsa1/d07a4bd166294dd8e5caf01003de985a/raw/8f1817e2d570c24b66037aea1ea4872987f81e65/covid19-custom-css.css',
                                          'rel': 'stylesheet'
                                      }
                                      ],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"},
                           {'name': 'description', 'content': 'COVID-19 Analytical Report'},
                           {'property': 'og:title', 'content': 'COVID-19'},
                           {'property': 'og:image',
                            'content': 'https://covid19-curves.herokuapp.com/assets/covid-curve-app.png'},
                           {'property': 'og:image:secure_url',
                            'content': 'https://covid19-curves.herokuapp.com/assets/covid-curve-app.png'},
                           {'property': 'og:image:type', 'content': 'image/png'},
                           {'http-equiv': 'X-UA-Compatible', 'content': 'IE=edge'},
                           {'name': "author", 'content': "Saridae"},
                           {'charset': "UTF-8"},
                           ],
                )

app.title = 'COVID-19 Analytical Report'
server = app.server
app.config.suppress_callback_exceptions = True

config = {'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'zoomOut2d', 'zoomIn2d', 'hoverClosestCartesian',
                                     'zoom2d', 'autoScale2d', 'hoverCompareCartesian', 'zoomInGeo', 'zoomOutGeo',
                                     'hoverClosestGeo', 'hoverClosestGl2d', 'toggleHover',
                                     'zoomInMapbox', 'zoomOutMapbox', 'toggleSpikelines'],
          'displaylogo': False}

'''
MAPS SECTION CONTAINER
TODOS 
1. ADD INTERACTIVITY TO THE MAP
2. DISPLAY TIMELINE DATA

'''
map_section = dbc.Container([
    dbc.Row([
        html.Div(id='output-clientside', style={'height': '5vh'}),
        dbc.Col(dcc.Graph(id='map_plot', config=config, figure=rendered_map, style={'height': '78vh'}), width=12),
    ]),

    dbc.Card([
        dbc.CardHeader(
            html.H2("", id='stat_card_header', className='m-0',
                    style={'color': '#508caf'})
            , style={'backgroundColor': 'rgba(255,255,255,0.5)'})
    ], style={'backgroundColor': 'rgba(255,255,255,0.5)', 'left': '3vw', 'top': '-25vh', 'width': '242px'}),

], fluid=True, id='map_section', style={'height': '90vh'})

'''
NAVBAR LAYOUT
'''
logo_img_src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAACXBIWXMAAAsTAAALEwEAmpwYAAAgAElEQVR4nO1de3xT5fn/Pu9JUi4FwSmOTcDLvOEUdHPepkPddODanKRrN+e2H14GMpxKk+Jdw+ackKQw5q1uA51uc8XmnBRF8YZu6m4MAYV5n+IdUQqUS5Oc9/n9kaQ95zRpkjZpquX7+fTz6Xt/et6n7+V5nwuwF3uxF3uxF4MUVG4CyoHa5mbFeFM5SQpxNBEnDCjPt9ZXrwURl5u2/sagYwB3WJ9G4DvAGG/OJ/B6Al8c8df8u1y0lQOi3AT0JzyhSCMxP2SffABg0LES4h9qSPtZOWgrFwbNCuAO69OI+aE8qsYNoRy3vL56Q8mJGgAYFCtAbXOzQuA7LJmEvxF4OjHPALDRVOJUpHFrvxJYRgwKBjDeVE4yL/sE/mvbjlFnan7vPVqD97cdroqTAbxmajKldkHz5/uf0v7H4GAAoRxlTksWdz8VOCORTj982bTtAO4314krzqP7ibyyYlAwABEnLBkCLnsdBlVY0gbFSkzWgMCgYAAJsc6cJubLpi5eMTKdrrpl+XgCX2CqYiQMx4v9RmAZMThuAczkCWtrGXRsOouI35AsXhQEg5lPA7CfqUVE93tq+p/Q/segWAFAxAS+GIBMZzHTIQSuZmYPrJO/XRjy8n6nsUwYHAwAICXhuwJAvIdq25lpeuTKmnf6iayyY9AwAADofs9viPl4AE9ZS4gBRIQhj442qFoZSCsbBscZIAPcYX0bMacPgi/qfs8xZSWoTHCUegBPMDIGwJhYwvXuQ1d/Z2upx8sXxGx++TPKRkgG9Oc3Kw0DMJMa1n8I4CoGJgKA0xmHGtL+BYnr9bmeR0sy7qcZZfpmRd8Czv3Vg6OdzvgfAUztodqSMSM2X3LXzJk9HchKCjWktQHYJ5Vcp/s9k8tFSzm/WdEPgU5nvBE9/yEAcOGHOw5oKPbYn1aU85sVlQHcQf2bAKZbMhlPM+hOAM+bswl8oyccObyY438aUe5vVlQGIOKf2LKu1/3qGVG/Oss5Pn4CgCWmMhcY/1fM8T+NKPc3K/YW8FXT71t0n/rLtJ7dsro6Awp85soMOqHI438aUdZvVtRbAIOGETpvVzvsSpZjhm3euXnHmIRp3OHFHN+O6YGlQ1xjY0ahB6fq+dEvKMI43VCU17ZvH7nW/HRcbJT7mxV7C3jVlDxIbdS+Zi7fsn2/2TAxHYFfLub4yUefyCQ1qF3tDuvPtFWO2rl5x5gPvAtaTs23C+/ClrFCkS8w0Z+FlP8eVdnWpoa0J9whfV51Y/SrYC7qzcnyzYgOUkOa5TD40fb9a1DCb1ZcOYBEBITTUimCxApPMHI1FLzCBk+RQrkRZvkLIVKMYb0LWo6XQsyksHYug74IAqhrnH1Z0FwA7nz6YklfB7CvKWs4gDMJfCZJvkEN669zUL9fQN6vNXj7/GTMTBqBT0snQLS8JtTyUynoZRj4miTxc9MKUbRvlkZRGaCjouKOiljHT5ASZAD4HBPdBQmACJbJByBJdNPOzReBQECsGXHcd4SU9ZLwDQDgLGINSeLNfPslwc+wQR8D+FyWKocS8bUMulYNak+DMF/3qY/0yqaAmahRH2+eXzArBkRT8psB5slnpkd0n/qQ9VTQNxR1C3j4smkdzHQhgPZ86pPk2zyhyCWFjDElsMrhCUUuWVs56SXBMorU5GfBRgA3yR3K1fn2H5lT875Q5DEMms2gPwL4X9bKybFXqGF9nRrSzgsEAvl/z6TkLwjGFXlVB30gDWVmsY1XSvIY5A21TJAQTQDOyVDcBmCUlQiepfm9d+bsN9xykmRxJ4BJGSsQdoHxBIFXEPjhiL/mrWx9FSIJ9C5sGcuSpjLT9wGchez/OH+XJGa3+tzPZylPgpk8IW0BE/ltJdlWnnucIl6/rL7ukx777QVK9xrITGpQnwTCFCLeX0K865CJxySJbUz0BIAvWwnJzgTqQm0UG/QrAs/MQvPrAH7tHBpfumx2XV6rjxrSPgEwOpV8Xvd7js+nXfWi6AEiLs8D4QoAEzJUkQy6gw26uvVK945updkn/3FjhMOtbEscbv9mLXO/+2q3foqEsjwH1y5u3j8ecz4JGxMw0SVRn9pkznMH9Soi/i2AAzJ09QyAsHN8fPmyurqCXvTUkNYKoAoACLxQ83vrC2k/o6nJubl9zPeI+SoGddcgJkR1n0e15GWf/MecIu5eVl+3uxAaioGy6QPkZAJmUhv168D4ebfGhE0s6dJog7q8t+NPXbxipCsem0Hgnc4d8d8vC9T1Sgs4EAiItcMnXQDCfFiX7w91v6fLtoCZ3OHofALb5fllm3ygzAohPTDB5YLlaQz6rq2JwaDG3Tx03qMN5+zsP0pzo7axed+44bwJhJkABIOujfrVmwEM2MkHBoBGUIoJngCQSyPnRcni/NYG9/r+oKu38C5sGRtPOIcsb6hO3h6yTT7hUSfF1XJOfpKMAYBcTEDgVsNQfpjxUDWQwUzukLaA7Hv+AJl8YIAohS67rO4jpyt+FoAXMhQ/PKl9vefTOPlqWL8lw+S3Gew4fyBMPjBAVoA0UivBfwCMsxX9WPd77u2x7S3N+8SdzivAOBfAwQC2EvgZknxrZG7NmlLRnA1qUAuAcGOmMmZ6xLUz5u7twbOYGFAMAABVoeX7OZBYxdaDofVEbYM32HIuEzUx6IsZig0iDu2zY1vg7sAFe4pPcXfU3tK8T9zh3Iqev+/duk+9sNxuaQYcAwBJJlCQeBJdZ4K1ut9zXKa6nmDkZCZ6Fjn+FiZaHPWpBVn81IQeOFJC+Bh0CgAXMT9HxLfmciMzdfGKiopYx/voEjStFCzXSBIWkTQRX7R1x+g/jB659VRIHAWGwQqtm7x93epAICC791x8lJUBPOHIJDAulSRedo2LLTQLc2obm/eNs3MeM412yMS8TNKwqYtXVFR0dDwPgtn8O4GkZPDz6BL1AgALKU+LzK15Nh/a3CH9YgLfBnSzJJZEfIPm8/6yp/ZJsbVSz4xXRu/cetPdN07vUEP6bSDMMlWLAdwG0BhzWwJvkCwuijao/8yH1r6gbAzgXdgyVhpiA7r+S67Q/Z5fF9KHJxypZaZmU9arUohprfXu16YuXlExJLbnVgZd3FmaSTqXATWhB440oKxD98nvBEs6PTpX/Vsh9M5oanJ+2H7AKmLORz9BIvlNflPIGIWibLcANmgxuiYf6H7wy90H0xRrBma01rtfA5Ivk1vbR88C8Kap/Ix8FDoS5KiHdfK3AHjPXIcE5/3CmMZdM2fGlYTxfRC251FdAAhXNbaW1FFFWRjAE4y4bVI+g0FLsjbIDrNVL6QUr5jTKVWu101ZI6fPu9viCCITiPkkU/ITp4gf4RTxLzHoJVP+yQU9/6agHGy8D2bLYZTAfyXwdAb9BIBZyaTk/oqKphBSvSh6gJIwvgnGFyTEFoWMJzM9x85oanJu3kFhcx4T3Rb1qRvtdXOC8J5FWUbwiQA6jTur50dHANIsXNqSz02AQU6TIkYcwG4ciBhtskycY8PEiQVvoYlNjpPNez4TP+sclzgzff6pnh/9i1DkGgBfSlWZ4l3YMjYyp+b9QsfKB31mgLODK4cPp52/4IS8nEEircUiIaCGtHspxnO0a7wfp+t/tGP/iwAcaupiSyLmCPRqcMajQJdCBYGb1LC23Tku/tTud4Z+XsjE7wF0HbAIeZlXEfifAI5MJQ+IS+c6bMIeWCWV/yz0BRIAJMSRZi0fkrTU3E/rle4daki7H8B1nW2kmAigJAzQpy3Au7Bl7DDatZ5Bc7L09SN20UZ3SJ8IALWNzUMZdIO5AjFf01sDyMnt61amroCpzrA/GI/HNzljDpl4B1aFlA6FjV/k068U4laYnEkAOAw2MTURL+oNzXZ/RSR4tL1Of/or6j0DMJM0xO0ADslRcwyBl04JrHIk2HEegLGdJYQ1jgmJ3uz9AIBAICAF5IUMsi/r3f8uxrwW/3df6pafAa317tVEfEMPVW7XfN4HCyC1E9Jgyysmg+aV019Rr6+BnsbIt1nSw6asBAhBkvxPEI5i0LUAKtOFUohZQspLYFLnYqZvRRvUx3tLQxruRv0YMngJyGJkkcY2MHy6X11SqNTNvUA/jYivAuEkAE4A/5IkFrf63K2F0jh18YoKVyx2DYGvTvVlxv8Y9BdidoHwY5gPt4wWvcFjfxYvGnrPAKHIEgZ1cSrhAt3nuTudrA5HzxAsnzSVrwHDrHb1ou5Tjy2WKHRKYJVjdOXW7zHRNAZNAKONmJ+VUtzTeqX7vdw99ABmCsybR72VzrnD+ikk+Xc2gVU+2J4QjokP1le925tx80GvD4EMOsKUNJw74n8yl7f63KvUkPY2uu73R8KK3xRTDp668v0x9VNcEHEAKJjW6vnREcIhbwbzbJD1n40Zu0BUQWAlS/PtzDS9lJMP9O0QaD6YKNjfJjVjFjDr8TGGmko7pCH+3IexBzw8jZFvCId8EYxLYVtpGXS/AB8sWE5GN39FMIhY6y9/Rb2/BhLWgjElnYzvdgbA3JD+r/aEtesY5LK0SIGJnq84uGNXr8ce4Dj3Vw+OZhl/GLAwPQC8Q8SzdJ8nfYDcDOCM2gXNn4+T80giTjhEYmMp1L+zoddngOpw9DjBcjWsq8iTDPqXgJzIoOocXfyPiG9lQUv0OZ623tIxEJGyi3jTln17h6vi6pRf4gGDPj0GqSEtBORlqCSRbbsh7ILEPYLk/J4MOUqJQCAg1o845muGVI4SQg4D8NYe55C/9mWy1KAWBuEKAr8IYLbm9z6TV7sF2qEgjGvbOeqZUlolp9EnBqgKLB+mVCb+AuA72eow0bNwYgbFqRZSzgZh/yxVPzHgOGK5v2pLX2gqBLWBZle80jkLwFwAX7AVxwD8yUg4blx+VdWm3vQ/o6nJedeMGYl8D7vukH4OgVcAEPm+XPYVfX8OTuq+fR/ATbAKhd4n5lsm7Vx/a/r6VBtodsWGu75LxJcBODEDNd/UfZ4nMg1THYweq5AxjUHHEvglIn404qv5R2/Jrl4UPUAkpAbg5BxVt5Hg72v13kd6O1a+UEPaUpjcxUhDfLHPV9gcKJ4+QNIU7BAGfcEhEh8d0/7iKz3dm91B/UQSfBkYdUgeRl+Thjjervw5JbDKMWp42/yUKZZ9G7l7Fw+7tFAbgdR//lPIPfnJPw20h4lOyWnz10d4gpGg2WqIBE/R6r1PF9pPIBAQzw0/eWg+36V45uFErCefXl8HgJYc1VPaLudXL4rWi7g8yjksvjqTXd+oyrZ6ANnMtqYPFbu3AyhI1Su17NsnfyUYD4KwDcBXAFwCoAIACDyEmJvAfGIpdfgkiZfND0VSisMA5M0AakhTAVy+FjhlGHa51JC2mcAPJRLOQLZtbEDqBKZRe0vzPjGH6wMCD+mhGkshDk8rguRCIBAQaysnvQ3rnn+l7lOD5sl1N+rHkOSnYVJaIeaztAbvkygRqkPR0wWkecIX6H7Plbna1TY27xuXrjsBrs1SpZ2Y67UG72/tBSVXCFEXaIeqIe0vakj7kzusF6T1E1NcJ5gnn0H3O13xMWA0mqqRwsbp+fb5/PDJJ8A6+Svtkw8A0Xr1BdhWFhbkKYT+QkHEVl8E3O1gmhE5Jh8AKpnoLndI72auX3IGIMFLANQBOI+Ybyuw7YGWNHjFssvqPmIm3ZzPoLwZS5C0iKSJeUW2ZT0ed1pf/LhgWX5BcMVj1munwIhcbdxB3WOffAJvALASgEWgRMR31d7WXGnOK7mzaAZNNCW+1EPVbpBSrBFkOUferIa1gyD5PNsYeUf7lCSGmPwHgQVlvesP69i1M+50GgDS8vph+Y6TL7yhlhMkxPcYNCQGkMUfENNX3CE9l0qY5apIxNdp9Z6bQcQp9fpHkDzTAIzxsV2uagCd7zYlZwDLGISCBBsVEzo2JDY5Npjs7w8E4+e2k8v7nKBCtHPftqSSL5R3Z6oYH+mcDAnzY82bBYyTE+6wPs5g/JXAQyjjWxMfSMDsfPsj5g80X3LyAWC5v2qLN9xyqWTx98464K/DxAD9oRTaYfo9q5p1JiyrqzOI+GKgR8b5aSF2gylmMT9kzawORo+115sSWOWAhFXrJ0+VsnwhpDwsxwG3IDAR27czA8q7tjoWDaT+YIBOOT+D9umpYiZEfDX/kCy+AuDvtqIXWNLput+jZ2qXDSlmMT9duwTJp9SQ9iPPzZHPTV28okJt1L42qrLtaVivip844/Givs7tqRjyLIDnitjl8KrQcoumtJDy25Y05BvmdH9sAdvSvxB1RugoCCmfAKfUNjbv2yErvlwhO15ZNrfug94SZCQcNyqOhAddlkOjAfyBXYSKWEfGdwsGXb/sqrpt9vxsqF3cvP/uxFBXT+/5D182raO2ufl0+aY4RJLIqa6eCUz8C0CkzwEjFSQecYf1y0jwe5TgbzGR1diGYTnYllwOoIa1lWCcnU6PGbHZVc44AWmoC7SzIaCj+5NtNzDozqjP/dOcQqCkW5v/A+NapNW6CZuYaZFrfGxxb7SIc6HqluXjFUdiA0zqd9np665eVvotgGF56t2ya7/9slXtT+hzPY9KEqcC6OkG8QmDZuc1+QA8Ye0uMJYCptsOYzyBG+ObnMuL7WYWAJZfVbWJmHM7uGJ85OT4pfbsvAiqva25smNPxZmC5QQAbVDwN32O58182rqD+k1EfG1nhsQ5AypkTNJz1xksyAPGEQCGMugdMB51GbFIvst+BiXZ7kOBfhL1q7/rqU7NwpZD2MDnIj7v6kLEzu6Qfg4R32UOkp0GgR8wHMqlrVe4P7SX9XgGmBJY5RhV2VYf342AgOxaKg3AE4o84JCJn+Xaiwls8elDxJMAPFoVWr4fQU5UYMhJ7euf6y9z6O4EEmvAk0j+9Bosabot6zEAOwB4O4dKqntnZQBPMOI2DNIAkBrWl+jARfmOH/WrK2tvaz46tstVTcSnMmgfMN4UkA9pDV77AboTWVeA1Fv/k8j0bNuFrYLktKzPsszkXdR6ijRklzIEYzMAMusFEPMftAbvpzp4hBrS3kDSMwlA2OQcFz9kWV2d4Q7rz5isgTvGjNg8ItsZSA1pq4BONTvW/Z6Sb9FZVwBleOIX6HnyAWC0ZHFPVdPy43gnRjtlfGJK8pf8CesTpdXzNkAYY++Eib4HfOqjh3yENAMw9u14p+Lg6kXRHZSQnUsyg7beNWNGAjNndms8PbB0SJv12pndR3ERkZEBqhpbj4Y05lgyCb8nyY8z0XgA16DrCnW42GF8TOAh2bx154HHettwoIDAzzIoHR+hUkj5KiQYplWWgL9l29e3jdznREiYr4JPlY7aLmRkAMUwam167DfpPs/16UR1OPqYWSG0UGkWgd9l0EYAG5lojYtiy3pB+4CCQyYWxIXzAlgdYZu/YYyBQNYO2BY1jLCqmPRlQ+YtgKxGHALScnBp9bmfdwf1bUTdDRtt/WxiSRuJeAMRbyTwRiVu/LcQgUo2TAmscowesfWQPc4hbz182bSO3C1Ki2Vz6z7wNEbOY0n3AN22uR0EnqX7PZlN4JmJw7r5RU9KRfTLqpiRARiUsJowczcZPhF/hJSyBIMYLFcQ0QZCcqIThuOlUvj2885vOZAVWshom8pMwytiHR3uoL6KJV3ReqW7T+FU+hqyVav3PuK5OTIRTlzIRCcxqILA/xCGvLuniORqWD8eVn3KpzJd2UqBjJu2JxhpYKIFpqx7JrevuzB9VfMGW86VJMwixf/ofk8mw0wLZjQ1OTdvHzOTiMfGhfP2Qs2e3CF9IoH/DiCTSLmDBJ9TsA6dKWQruiKdAEBRQ7bWBppdR2NjItN1164MmslreqmQkQG8oZYJBpSXLHs74W/MtEpAjmPQj9H1Rg4GzY761dtzDWZ2nkjgDVvbR0/OV/c9EAiI5ysnP0uwuG+x43WniB+TrxfO/grZqoa1G8G4DsBbkPipmanUhdpBMPAaUt+TQXsklHH9pR6f8Z4Z8de8RWCrl0vGaQS+IWURbH4j/7trfCw/bjVZxzLo6H1GbPtBvoS+UPnlw22TvxXA7QQ2ryKHJqTj6/n22R8hW6cuXjESjBuQ3G4PhcBKNajdfnZw5XAAoARfBdP3FJD39adtRFZBQ1v7qEYG3Z+j/ctEPD3fRw4GWU77xHz9lMCqvF4kE+SwhKADo0H3e2ZLFtMt2UQ9rRCd6K+QrZWftO9B0suYucNZw2jXOm+wxcNkMrFP0lCQq7y+IisDPBU4IxH1q+cxkxdWT1sAsINBt4xqb5us+byvZGqfCce1r43YRMNfGl259fx82hLzR7asrwQCASFIWs4eDNqcV3/9FLJ1WaAuJoU4F8AbtqJDJSgCs5IMY0UxQtEVgvwkN8zkadQOk1KMZ4Xa4g7nC729eqV0182KFR/G486jcp26PTdHPscu+hDW7cewpcGgo6P+3B7H1JD2OrpO3lt0nzrGLKRRF2qjYMBM02O633M2eona25orY7tdQQJnjZJGxJM1n3ddb8foDfKTNROx5vO+Em1QH2+td6/uy71b96lRMFabsg5wOWMLsjZIQbvG+zGDgrZsu3OFe/OZfCAZstWUzBiyFVZVtD6FbF02u6496ldnMejbtnNLF0kM94ymJrv7mJKi/x1FEjEIl8DkhYtBF6tBbUqupi4R+zmA5izFj1GM52Qpy0RGj2FuSxWyNepXV8birmPAuM9OEoPmbd4+5rm0V7X+QNksg1Lm02ZFhvecMv6VfFS91AXa2azQuYLlMRLiZQH5mObzaIW8n6tB7QoQFpqyPibmq6HgFVPI1s5rMBFX9dYzWFYawloNGHfC5vEUQAcRXzNpx/pFgRtvZLVR94LpewR5BDPFiHgtGEt6eubNF2VjgLODK4cPo10vAjioixj+6/4jPvpmf6iMpVy6r4FV+JMRzPRI1O+e1me7QGaqCbccIYTcnPYCUr0oeoAwZBM4Y2zjfxJxBzNltHxi0G1Z4xPmibI5i3604ZydxPwDJF2xAgAYdPqH7QeE0qpT0wNLh5h96BUT+Ya5LVbI1hlNTU41rN9vQPlvXDo3pSOat17h/lCvVz0Eng50cyJ9YrbJBwACzxYO+UBfVM3KbhzqDuk/Tfnl7wIhwJLWEPF9AIaD8DPd57mjFOPnCHNblJCtKRd2f7Y4yCb8Xvd5LjbXSyl4LkEyPG0m7ETy2mg9KNpc9BWCsgeNivrcdxDzHyyZjIAgqSMp81fAyMvFa28Q8de8pfvUqZA4Dow5BL6ZQbMVaRyu+z3T+zr5tc3Nyj6V2+61x0Ak5tX2usuvqto0uX3d2cR8naWAwESibnL7upFjRmweDsY8W9N5vV0Fyr4CAEkfwnHpfBDAmVmqPKf7PfkEWeh3qEHtIhDOYqY/2yOZ1jY3K/FNzqUAfmRpxLhD96uzs20r7rD+Y2K+x1T/Pr3B09VH8gHrYZhWLUUah/cmxnDZVwAAWFZft9s5NO4mqz/+NN6Cgrykhf0NTyjyLRB+B+A8Io6aza+rQsv3i7/tXAH75AN3Td657tKezhTEbAmQReAHrBWIGWQRVyfgyBpUqyf0h2VQXojvdn4TYLv18MdQMCVfFfQywGy/TwS+zzu/5TjpFF+ATDwA7hYFZcnk9nWzcmlAE/hDs3odCzoWQNRSh/lY8/rNnJ8I3I4BsQKkxMPLYGFI3gwFXx3Akw/H0EQLrDL+/VihpyHxDGwhcAi81Dk+PiMf9Xcy2Oooi3G1Jxz5DpgpEAgITyhyFQjTTDXeaZ1bnfebjJWuMsMd1D1E3AyrGfkmQypTOuPvpqCGtbMgcRDFWTcHoSgnvAtajpdCPAcgm21fgsBzNZ9nUSFXSU8o8ltLwKsktoJQAe7mp2Cm7vfcVQjdaZR1BShk8t1B/QdgPA7C79hFb6ghbe70wNKimVb3FpG5NWuYqCcnVQ4G/Upt1DXPwkjeHkZYoQZ0jxIyOsPkPzW5fV2P1kY9oWwrQCGTD2RwT5/EW2CEdmHY0kJdxalh7Sww7kDSgdKP+/QMmzQKvQ+MXAouMQDX635PzscvAKhZ8MBhUojfMTILgwi8NBZ3+XobcQUoV9SwUMSbafIVIc/INPkp/BndHUVMAOE3w2jX255w5JaCHlEYtyMZCuY4m/5j4SBiOUpcwqBcTOgCMN8TjGQS+3ZDy9zvvjqpff0ZBP4hgVsBvIJkgO17wThD83sv7MvkAyVcATzhyOHMdDkYZ6Ssgd4BsJKIX2amJmSY/JY5NXalCQuqg9FjBckFyCy1S3XF60FoJvAT+1Vu+U8PZlht6DJuWaf7PZMz1Uspsp4KoIqJphF4HDMtijaoFmGNGtampyyDzfgPgNcAnALrofD9DlfFkQPBcXTRGSAl/PAxaF6eBiNvK4qckmvyzfCEIt9iUD6maztBeFwxjAa7kMTMAAxa70rETu9wVewvWE4g8ASWdDQIJzHo+Ex/h5FwTDA7X1RD2mqknTEBYOZfRhu81wHJwBHk4IdtEUNzRkTvDxR9C4hvcvoAzC/V5AOA5vc+pvs9JzHRqQAiyB7NYzgY7oTisP9ngkHmt/5j4w5nm5DyVTAeZ6bfp56qT8n0dzBoj1KR6PzvrQ00uwBTOBzG6vTkA0m3NIphWB0+Eqw6jmVCURnAE44cziC7nHpnKuKmPfSZIZQOtdDJNyPqU5/T/Z6ahHCMY1A9sjh7IO7umobAOT2DZIBMhalTLTEOhmAozKspwa6/CFbImsd5ePToBxSVAZjpcosSBbhVGmJs1K8e5RTxQwAyH1gUmajI28NnT3iwvurdqF9dqPs9X4OCg4n4Igb9Eclzx1sE7h7TILNfNjs4xbz3gvAjA44Doj7161G/utJcadmVtdsBmOUSJ9UuaP68tSOyu363K9qWBcUWBU8x/b7TMTRxvjbb2w4Ay+rr3lUXaCdAoMunL+FMAL0KwJgNKcnhEli1eruDsRudfpPrn5wAAAMBSURBVHVoB4ifJMnbJIk3ifh/ksUbFYmOdXnZMRIxh/UIcaem8ei4cD7hDusNDHpfgTGN2WoYKlkUHHquFCg2A5hVm96ze//WG9Q31LCeMI3bzVdAP8Jky8Bv9DU4gyKMG6UhatFlHTyRmB8iMOxm80z021a/e323TsqAYh8CzcENJngXtow1F3rDka/Cqmhp9dr5KUZkTs37BL4U1pCzmfCGKx7rtaVRsVFsBjAbUrqkIaI1Cx44LBAIiJRP3L9YanNxPW+WG5rf+0dB8lQw/pulyu3SEJOLYR5fLBR1C3DK+MK4cP4EXT72TzCE8sraykmZnC++7FASdtXoTz0ivpp/1AaaJydGOs5kSaeCMAoSrytsPNQbhY1So+iCIDWk/QjAH3JUYyHlaZG5Nc/mqFcy5CsJ/Kyj6IIg3e+5l5m8DMqm3/9KuSd/L7pQksegaIOquUTsaDDmgBAF8BxAy4h5hlPEJ++d/IGDkqmEpbRpF6HI9/y9KC4GhEpYf6Mm9MCRDOrU4GHG/t75LQf21OazirKrhPUnahubh8aka15KNGxn/t0MurZUXr0HKgbNClDb3KzEpfMJAjcg8989lMCNsU2uezKUfWYxaBggvsl5BfKIFErg8/PV2PksYFAwwNnBlcNB+Lklk/ArRZGHEvERdtM0JgqWwrf/QMSAMQwpJYaK3d+wadMu0X2ea9KJQCBwwdrhkyaA8I1U1mGeRu0wLamD95nGoFgBCDzBlrbEBggEAhICFmMMyeLg/qCt3BgUDGAPWyNZdLvy2aOPkuA+adt+WjAoGEBAWkKzEfFV1eHocem0O6xPI2azzcGODkdFv3rrKhcGxUEHADzhSITZEvw5DmA1GE4Q7L4Gg1G/Ord/KSwPBsUKAAAkeDZg2QqcAE62Tz6AV10idiMGCQYNA0Tm1LwvpPwOYNJJ7I5/KzCq83U2/VnAoNkC0qgKLB+mjEg0MNP3CXw4AAOEF8C4u6191B35ei/fi88ApgRWOQKBwKBZBfdiL/ZiL6z4f7oNOyo3taZ3AAAAAElFTkSuQmCC'

navbar_layout = dbc.Navbar([
    html.A(
        # Use row and col to control vertical alignment of logo / brand
        dbc.Row([
            dbc.Col(html.Img(src=logo_img_src, height="60px", style={'stroke': '#508caf'})),
            dbc.Col(dbc.NavbarBrand("COVID-19 Analytical Report", className="ml-2",
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

'''
FOOTER SECTION
'''
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

'''
APP LAYOUT SECTION
'''
app.layout = html.Div([
    navbar_layout,
    map_section,
    footer_section
])

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
