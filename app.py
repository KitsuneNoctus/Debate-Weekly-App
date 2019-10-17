#Fall 2019 Intensive 1.1 - Henry Calderon
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import os
#Project Name: Debate Weekly
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Debate')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
#db = client.Arguments
arguments = db.arguments


app = Flask(__name__)

#Read
@app.route('/')
def index():
    """Homepage"""
    return render_template('debate_home.html', arguments1=arguments.find({'optradio':'argument1'}),arguments2=arguments.find({'optradio':'argument2'}))
#Create Call
@app.route('/arguments/new1')
def arguments_new1():
    """Creating new argument point."""
    opt_choice = 'argument1'
    return render_template('arguments_new.html', argument={}, name='New Argument', opt_choice=opt_choice)

@app.route('/arguments/new2')
def arguments_new2():
    """Creating new argument point."""
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
    arguments.insert_one(argument)
    #argument_id = arguments.insert_one(argument).inserted_id
    return redirect(url_for('index'))

#Update
@app.route('/arguments/<argument_id>/edit')
def arguments_edit(argument_id):
    argument = arguments.find_one({'_id' : ObjectId(argument_id)})
    return render_template('arguments_edit.html',argument=argument)


@app.route('/arguments/<argument_id>', methods=['POST'])
def arguments_update(argument_id):
    update_argument={
        'title': request.form.get('title'),
        'point': request.form.get('point'),
        'optradio': request.form.get('optradio')
    }
    arguments.update_one({'_id':ObjectId(argument_id)},{'$set': update_argument})
    return redirect(url_for('index'))

#Destroy
@app.route('/arguments/<argument_id>/delete')
def arguments_delete(argument_id):
    arguments.delete_one({'_id':ObjectId(argument_id)})
    return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
