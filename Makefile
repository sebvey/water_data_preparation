# ENV VARIABLES IMPORT
include .env

## GCLOUD

gcloud_prj_select:
	@echo "SELECTING GCP PROJECT ..."
	@gcloud config set project ${GCP_PRJ_ID}

gcloud_services_enable: gcloud_prj_select
	@echo "ENABLING NEEDED APIs ..."
	@gcloud services enable cloudbuild.googleapis.com
	@gcloud services enable cloudfunctions.googleapis.com
	@gcloud services enable cloudscheduler.googleapis.com

# PUBSUB TOPIC CREATION
gcloud_topic_create: gcloud_prj_select
	@gcloud pubsub topics create db-update-topic

# FUNCTION DEPLOYMENT
gcloud_func_deploy: gcloud_prj_select gcloud_services_enable
	@echo "DEPLOYING ON GCP FUNCTIONS ..."
	@gcloud functions deploy db-update-func\
		--entry-point main\
		--runtime python39\
		--trigger-topic db-update-topic\
		--region europe-west1\
		--allow-unauthenticated

# SCHEDULER JOB CREATION / UPDATE
gcloud_job_create: gcloud_prj_select gcloud_services_enable
	@echo "CREATING SCHEDULER JOB ..."
	@gcloud scheduler jobs create pubsub db-update-job\
		--schedule "0 */6 * * *"\
		--max-retry-attempts=2\
		--topic db-update-topic\
		--location europe-west1\
		--time-zone CET\
		--message-body "Message from bd-update-job"

gcloud_job_update: gcloud_prj_select
	@echo "UPDATING SCHEDULER JOB ..."
	@gcloud scheduler jobs update pubsub db-update-job\
		--schedule "0 */6 * * *"\
		--max-retry-attempts=2\
		--location europe-west1\
		--time-zone CET\

mysql_connect: gcloud_prj_select
	@mysql -u ${SQL_USER} --password=${SQL_PWD} -h ${SQL_HOST}\
	 --ssl-ca=${SQL_SSL_CA} --ssl-cert=${SQL_SSL_CERT} --ssl-key=${SQL_SSL_KEY}
