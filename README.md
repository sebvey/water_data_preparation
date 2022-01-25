# Description

This repo is related to the Water Pollution Project (Predict Water Pollution
of the Sâone River). For the project, we need to store :
- the weather forecast history from weatherapi.com in a SQL table
- the stations information in a SQL table (a station is where the water quality
is measured)

This SQL DB is first constituted with data previously constituted and 
stored locally.  

The daily update of the SQL weather table is needed. For that purpose,
a GCP Function is coded and deployed. A Cloud Scheduler Job is created to
trigger this function daily.  


# mysql_table_creation.ipynb notebook
This notebook shows how the sql table were created :
- a stations table, with information on the stations
- a weather table, with the 10 years history of the weather forecast


# mysql_update_from_weatherapi.ipynb
This notebook shows how to update the SQL weather table :
- We access a 10 days history from weatherapi.com (free subscription)
- We check what needs to be updated the SQL weather table
- we update the SQL table

# main.py
This is the implementation of the Cloud Function. The code of the notebook is
adapted.

# Makefile
It shows the workflow to :
- create a Pub/Sub topic
- deploy/update the Cloud Function
- create and update the Scheduler Job
- manually trigger the function (manually run the job)
