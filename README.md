# RealTime_World_Demographics_data_Visualization

This project is about real time world demographics data collection and visualizations. The project simply includes a UI that displays various graphs and plots as visualization and for analysis.
The data is collected by scraping a webpage called [“countrymeters.info”](https://countrymeters.info/en) every other interval.


TOOLS AND TECHNOLOGIES USED
1.	Python
2.	Airflow
3.	BeautifulSoup
4.	MongoDB
5.	Dash
6.	Plotly

PROJECT OVERVIEW
1. Website is scraped every other interval depending on website updates. Following data is collect in specified orders:

    a.	World Population (Live): Every 3 seconds
    
    b.	Country Population: Every day
    
    c.	Continent Population: Every day
    
    d.	History Population per year: Only once for previous years and every day for current year
    
    e.	Age structure: Every month
    
    f.	Religion Structure: Every month
    
2. Scraped data is stored in MongoDB
3. Airflow is used to automate scraping process in their respective intervals
4. Stored data is accessed by Python file with Dash Plotly for Visualizations.
5. UI with visualizations is created using Dash Plotly

PROJECT STRUCTURE

The project contains following folders:
1. history_data.py is used  to scrape old world yearly population data and store in MongoDB
2. dags/ folder contains airflow dag files for scraping data in regular intervals

    a. data_daily.py scrapes data daily
    
    b. data_monthly.py scrapes data monthly
    
    c. live_seconds.py scrapes data every 3 seconds
    
3. visualization/ folder contains python files for visualizations

    a. get_data.py accesses mongoDB and gets latest data based on 'type'. It contains function called from visualization_dash.py
    
    b. visualization_dash.py contains html css part of Dash for UI
    
    c. functions.py contains all the functions which returns data and figures to visualization_dash.py for displaying in the UI
