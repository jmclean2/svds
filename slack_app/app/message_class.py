from datetime import datetime
from slacker import Slacker
from app import db, slackconnect
from datetime import timedelta
from app.model import message, slack_user
from flask import Flask, Request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import collections, sys

class Message_Class(object):
    def __init__(self):
        self.ListOfMessages = []

    #Gets messages from Slack from since last timestamp
    def getMessageInfo(self,channel, date):
        responseObject = slackconnect.channels.history(channel, oldest = date, inclusive = 0)
        responseDict = responseObject.body["messages"]
        messageLogInfo = []
        #duplicate messages
        latestMessage = message.query.order_by(desc(message.date_time)).first()
        loopLength = len(responseDict)
        if latestMessage != None and loopLength >0 and latestMessage.msg == responseDict[loopLength-1]["text"]:
            #there is a repeat message so get rid of extra entry
            loopLength -=1

        for i in responseDict[0:loopLength]:
            mess = i
            text = mess["text"]
            text = self.textConverter(text)
            if "user" in mess:
                user = mess["user"]
            else:
                user = ""
            timestamp = float(mess["ts"])
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
                if (userName == ""):
                    pass
                elif userName in messageStack.keys():
                    messageStack[userName].append(individualMessage)

                else:
                    messageStack[userName] = individualMessage
            if (user == 'None'):
                for theUser in messagedUsers:
                     individualMessage = [" ", channel, " ", theUser]
                     messageStack[theUser] = individualMessage
            else: pass

            #Entries are displayed in alphabetical order
            alphabeticalDict = collections.OrderedDict(sorted(messageStack.items(), key=lambda t: t[0]))

            return alphabeticalDict

    #modifies text to display actual usernames and channels instead of ids
    def textConverter(self, text):
        i = 0;
        revisedText = text
        if text is not None and len(text) >9:

            while i < len(revisedText) -8:
                string = revisedText[i]+revisedText[i+1]
                if string == '<@' and revisedText[i+11] == '>':
                    username = revisedText[i+2:i+11]
                    user = slack_user.query.filter(slack_user.slack_number == username).all()
                    if len(user) != 0:
                        name = user[0].first_name + " " + user[0].last_name
                        userNamelength = len(name)
                        #adds space to end of comment to get around bug
                        #revisedText = revisedText + " "
                        revisedText = revisedText[:i] + name + revisedText[i+12:]
                        i = i + 1 + userNamelength -1
                    else:
                        i+=1
                elif string == '<#' and revisedText[i+11] == '>':
                    channelID = revisedText[i+2:i+11]
                    channel = message_channel.query.filter(message_channel.channel_number == channelID).all()
                    if len(user) != 0:
                        channelName = channel[0].channel_name
                        channelNamelength = len(channelName)
                        #adds space to end of comment to get around bug
                        #revisedText = revisedText + " "
                        revisedText = revisedText[:i] + channelName + revisedText[i+12:]
                        i = i + 1 + channelNamelength -1
                    else:
                        i+=1
                else:
                    i+=1
        return revisedText


    #converts timestamp to datetime
    def datetimeChange(self, timestamp, seconds):
        date = datetime.fromtimestamp(float(timestamp))
        if(seconds):
            return date.strftime('%-I:%M:%S %p')
        else:
            return date.strftime('%m/%d/%Y')