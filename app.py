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

#Read
@app.route('/')
def index():
    """Homepage"""
    return render_template('debate_home.html', arguments1=arguments.find({'optradio':'argument1'}),arguments2=arguments.find({'optradio':'argument2'}))
#Create Call
@app.route('/arguments/new')
def argumentss_new():
    """Creating new argument point."""
    return render_template('arguments_new.html', argument={}, name='New Argument')

#Actually Creating --------------------------
@app.route('/arguments', methods=['POST'])
def arguments_submit():
    """Submit a new Argument point."""
    argument ={
        'title': request.form.get('title'),
        'point': request.form.get('point'),
        'optradio': request.form.get('optradio')
    }
    print(argument['optradio'])
    arguments.insert_one(argument)
    #argument_id = arguments.insert_one(argument).inserted_id
    return redirect(url_for('index'))

#Update
#Destroy
if __name__=='__main__':
    app.run()
