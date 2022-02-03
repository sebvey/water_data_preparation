# Description

This repo is related to the Water Pollution Project (Predict Water Pollution
of the Sâone River). For the project, we need to store in a SQL DB :
- the weather forecast history from weatherapi.com
- the stations information (a station is where the water quality
is measured)
- the Nitrates History from 2011 to 2021 measured on each station in a SQL table
(Nitrates is a good indicator of water pollution, the main goal is to predict
this indicator)

This SQL DB is first filled with data previously constituted and 
stored locally. 

The daily update of the SQL weather table is needed. For that purpose :
- A GCP Function is coded and deployed.
- A Cloud Scheduler Job is created to trigger this function daily.  

# Nitrates data extraction and cleaning
The code is presented in the 
[nitrate_data_preparation](notebooks/nitrate_data_preparation.ipynb)
notebook.  
The data is extracted from Naïades (french government website that gather water
quality information). The data is then cleaned.

# Cloud SQL Tables Creation 
The code is presented in the
[mysql_table_creation](notebooks/mysql_table_creation.ipynb) notebook.
This notebook shows how the sql table were created and populated :
- a stations table, with information on the stations
- a weather table, with the ~10 years history of the weather forecast
- a nitrates table, with the ~10 years history of the nitrates measurement

# Update for the SQL weather Table with Weatherapi.com (manual)
The code is presented in the
[mysql_update_from_weatherapi](notebooks/mysql_update_from_weatherAPI.ipynb) notebook.
This notebook shows how to update the SQL weather table :
- We access a 10 days history from weatherapi.com (free subscription)
- We check what needs to be updated the SQL weather table
- we update the SQL table

# Cloud Function for Automatic Updates

## [main.py](main.py)
This is the implementation of the Cloud Function. The code of the previous
notebook is adapted.

## [Makefile](Makefile)
It shows the workflow to :
- create a Pub/Sub topic
- deploy/update the Cloud Function
- create and update the Scheduler Job
- manually trigger the function (manually run the job)
