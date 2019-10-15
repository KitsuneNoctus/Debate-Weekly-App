#Fall 2019 Intensive 1.1 - Henry Calderon
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import os
#Project Name: Debate Weekly
client = MongoClient()
#db = client.get_default_database()
db = client.Arguments
arguments = db.arguments


app = Flask(__name__)

@app.route('/')
def index():
    """Homepage"""
    return render_template('debate_home.html')

#Create
#Read
#Update
#Destroy
if __name__=='__main__':
    app.run()
