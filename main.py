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

    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)


    ### CONFIGS

    settings = dotenv_values()  # Loads settings from .env file

    # SQL CONFIG
    
    ROOT = '..'  # relative path to the root of the project

    db_uri = (f"mysql+pymysql://{settings['SQL_USER']}:{settings['SQL_PWD']}"
            f"@{settings['SQL_HOST']}/{settings['SQL_DB']}"
            f"?ssl_ca={os.path.join(ROOT,settings['SQL_SSL_CA'])}"
            f"&ssl_cert={os.path.join(ROOT,settings['SQL_SSL_CERT'])}"
            f"&ssl_key={os.path.join(ROOT,settings['SQL_SSL_KEY'])}"
            f"&ssl_check_hostname=false")

    engine = create_engine(db_uri, echo=False, future=False)

    # WeatherAPI CONFIG

    url = 'http://api.weatherapi.com/v1/history.json'
    key = settings['WA_KEY']
