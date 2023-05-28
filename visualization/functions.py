#this file collects latest data and generated figures and returns them to visualization_dash.py file
import pandas as pd
from get_data import get_scrape_data
import plotly.express as px
from dash import callback,Output,Input
import numpy as np
import plotly.graph_objects as go
#returning live data and figures every 3 seconds ie current population

custom_colors = ['#6495ED', '#FFA07A', '#BDB76B', '#FF69B4', '#20B2AA', '#9370DB']

@callback(
    Output('live_linec', 'figure'),
    Output('male_female_linec', 'figure'),
    Output('live_table', 'data'),
    Input('my_interval_3sec', 'n_intervals')
)
def update_3sec(n_intervals):
    live_df = get_scrape_data('live')

    live_pop = live_df.replace(',', '', regex=True) #removing , to change numbers into integer
    live_pop['Current population']=live_pop['Current population'].astype(np.int64)
    live_pop['Current male population (50.5%)']=live_pop['Current male population (50.5%)'].astype(np.int64)
    live_pop['Current female population (49.5%)']=live_pop['Current female population (49.5%)'].astype(np.int64)

    live_linec = go.Figure(data=go.Scatter(x=live_pop['Time'], 
                                           y=live_pop['Current population'], 
                                           mode='lines+markers'))
    live_linec.update_layout(
        title='Current Population Over Time',
        xaxis_title='Time',
        yaxis_title='Current population'
    )
    live_linec.update_traces(marker=dict(symbol='circle', size=1))

    # Create the figure and add two lines for male and female population
    male_female_linec = go.Figure()
    male_female_linec.add_trace(go.Scatter(x=live_pop['Time'], y=live_pop['Current female population (49.5%)'], name='Female', mode='lines+markers'))
    male_female_linec.add_trace(go.Scatter(x=live_pop['Time'], y=live_pop['Current male population (50.5%)'], name='Male', mode='lines+markers'))
    male_female_linec.update_layout(
        title='Current Male and Female Population Over Time',
        xaxis_title='Time',
        yaxis_title='Population'
    )
    
    live_df = live_df.iloc[-1] #getting only most recent data for table
    live_df = pd.DataFrame(live_df.items(), columns=['Attribute', 'Value'])
    
    return live_linec, male_female_linec,live_df.to_dict('records')

#returning latest data and figures every day ie. history_data, country and continent data
@callback(
    Output('history_linec', 'figure'),
    Output('history_table', 'data'),
    Output('country_table','data'),
    Output('continent_table','data'),
    Output('country_mapc','figure'),
    Output('continent_piec','figure'),
    Output('country_top10','figure'),
    Output('country_bottom10','figure'),
    Input('my-radio-buttons-final', 'value'), #radio butto for 'POPULATION' or 'GROWTH RATE' in history_linec
    Input('my_interval_daily','n_intervals')
)
def update_daily(col_chosen,n_intervals):
    #getting all history data and figures
    history_df = get_scrape_data('history')
    history_visual=history_df
    history_visual['Growth Rate']=history_visual['Growth Rate'].replace('%','',regex=True)
    history_visual['Population']= history_visual['Population'].replace(',', '', regex=True)
    history_visual[col_chosen]=history_visual[col_chosen].str.strip().astype(float)
    history_linec = px.line(history_visual, 
                            x='Year', 
                            y=col_chosen, 
                            markers=True,
                            title="Population Growth Over Time")

    history_df = history_df.iloc[::-1]

    #getting continent data and figures
    continent_df = get_scrape_data('continent')
    continent_df=continent_df.replace(',', '', regex=True)  #removing , to change numbers into integer
    continent_df['Population']=continent_df['Population'].astype(np.int64)
    continent_piec = px.pie(
    continent_df,
    values='Population',
    names='Continent',
    title='Continent Population ratio',
    height=600,
    width=800
    )
    continent_piec.update_traces(
        textposition='inside',
        textinfo='label+percent',
        marker=dict(colors=custom_colors)
    )
    continent_piec.update_layout(
        title_font=dict(size=24),
    )

    #getting country data and figures
    country_df = get_scrape_data('country')
    country_fig=country_df
    country_fig['Population']= country_fig['Population'].replace(',', '', regex=True).astype(np.int64)
    country_mapc = px.choropleth(
    country_df,
    locations="Area name",
    locationmode="country names",  # Specify that the locations are full country names
    color="Population",
    hover_name="Area name",
    title="World Population Countrywise",
    color_continuous_scale='YlGnBu',
    scope='world'
    )
    country_mapc.update_layout(
    title_font=dict(size=24),
    height=700,  # Adjust the height of the map
    width=1500,  # Adjust the width of the map
    coloraxis_colorbar=dict(
        title='Population',
        lenmode='fraction',
        len=0.75  # Adjust the length of the colorbar
    )
    )
    #getting top 10 most populated countries
    country_top10=px.bar(country_fig.iloc[:10], x='Area name', y='Population',
                         color='Population', 
                         color_continuous_scale='YlGnBu',
                         title='Top 10 Most populated countries',
                         text=country_fig.iloc[:10]['% of total']+ '%' # Display population percentage inside bars
    ) 
    #getting top 10 least populated countries
    country_bottom=country_fig.tail(10)
    country_bottom10=px.bar(country_bottom[::-1], x='Area name', y='Population',
                            color='Population',
                            color_continuous_scale='YlGnBu',
                            title='Top 10 Least populated countries',
                            text=country_bottom[::-1]['% of total']+ '%') 
    
    return history_linec, history_df.to_dict('records'), country_df.to_dict('records'), continent_df.to_dict('records'),country_mapc,continent_piec,country_top10,country_bottom10



#returning latest data every month ie age and religion data
@callback(
    Output('age_table', 'data'),
    Output('religion_table', 'data'),
    Output('religion_piec', 'figure'),
    Output('age_barsc', 'figure'),
    Input('my_interval_monthly', 'n_intervals'),
)
def update_monthly(n_intervals):
    #getting latest age data
    age_df = get_scrape_data('age').iloc[-1]
    age_df = pd.DataFrame(age_df.items(), columns=['Age', 'Percentage'])
    age_piec = px.pie(
    age_df,
    values='Percentage',
    names='Age',
    title='Age Population ratio',
    height=600,
    width=800
    )
    age_piec.update_traces(
        textposition='inside',
        textinfo='label',
        marker=dict(colors=custom_colors)
    )
    age_piec.update_layout(
        title_font=dict(size=24),
    )
    
    #getting latest religion data
    religion_df = get_scrape_data('religion').iloc[-1]
    religion_df = pd.DataFrame(religion_df.items(), columns=['Religion', 'Population'])
    religion_fig=religion_df
    religion_fig['Population']= religion_fig['Population'].replace(',', '', regex=True).astype(np.int64)
    religion_piec = px.pie(
    religion_fig,
    values='Population',
    names='Religion',
    title='Religion Population ratio',
    height=600,
    width=800
    )
    religion_piec.update_traces(
        textposition='inside',
        textinfo='label+percent',
        marker=dict(colors=custom_colors)
    )
    religion_piec.update_layout(
        title_font=dict(size=24),
    )
    return age_df.to_dict('records'),religion_df.to_dict('records'),religion_piec,age_piec

