# Description

This repo is related to the Water Pollution Project (Predict Water Pollution
of the Sâone River). For the project, we need to store the weather forecast
history in a SQL table.  

- A 10 years history has previously been retreived from weatherAPI.com (with
a paid subscription) and stored locally
- GCP SQL is choosen from the database  

- a table is created and the history loaded (see mysql_table_creation.ipnb)
- this table can be updated manually using weatherAPI.com using a free
subscription. We can access a 10 days history (see mysql_update_from_weatherAPI.ipnb)

The goal is to deploy an app in the cloud that will update the DB
on a daily basis.
