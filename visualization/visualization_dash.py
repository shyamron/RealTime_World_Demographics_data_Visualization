# This file contains all html css for dash
# figures and updated data to be displayed are import from 'functions.py' file
from get_data import get_scrape_data
import pandas as pd
from datetime import datetime
from functions import *
from dash import Dash, html, dash_table,dcc

app = Dash(__name__)

history_df = get_scrape_data('history').iloc[::-1]

live_df=get_scrape_data('live').iloc[-1] #getting only latest value
live_df = pd.DataFrame(live_df.items(), columns=['Attribute','Value'])

religion_df = get_scrape_data('religion').iloc[-1] #getting only latest value
religion_df = pd.DataFrame(religion_df.items(), columns=['Religion', 'Population'])

age_df = get_scrape_data('age').iloc[-1] #getting only latest value
age_df = pd.DataFrame(age_df.items(), columns=['Age', 'Percentage'])

continent_df = get_scrape_data('continent')
country_df = get_scrape_data('country')


app.layout = html.Div([
    html.Div(
        className='row',
        children='World Demographic Data ' + str(datetime.now().year),
        style={'textAlign': 'center', 'fontSize': 40,'fontstyle':'bold','text-decoration': 'underline','color': 'darkblue'}
    ),

    # LIVE DATA
    html.Div(
        className='row',
        children='Live Data',
        style={'color': 'darkblue', 'fontSize': 30, 'padding-left':'20px','padding-top':'20px','text-decoration': 'underline'}
    ),

    html.Div(
        className='gridcontainer2',
        children=[
            html.Div(
                className='live_table_data',
                children=[
                    dash_table.DataTable(
                        id='live_table',
                        columns=[{'name': i, "id": i} for i in live_df.columns],
                        data=live_df.to_dict('records'),
                    )
                ]
            ),
            html.Div(
                className='Graph',
                children=[dcc.Graph(figure={}, id='live_linec')]
            )

        ],
        style={
            'display': 'grid',
            'grid-template-columns': '40% 60%',
            'grid-gap': '5%',
            'margin':'20px 20px 10px 10px'
        }
    ),
    html.Div(
        className='bar-m-l',
        children=[
            html.Div(
                className='linechart',
                children=[dcc.Graph(figure={}, id='male_female_linec')]
            )
        ]
    ),

    # EACH COUNTRY POPULATION
    html.Div(
        className='row',
        children="Latest Country Population Data",
        style={'color': 'darkblue', 'fontSize': 30, 'padding-left':'20px','padding-top':'50px','padding-bottom':'30px','text-decoration': 'underline'}
    ),

    html.Div(
        className='gridcontainer2',
        children=[
            html.Div(
                className='country_table_data',
                children=[
                    dash_table.DataTable(
                        id='country_table',
                        columns=[{'name': i, "id": i} for i in country_df.columns],
                        data=country_df.to_dict('records'),
                        page_size=18
                    )
                ],style={ 'justify-content': 'center','width':'50%','padding-left':'25%'},
            ),
            html.Div(
                className='map',
                children=[dcc.Graph(figure={}, id='country_mapc')],
                style={'justify-content': 'center','width':'90%'}
            ),
            html.Div(className='barcharts', children=[
            html.Div(
                className='top10',
                children=[dcc.Graph(figure={}, id='country_top10')]
            ),
            html.Div(
                className='bottom10',
                children=[dcc.Graph(figure={}, id='country_bottom10')]
            )],
        style={
            'display': 'grid',
            'grid-template-columns': '50% 50%',
            'grid-gap': '20px',
            'margin-bottom': '20px',
            'margin-left': '10px',
            'margin-right': '10px'
        })
        ]),

    html.Div(
        className='row',
        children="Latest Continent Population Data",
        style={'color': 'darkblue', 'fontSize': 30, 'padding-left':'20px','padding-top':'50px','padding-bottom':'30px','text-decoration': 'underline'}
    ),

    html.Div(
        className='gridcontainer2',
        children=[
            html.Div(
                className='continent_table_data',
                children=[
                    dash_table.DataTable(
                        id='continent_table',
                        columns=[{'name': i, "id": i} for i in continent_df.columns],
                        data=continent_df.to_dict('records'),
                    )
                ],style={ 'justify-content': 'center','width':'80%','padding-left':'10%','padding-top':'25%'},
            ),
            html.Div(
                className='map',
                children=[dcc.Graph(figure={}, id='continent_piec')]
            )
        ],
        style={
            'display': 'grid',
            'grid-template-columns': '40% 60%',
            'grid-gap': '20px',
            'margin-bottom': '20px',
            'margin-left': '10px',
            'margin-right': '10px'
        }
    ),

    # WORLD POPULATION HISTORY
    html.Div(
        className='row',
        children='History Population Data (1952-2023)',
        style={'color': 'darkblue', 'fontSize': 30, 'padding-left':'20px','padding-top':'50px','padding-bottom':'30px','text-decoration': 'underline'}
    ),
    html.Div(
        className='grid-container',
        children=[
            html.Div(
                className='table_data',
                children=[
                    dash_table.DataTable(
                        id='history_table',
                        columns=[{"name": i, "id": i} for i in history_df.columns],
                        data=history_df.to_dict('records'),
                        page_size=12
                    )
                ]
            ),
            html.Div(
                className='Graph',
                children=[
                    dcc.RadioItems(
                        options=['Population', 'Growth Rate'],
                        value='Population',
                        inline=True,
                        id='my-radio-buttons-final'
                    ),
                    dcc.Graph(figure={}, id='history_linec')
                ]
            )
        ],
        style={
            'display': 'grid',
            'grid-template-columns': '40% 60%',
            'grid-gap': '20px',
            'margin-bottom': '20px',
            'margin-left': '10px',
            'margin-right': '10px'
        }
    ),

    # AGE STRUCTURE
    html.Div(
        className='row',
        children='Current Age Structure',
        style={'color': 'darkblue', 'fontSize': 30, 'padding-left':'20px','padding-top':'50px','padding-bottom':'30px','text-decoration': 'underline'}
    ),

    html.Div(
        className='gridcontainer1',
        children=[
            html.Div(
                className='age_table_data',
                children=[
                    dash_table.DataTable(
                        id='age_table',
                        columns=[{'name': i, "id": i} for i in age_df.columns],
                        data=age_df.to_dict('records'),
                    )
                ],style={ 'justify-content': 'center','width':'80%','padding-left':'10%','padding-top':'25%'},
            ),
            html.Div(
                className='barchart',
                children=[dcc.Graph(figure={}, id='age_barsc')]
            )
        ],
        style={
            'display': 'grid',
            'grid-template-columns': '40% 60%',
            'grid-gap': '20px',
            'margin-bottom': '20px',
            'margin-left': '10px',
            'margin-right': '10px'
        }
    ),

    # RELIGION POPULATION DATA
    html.Div(
        className='row',
        children='Religion Division',
        style={'color': 'darkblue', 'fontSize': 30, 'padding-left':'20px','padding-top':'50px','padding-bottom':'30px','text-decoration': 'underline'}
    ),

    html.Div(
        className='gridcontainer1',
        children=[
            html.Div(
                className='religion_table_data',
                children=[
                    dash_table.DataTable(
                        id='religion_table',
                        columns=[{'name': i, "id": i} for i in religion_df.columns],
                        data=religion_df.to_dict('records'),
                    )
                ],style={ 'justify-content': 'center','width':'80%','padding-left':'10%','padding-top':'25%'},
            ),
            html.Div(
                className='piechart',
                children=[dcc.Graph(figure={}, id='religion_piec')]
            )
        ],
        style={
            'display': 'grid',
            'grid-template-columns': '40% 60%',
            'grid-gap': '20px',
            'margin-bottom': '20px',
            'margin-left': '10px',
            'margin-right': '10px'
        }
    ),
    #interval for displaying daily updated data
    dcc.Interval(
    id='my_interval_daily',
    disabled=False,
    interval=1*24*60*60*1000,
    n_intervals=0
    ),
    #interval for displaying live data
    dcc.Interval(
    id='my_interval_3sec',
    disabled=False,
    interval=1*1000,
    n_intervals=0
    ),
    #interval for displaying monthly updated data
    dcc.Interval(
    id='my_interval_monthly',
    disabled=False,
    interval=24*60*60*1000,
    n_intervals=0
    )
],style={  'margin':'20px 10px 20px 20px', 
         'fontSize':14
        })
if __name__ == '__main__':
    app.run_server(debug=True)
