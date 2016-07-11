from flask import render_template, redirect, session, url_for, request
from datetime import datetime, date, timedelta
from app import app, db
from app.model import slack_user, message_channel, message
from app.channel import Channel
from app.user import User
from app.message_class import Message_Class
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import SelectMultipleField, SubmitField, DateField, SelectField
from sqlalchemy import desc
from flask_wtf import Form
from wtforms import DateField
import time

#GLOBAL VARIABLES
usr = User()
ch = Channel()
#Querying the database for all exsisting users and chanels, 
#then returning them as an ordered dictionary
allUserData = usr.userList()
allChannelData = ch.channelList()

#Formating dictionaries into a list of tuples for dropdown fields
def formatDataForDropdown(dataDictionary):
    avaliableSelections = [('None', 'All')]
    for key in dataDictionary:
        selection = (key, key)
        avaliableSelections.append(selection)
    return avaliableSelections


#Form class that holds information on dt(Date FIeld), user and channel fields.
class Select2TagForm(Form):
    dataUser = usr.names
    userOptions = formatDataForDropdown(dataUser)

    dataChannel = ch.allChannels
    channelOptions = formatDataForDropdown(dataChannel)
    userChoice = SelectField(u'Select User: ', choices = userOptions)
    channelChoice = SelectField(u'Select Channel: ', choices = channelOptions)
    dt = DateField('Pick a Date', format="%m/%d/%Y")


# #Updates tables that need to be updated before loading a page
# def before_Pageload():
#     #Initilizing chanel, user and message objects
#     cha = Channel()
#     usa = User()
#     msg = Message_Class() 
#     #Calling slack api for new information
#     channels = cha.getChannelInfo()
#     users = usa.getUserInformation()

#     #Querying the database for all users
#     userQuery = slack_user.query.all()
#     #Comparing information from slack and query from databse, to see if an update is needed
#     if (len(userQuery) < len(users)) :
#         #Insert users in the user table
#         usa.sendUsersToDatabase(False) 
#     #Querying the database for all channels
#     channelQuery = message_channel.query.all()
#     #Comparing information from slack and query from databse, to see if an update is needed
#     if (len(channelQuery) < len(channels)) :
#         # Insert channels in the channel table
#         cha.sendChannelsToDatabase(False) 
    
#     #Querying the message table for the last date time a message was posted
#     lastMessageTimestamp = message.query.order_by(desc(('date_time'))).first()
#     if lastMessageTimestamp == None:
#         #convert date to a timestamp
#         dateTimeToday = date.today()
#         lastMessageTimestamp =  dateTimeToday.strftime('%s')
#         lastMessageTimestamp = int(lastMessageTimestamp)
#     else:
#         lastMessageTimestamp = lastMessageTimestamp.date_time
#     #Get messageObjects from slack and send them to the database
#     for channelIdNumber in channelQuery:
#         slackMessages = msg.getMessageInfo(channelIdNumber.channel_number, lastMessageTimestamp)
#         #Insert messages in the the message table

#         if(slackMessages != None):
#             msg.sendMessagesToDatabase(slackMessages)
#     #Commit the inserts
#     db.session.commit() 


#Returns the selection choices for date, time and user and handles no entry
def loadChoices(form):
    #before_Pageload()
    #Checking if no date entered, Display current date as default
    if (form.dt.data != None):
        theDate = form.dt.data.strftime('%s') 
        theDate = int(theDate)
    else:
        dateTimeToday = date.today()
        theDate =  dateTimeToday.strftime('%s')
        theDate = int(theDate)
    #Checking if no user has been selected
    if (form.userChoice.data != 'None') :
        submittedUser = form.userChoice.data
        userID = allUserData[submittedUser]
    else:
        submittedUser = 'None'
        userID = 'None'
    #Checks if a channel has been selected
    if(form.channelChoice.data != 'None'):
        submittedChannel = form.channelChoice.data
        channelID = allChannelData[submittedChannel]
    else:
        submittedChannel = 'None'
        channelID = 'None'
    choices = [theDate, channelID, userID, submittedChannel, submittedUser]
    return choices


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST','GET'])
def index():
    form = Select2TagForm(request.form)
    #Create a new form with user, date and channel fields
    selectionChoices = loadChoices(form)
    #call for messages from database (DATE TIME, CHANNEL IDENTIFICATION, USER IDENTIFICATION)
    messageObjects = Message_Class().queryMessages(selectionChoices[0],selectionChoices[1], 
        selectionChoices[2])
    
    #Takes array of messages, userInformation(GLOBAL VARIABLE), channel selection, user 
    #selection date selection and dict of channelIDS. Orders them into a list of lists
    messageStack = Message_Class().messageList(messageObjects, allUserData,
        selectionChoices[3], selectionChoices[4], selectionChoices[0], ch.reverseChannelLookup)

    #returns a render template object to pass items onto html templates
    return render_template('index.html', title="User Directory", messageInfo = messageStack,
        form =form, user = selectionChoices[4])
