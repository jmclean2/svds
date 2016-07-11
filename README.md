# Slack-Application
 Search through messages on a slack team via users, dates and channels.
   - Works on all channels and users, starting from the day the program is implemented.

## Setup:

 -Config.py in instance directory takes a web-api Oauth2 token from slack.com.
 	- Database and username "mysql://USERNAME:PASSWORD@HOST/DATABASE". One can use any database supported by sqlalchemy.
 	- Think of a random SQLalchemy secret key
 
 - Run the table_creator_script.py to generate and initialy populate the necesary  tables.

 - Setup a cron-job to execute update_database_information.py every 45 seconds or so. 

 - The program will either run on a production or development enviroment. Default is production but this can be changed in defining which configuration file is read in __init__.

 - Run "bash start.sh" to start the program. Web app will run at 127.0.0.1:5000 on local machine.

 ## Setup (not required):
 	- Run the web app on ngrok --> Go to www.ngrok.com and follow directions.

## Notes:
 TRUE was changed from NONE in ~/python3.5/site-packages/flask_sqlalchemy/__init__.py
 	- Gets rid of unwanted messages while debugging
 Run on Python 3.5, mysql 5.5 and anacondaEnv


