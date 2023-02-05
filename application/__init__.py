from flask import Flask,jsonify, make_response, render_template, request, redirect, url_for,session
from matplotlib.style import use
import pymysql
#import 
import json
import pandas as pd
from datetime import datetime
# Import Blueprint
from .komplek.controllers import komplek
app = Flask(__name__)
app.debug = True

# Koneksi ke database MySQL
mydb = pymysql.connect(
	host="localhost",
	user="root",
	passwd="",
	database="smart_barrier_1"
)
app.secret_key = '12345678'

# Buat root path untuk project flask, biar gak error 404B
@app.route("/",methods=['GET','POST'])
def index():
    return render_template("login.html")

@app.route("/login",methods=['GET','POST'])
def login():
      
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM tb_admin WHERE username = %s AND password = %s", (username, password))
        # Fetch one record and return result
        data = mycursor.fetchone()
        # login dengan variable sesuai row
        # saat query select dijalankan, fungsinya untuk cek kondisi apakah ada data yang ditemukan/cocok dengan inputan user (email & passwordnya)
        rc = mycursor.rowcount
        # lalu buat kondisi untuk cek jika row yang didapat lebih dari 0 (ada datanya)
        if  rc > 0:
            #barulah buat session 
            print("berhasil")
            session['loggedin'] = True
            session['username'] = data[0]
            session['password'] = data[1]
            # Create session data, we can access this data in other routes
            # Redirect to home page
            return redirect(url_for('komplek.dashboard_view'))
        else:
            # Account doesnt exist or username/password incorrect
            return render_template('login.html', msg = True)
        
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    #    session['loggedin'] = False
    #    session.pop('username', None)
    #    session.pop('password', None)
    #  function clear 
   session.clear()
   # Redirect to login page
   return redirect(url_for('index'))
app.register_blueprint(komplek, url_prefix='/komplek')
