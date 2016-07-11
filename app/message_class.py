from datetime import datetime
from slacker import Slacker
from app import db, slackconnect
from datetime import timedelta
from app.model import message, slack_user
from flask import Flask, Request
from flask_sqlalchemy import SQLAlchemy
import collections, sys

class Message_Class(object):
    def __init__(self):
        self.ListOfMessages = []
   
    #Gets messages from Slack from since last timestamp
    def getMessageInfo(self,channel, date):
        
        responseObject = slackconnect.channels.history(channel, oldest = date)
        responseDict = responseObject.body["messages"]

        messageLogInfo = []
        for i in responseDict[0:len(responseDict)-1]:
            message = i
            text = message["text"]
            if "user" in message:
                user = message["user"]
            else:
                user = ""
            timestamp = float(message["ts"])
            timestamp = int(timestamp)
            if text is None:
                pass
            else:
                messageInfo = [user,text,timestamp,channel]
                messageLogInfo.append(messageInfo)
        return messageLogInfo

    #pushes the messages to the database
    def sendMessagesToDatabase(self, messageLogInfo):
        for mess in messageLogInfo:
            userNum = mess[0]
            text = mess[1]
            date = mess[2]
            channelNum = mess[3]

            new_message = message(date, text, userNum, channelNum)
            db.session.merge(new_message)

    #Queries for messages given the filters 
    def queryMessages(self, startDate, channelID, slackID):
        eod = startDate + 23* 59 * 59
        if (channelID  == "None" and slackID == "None"):
            messageObjects = message.query.filter(startDate < message.date_time, message.date_time <eod).all()
        elif ((channelID) == "None"):
            messageObjects = message.query.filter(startDate < message.date_time, message.date_time <eod, message.slack_number == slackID).all()
        elif (slackID == "None"):   
            messageObjects = message.query.filter(startDate < message.date_time, message.date_time <eod, message.channel_number == channelID).all()
        else:
            messageObjects = message.query.filter(startDate < message.date_time, message.date_time <eod, message.channel_number == channelID, message.slack_number == slackID).all()
        return messageObjects

    #Organizes a list of all the messages into a list of lists
    def messageList(self, messageObjects, userObjects, channel, user, theDate, channelIDNumber):
        messageStack = collections.OrderedDict()
        messagedUsers = userObjects.copy()
        
        #If user does not have any messages for selected date or channel, display a message
        if len(messageObjects) == 0:
            individualMessage = ["There are no messages on " + str(self.datetimeChange(theDate,  False))+ " in channel: " +
            channel, "", "", ""]
            messageStack['none'] = individualMessage

            return messageStack
        else: 
            for mess in messageObjects:
                #Channel number, text, and date from message table
                channelNum = mess.channel_number
                messageText = mess.msg
                messageDate = mess.date_time
                messageUserID = mess.slack_number

                slackUserID = slack_user.query.filter(slack_user.slack_number == messageUserID).all()
                #Accounts for bug that occurs due to bot that posts to trains channel
                if len(slackUserID) == 0:
                    userName = 'BOT'
                else:
                    userName = slackUserID[0].first_name + " " + slackUserID[0].last_name

                if(userName in messagedUsers):
                    del(messagedUsers[userName])

        #Query the message_channel table to find the channel name
                channelName = channelIDNumber[channelNum]
                messageDate = self.datetimeChange(messageDate, True)
              
                #append Message
                individualMessage = [messageText, channelName, messageDate, userName]
                #print("uxers  " + str(individualMessage), file=sys.stderr)
                
                if userName in messageStack.keys():
                    #item = messageStack[userName] + individualMessage
                    messageStack[userName].append(individualMessage)
                    #messageStack.update({userName : item}) 
                else:
                    messageStack[userName] = individualMessage
               # print(' THis is the message stack ' + str(messageStack), file=sys.stderr)
            #Checking if the selection for users was 'all' and adding thoose who never commented 
            #in that channel for the day
            if (user == 'None'):
                for theUser in messagedUsers:
                     individualMessage = [" ", channel, " ", theUser]
                     messageStack[theUser] = individualMessage
            #dictionary with first and other
            #first holds an array with all the info, other holds an array of arrays with all the info
                #if already entered into database then add to an array of arrays for other messages 
            else: pass
            #messageStack = messageStack.sort()
            
            return messageStack

    #converts timestamp to datetime
    def datetimeChange(self, timestamp, seconds):
        date = datetime.fromtimestamp(float(timestamp))
        if(seconds):
            return date.strftime('%-I:%M:%S %p')
        else:
            return date.strftime('%m/%d/%Y')