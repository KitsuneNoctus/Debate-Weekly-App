#Fall 2019 Intensive 1.1 - Henry Calderon
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for
# from oauth2client import client
from bson.objectid import ObjectId
import os
#Project Name: Debate Weekly
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Debate')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
#db = client.Arguments
arguments = db.arguments
comments = db.comments
users = db.users


app = Flask(__name__)

#Read
@app.route('/')
def index():
    """Homepage: Displays everything"""
    # argument_comments = comments.find({'argument_id': ObjectId(argument_id)})
    return render_template('debate_home.html', arguments1=arguments.find({'optradio':'argument1'}),arguments2=arguments.find({'optradio':'argument2'}),comments=comments.find())
#Create Call
@app.route('/arguments/new1')
def arguments_new1():
    """Link to create a new argument for the pro side"""
    opt_choice = 'argument1'
    return render_template('arguments_new.html', argument={}, name='New Argument', opt_choice=opt_choice)

@app.route('/arguments/new2')
def arguments_new2():
    """Link to create a new argument for the con side"""
    opt_choice = 'argument2'
    return render_template('arguments_new.html', argument={}, name='New Argument',opt_choice=opt_choice)

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
    argument_id = arguments.insert_one(argument).inserted_id
    #argument_id = arguments.insert_one(argument).inserted_id
    return redirect(url_for('index',argument_id=argument_id))

#Update
@app.route('/arguments/<argument_id>/edit')
def arguments_edit(argument_id):
    """Update argument point if needed"""
    argument = arguments.find_one({'_id' : ObjectId(argument_id)})
    return render_template('arguments_edit.html',argument=argument)


@app.route('/arguments/<argument_id>', methods=['POST'])
def arguments_update(argument_id):
    """Takes in the updated info"""
    update_argument={
        'title': request.form.get('title'),
        'point': request.form.get('point'),
        'optradio': request.form.get('optradio')
    }
    arguments.update_one({'_id':ObjectId(argument_id)},{'$set': update_argument})
    return redirect(url_for('index',argument_id=argument_id))
#
#Destroy
@app.route('/arguments/<argument_id>/delete')
def arguments_delete(argument_id):
    """Delete an argument you don't want anymore"""
    arguments.delete_one({'_id':ObjectId(argument_id)})
    return redirect(url_for('index'))

#========================================================================
#-------Comments--------------
@app.route('/arguments/comments', methods=['POST'])
def comments_new():
    comment={
        'content': request.form.get('content'),
        'argument_id': ObjectId(request.form.get('argument_id'))
    }
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('index'))

#Delete a Comment ----------------------------------------
@app.route('/arguments/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('index'))

#=========================================================================
@app.route('/login/new_user')
def sign_up():
    return('login.html')
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    """To open a login page for users"""
    # Used code from here initially
    # https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
