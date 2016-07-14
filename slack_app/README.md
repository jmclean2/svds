# Slack-Application
 Search through messages on a slack team via users, dates and channels.
   - Works on all channels and users, starting from the day the program is implemented.

## Setup:

 -Config.py in config directory takes a web-api Oauth2 token from slack.com.
 	- Database and username "mysql://USERNAME:PASSWORD@HOST/DATABASE". One can use any database supported by sqlalchemy.
 	- Think of a random SQLalchemy secret key
 
 - Run the table_creator_script.py to generate and initialy populate the necesary  tables.

 - Setup a cron-job to execute update_database_information.py every minute or so. 

 - Run "python run.py" to start the program. Web app will run at 127.0.0.1:5000 on your local machine.

 ## Setup (not required):
 	- Run the web app on ngrok --> Go to www.ngrok.com and follow directions.

## Notes:
 A bug occansionally occurs where the default character set is Latin 1. To change this copy the create statement for the 'message' table, drop the 'message' table and change the default character set to utf8mb4. Run the create table query.

 TRUE was changed from NONE in ~/python3.5/site-packages/flask_sqlalchemy/__init__.py
 	- Gets rid of unwanted messages while debugging
 Was tested on Python 3.5, mysql 5.5 and anacondaEnv


