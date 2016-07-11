from slacker import Slacker
from flask import Flask
from app.model import slack_user
from app import app, db, slackconnect
from flask_sqlalchemy import SQLAlchemy


class User(object):
    def __init__(self):
        self.userInfo = []
        self.table = slack_user
        self.allUsers = []
        self.names ={}

    #retrives user information through slack web-api call
    def getUserInformation(self):
        #Api call for all of the users
        responseObject = slackconnect.users.list()
        responseMemberList = responseObject.body["members"]
        for member in responseMemberList:
            idCode = member["id"]
            profile = member["profile"]
            firstName = ""
            if "first_name" in profile:
                firstName = profile["first_name"]
            lastName = ""
            if "last_name" in profile:
                lastName = profile["last_name"]
            memberInfo = [idCode, firstName, lastName]
            self.userInfo.append(memberInfo)
        return self.userInfo

    #pushes all of the users to a database
    def sendUsersToDatabase(self, populate):
        
        for user in self.userInfo:
            userNum = user[0]
            userFirst = user[1]
            userLast = user[2]

            new_user = slack_user(userNum, userFirst, userLast)
            if populate:
                db.session.add(new_user)
            else:
                db.session.merge(new_user)

    #Queries the database for all of the users
    def userList(self):
        query = self.table.query.all()
        for user in query:
            userID = user.slack_number
            userFirst = user.first_name
            userLast = user.last_name
            name = ""
            if (userFirst != None and userLast != None):
                name = userFirst + " " + userLast
            
            # added .title() after name to capitalize the first letter of fn and ln
            self.names[name] = userID
        return self.names