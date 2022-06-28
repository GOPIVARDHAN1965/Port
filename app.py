from base64 import encode
from crypt import methods
from encodings import utf_8
import bcrypt
from flask import Flask, flash, redirect, render_template, request, session, url_for
import pymongo


app = Flask(__name__, template_folder="template")

try:
    mongo = pymongo.MongoClient(
        host = "localhost",
        port = 27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.port
    mongo.server_info()
except:
    print("Error connecting to the DB")


# @app.route('/')
# def index():
#     if 'user_id' in session:
#         return 'Your are logged in as '+session['user_id']
#     return render_template('login.html')

@app.route('/', methods=['POST','GET'])
def login():
    if request.method=='POST':
        users = db.users
        login_user = users.find_one({'user_id': request.form['user_id']})
        if login_user:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['user_id'] = request.form['user_id']
                return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/regsiter',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'user_id': request.form['user_id']})
        if existing_user is None:
            if request.form['pass'] == request.form['pass2']:
                hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'),bcrypt.gensalt())
                users.insert_one({'user_id': request.form['user_id'], 'password': hashpass })
                session['user_id'] = request.form['user_id']
                return redirect(url_for('home'))
            else:
                return "Both passwords must be same!" 
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    return render_template('login.html')

@app.route('/change-password')
def change_password():
    pass

if __name__ == "__main__":
    app.secret_key = 'donjon'
    app.run(debug=True)