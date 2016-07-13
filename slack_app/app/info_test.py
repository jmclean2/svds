from slacker import Slacker
from flask import Flask
from model import slack_user
from flask_sqlalchemy import SQLAlchemy


class User(object):
    def __init__(self):
        self.userInfo = []
        self.table = slack_user
        self.allUsers = []
        self.names ={}

    #retrives all of the user information
    def getUserInformation(self):
        responseObject = slackconnect.users.list()
        responseMemberList = responseObject.body["members"]
        for member in responseMemberList:
            idCode = member["id"]
            profile = member["profile"]
            firstName = profile["first_name"]
            LastName = profile["last_name"]
            print(LastName)