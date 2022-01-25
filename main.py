import base64
import os, re
from dotenv import dotenv_values

from sqlalchemy import create_engine, text

from datetime import date, timedelta
import pandas as pd

import requests


def main(event,context):
    """
    Triggered from a message on the Pub/Sub topic db-update-topic.

    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    # SQL CONFIG
    settings = dotenv_values()  # Loads settings from .env file
    ROOT = '.'  # relative path to the root of the project

    db_uri = (f"mysql+pymysql://{settings['SQL_USER']}:{settings['SQL_PWD']}"
            f"@{settings['SQL_HOST']}/{settings['SQL_DB']}"
            f"?ssl_ca={os.path.join(ROOT,settings['SQL_SSL_CA'])}"
            f"&ssl_cert={os.path.join(ROOT,settings['SQL_SSL_CERT'])}"
            f"&ssl_key={os.path.join(ROOT,settings['SQL_SSL_KEY'])}"
            f"&ssl_check_hostname=false")

    engine = create_engine(db_uri, echo=False, future=False)

    # Loads the stations DataFrame from SQL stations table
    query = "SELECT * FROM stations;"
    stations = pd.read_sql(query, engine)
    stations = stations.set_index('station_id', drop=True)

    ### MAIN CODE --------------------------------------------------------------
    # For each station :
    # - gets the previous days where the weather is already known
    # - gets the 10 days weather history for weatherapi.com
    # - updates the days when the weather is unknown


    for station_id in stations.index :

        nb_of_days = 10 # We check and update the last 10 days of history

        station_coord = \
            f"{stations.loc[station_id,'lat']},{stations.loc[station_id,'lon']}"

        known_days = get_sql_known_days(nb_of_days,station_id,engine)
        print(f'Station {station_id} :',end='')
        print(' {len(known_days)}/{nb_of_days} days on the SQL DB')

        if len(known_days) < nb_of_days :

            print(15*' ' + 'requesting Weather API...',end='')
            history = get_weatherapi_history(nb_of_days,station_id,
                                             station_coord)
            print('done')

            print(15*' ' + 'Updating SQL table...',end='')
            update_sql_station(station_id,history,known_days)
            print('done')


def get_weatherapi_history(nb_of_day, station_id, station_coord):
    """Requests weatherAPI and constitutes the weather history

    PARAMS :
    - nb_of_days : number of days of the history
    - station_id : id of the station
    - station_coord : GPS coordinates of the station

    RETURNS:
    - a pandas DataFrame of the history
    """

    # Weatherapi.com settings
    settings = dotenv_values()
    url = 'http://api.weatherapi.com/v1/history.json'
    key = settings['WA_KEY']

    # Past Days to check
    days = [
        date.today() - timedelta(delta) for delta in range(nb_of_day, 0, -1)
    ]

    dt = days[0].strftime('%Y-%m-%d')
    end_dt = days[-1].strftime('%Y-%m-%d')

    params = {'key': key, 'q': station_coord, 'dt': dt, 'end_dt': end_dt}

    response = requests.get(url, params)
    jr = response.json()
    forecasts = jr.get('forecast').get('forecastday')

    history_list = []

    for f in forecasts:

        dt = f['date']
        temp = f['day']['avgtemp_c']
        precipitation = f['day']['totalprecip_mm']
        maxwind = f['day']['maxwind_kph']
        condition = f['day']['condition']['text']

        history_list.append((dt, temp, precipitation, maxwind, condition))

    columns = [
        'day',
        'temperature',  # °C
        'precipitation',  # mm
        'maxwind',  # km/h
        'description'  # description
    ]

    history = pd.DataFrame(history_list, columns=columns)
    # converts strings to dates
    history['day'] = pd.to_datetime(history.day).dt.date
    # adds station_id column to match SQL Table
    history['station_id'] = station_id

    return history


def get_sql_known_days(nb_of_days, station_id, engine):
    """
    ARGS :
    - nb_of_days : number of days to check in the db
    - station_id : the id of the concerned station
    - engine : the sqlalchemy engine

    RETURNS :
    - the list a days (datetime.date) for which the weather is already known on this station
    """

    # Past Days to check
    days = [
        date.today() - timedelta(delta) for delta in range(nb_of_days, 0, -1)
    ]

    days = [d.strftime("%Y-%m-%d") for d in days]  # string conversion

    query = """
                SELECT day FROM weather
                WHERE station_id = :st_id AND day BETWEEN :first_day AND :last_day ;
            """

    params = {'st_id': station_id, 'first_day': days[0], 'last_day': days[-1]}

    with engine.connect() as conn:
        result = conn.execute(text(query), params)

    known_days = list(row.day for row in result)

    return known_days


def update_sql_station(history, known_days, engine):
    """
    Updates the SQL weather table for a station

    ARGS :
    - history : the weather history DataFrame of the station
    - known_days : list of days not to update, already in the table for the station
    - engine : the sqlalchemy engine
    """

    # Computes the unknown history dataframe
    unknown_bi = ~history['day'].isin(known_days)  # == day not in known_days
    unknown_history = history[unknown_bi]

    # Feed the SQL weather table with these new rows
    unknown_history.to_sql('weather', engine, if_exists='append', index=False)
