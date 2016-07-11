from app.model import slack_user, message_channel, message
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

from app.message_class import Message_Class
from app.user import User
from app.channel import Channel

from app import db

def main():
	ch = Channel()
	usr = User()
	channels = ch.getChannelInfo()
	people = usr.getUserInformation()
	#messagesForAllChannels = []
	#for chan in channels:
	#	mes =  getMessageinfo(chan)
	#	messagesForAllChannels.append(mes)


	insertData(people, channels)

def insertData(users, channels):
	db.create_all()

	ch = Channel()
	usr = User()
	ch.getChannelInfo()
	usr.getUserInformation()
	ch.sendChannelsToDatabase(True) 
	usr.sendUsersToDatabase(True)
	db.session.commit()  

if __name__ == '__main__':
	main()