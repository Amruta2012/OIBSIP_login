from flask import Flask, render_template, redirect, url_for, session, request
from flask_mysqldb import MySQL
import bcrypt
import mysql.connector

app = Flask(__name__)
app.secret_key = 'my-secret-key'

#MySQL
'''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydatabase'
'''
connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mydatabase'
    )

#mysql = MySQL(app)



@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login_form', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = connection.cursor()
        #cursor = mysql.connection.cursor()
        cursor.execute(f"select username, password from user where username = '{username}'")
        users = cursor.fetchone()
        cursor.close()
        if users and password == users[1]:
            session['username'] = users[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error = 'invalid username or password')
    
    return render_template('login.html')


@app.route('/register_form', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = connection.cursor()
        #cursor = mysql.connection.cursor()
        cursor.execute(f"insert into users (username, password) values('{username}','{password}')")
        connection.commit()
        cursor.close()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')





if __name__ == '__main__':
    app.run(debug=True)