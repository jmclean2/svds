from app.model import slack_user, message_channel, message
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import datetime
from sqlalchemy import desc
from app.message_class import Message_Class
from app.user import User
from app.channel import Channel

from app import db
from app.views import ch, usr

class updateDatabase(object):
	def __init__(self, channel, user):
		self.channel = channel
		self.user = user

	def before_Pageload(self):
	    #Initilizing chanel, user and message object
	    msg = Message_Class() 
	    #Calling slack api for new information
	    channels = self.channel.getChannelInfo()
	    users = self.user.getUserInformation()

	    #Querying the database for all users
	    userQuery = slack_user.query.all()
	    #Comparing information from slack and query from databse, to see if an update is needed
	    if (len(userQuery) < len(users)) :
	        #Insert users in the user table
	        self.user.sendUsersToDatabase(False) 
	    #Querying the database for all channels
	    channelQuery = message_channel.query.all()
	    #Comparing information from slack and query from databse, to see if an update is needed
	    if (len(channelQuery) < len(channels)) :
	        # Insert channels in the channel table
	        self.channel.sendChannelsToDatabase(False) 
	    
	    #Querying the message table for the last date time a message was posted
	    lastMessageTimestamp = message.query.order_by(desc(('date_time'))).first()
	    if lastMessageTimestamp == None:
	        #convert date to a timestamp
	        dateTimeToday = datetime.date.today()
	        lastMessageTimestamp =  dateTimeToday.strftime('%s')
	        lastMessageTimestamp = int(lastMessageTimestamp)
	    else:
	        lastMessageTimestamp = lastMessageTimestamp.date_time
	    #Get messageObjects from slack and send them to the database
	    for channelIdNumber in channelQuery:
	        slackMessages = msg.getMessageInfo(channelIdNumber.channel_number, lastMessageTimestamp)
	        #Insert messages in the the message table

	        if(slackMessages != None):
	            msg.sendMessagesToDatabase(slackMessages)
	    #Commit the inserts
	    db.session.commit() 


if __name__ == '__main__':
	update = updateDatabase(ch, usr)
	update.before_Pageload()