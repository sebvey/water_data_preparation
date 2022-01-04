# ENV VARIABLES IMPORT
include .env

mysql_connect:
	@mysql -u ${SQL_USER} --password=${SQL_PWD} -h ${SQL_HOST}\
	 --ssl-ca=${SQL_SSL_CA} --ssl-cert=${SQL_SSL_CERT} --ssl-key=${SQL_SSL_KEY}
