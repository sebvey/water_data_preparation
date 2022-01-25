# Description

This repo is related to the Water Pollution Project (Predict Water Pollution
of the Sâone River). For the project, we need to store :
- the weather forecast history from weatherapi.com in a SQL table
- the stations information in a SQL table (a station is where the water quality
is measured)

This SQL DB is first filled with data previously constituted and 
stored locally.  

The daily update of the SQL weather table is needed. For that purpose :
- A GCP Function is coded and deployed.
- A Cloud Scheduler Job is created to trigger this function daily.  

# Cloud SQL Tables Creation 
The code is presented in the
[mysql_table_creation.ipynb](notebooks/mysql_table_creation) notebook.
This notebook shows how the sql table were created and populated :
- a stations table, with information on the stations
- a weather table, with the 10 years history of the weather forecast

# Update for the SQL weather Table with Weatherapi.com (manual)
The code is presented in the
[mysql_update_from_weatherapi.ipynb](notebooks/mysql_update_from_weatherapi.ipynb) notebook.
This notebook shows how to update the SQL weather table :
- We access a 10 days history from weatherapi.com (free subscription)
- We check what needs to be updated the SQL weather table
- we update the SQL table

# Cloud Function for Automatic Updates

## main.py
This is the implementation of the Cloud Function. The code of the previous
notebook is adapted.

## Makefile
It shows the workflow to :
- create a Pub/Sub topic
- deploy/update the Cloud Function
- create and update the Scheduler Job
- manually trigger the function (manually run the job)
