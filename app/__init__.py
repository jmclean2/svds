import os, configparser
import os.path
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from slacker import Slacker
from flask_bootstrap import Bootstrap

dir = os.path.dirname(__file__)
config_file_name = os.path.join(dir, '../config/config_file.cfg')

app = Flask(__name__, instance_path=config_file_name)
#app.config.from_object('config')
app.route
Bootstrap(app)
db = SQLAlchemy(app)

app.config.from_pyfile(config_file_name)
app.config['SQLALCHEMY_DATABASE_URI']
app.config['CSRF_ENABLED']
app.config['SECRET_KEY']
app.config['DEBUG']

slackconnect = Slacker(app.config['SLACK_API_TOKEN'])

from app import views
from app.channel import Channel
from app.user import User
from app.message_class import Message_Class
from app.model import slack_user, message_channel, message