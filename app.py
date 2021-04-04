from flask import Flask, render_template, flash, redirect, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '*******'
app.config['MYSQL_DB'] = 'crypto'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return "Hello BlockTrain!"

@app.route('/register', methods['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration_form.html')
    elif request.method == 'POST':
        return register_user(request.form['username'], request.form['password'])

def register_user(username, password):
    # check if username exists, if so return error

    # add username and password to db



if __name__ == '__main__':
    app.secret_key = 'dank1234'
    app.run(debug = True)