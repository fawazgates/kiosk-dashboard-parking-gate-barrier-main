from cProfile import label
from flask import Flask,jsonify, make_response, render_template, request, redirect, url_for,session,Blueprint
import pymysql
import json
import pandas as pd
from datetime import datetime
komplek = Blueprint('komplek', __name__,template_folder='templates',static_folder='static',url_prefix='/komplek')
# Koneksi ke database MySQL
mydb = pymysql.connect(
	host="localhost",
	user="root",
	passwd="",
    port=3306,
	database="smart_barrier_1"
)
########################### Record Data Fitur#######################################################
@komplek.route("/get_record_data",methods=['GET'])
def record():
    # Awal Query
	query = "SELECT * FROM tb_record"
	values = ()

	# Mengatur Parameter
	nama = request.args.get("nama")
	rfid = request.args.get("rfid")
	alamat = request.args.get("alamat")

	if nama:
		query += " AND nama LIKE %s "
		values += (nama,)
	if rfid:
		query += " AND rfid=%s " 
		values += ("%"+rfid+"%", )
	if alamat:
		query += " AND alamat LIKE %s "
		values += (alamat,)

	mycursor = mydb.cursor()
	mycursor.execute(query, values)
    #print(mycursor.description)
	row_headers = [x[0] for x in mycursor.description]
	data = mycursor.fetchall()
	json_data = []
	print(row_headers)
	for result in data:
		json_data.append(dict(zip(row_headers, result)))
	print(json_data)
	return json.dumps(json_data)

@komplek.route('/record',methods=['GET'])
def get_data():
    url = 'http://localhost:5000/komplek/get_record_data'
    #headers = {}
    #response = requests.request('GET',url)
    df = pd.read_json(url)
    records = df.to_dict('records')
    columnNames = df.columns.values
    #print(columnNames[0])
    return render_template('komplek/record.html', records=records, colnames=columnNames)
########################### Register Data Fitur#######################################################
@komplek.route('/insert_data_regis', methods=['GET','POST'])
def insert_data_regis():
    msg = ''
    if request.method == 'POST' and 'nama' in request.form and 'rfid' in request.form and 'alamat' in request.form:
        nama = request.form['nama']
        rfid = request.form['rfid']
        alamat = request.form['alamat']
        print(nama,rfid,alamat)
        mycursor = mydb.cursor()
        mycursor.execute('INSERT INTO tb_record VALUES (%s, %s, %s)', (nama, rfid, alamat,))
        mydb.commit()
        msg = 'Berhasil Terdaftar!'
    elif request.method == 'POST':
        msg = 'Gagal!'
    print(msg)
    return redirect(url_for('.get_data'))

@komplek.route("/register",methods=['GET','POST'])
def register():
    return render_template("/komplek/register.html")
########################### Register Admin Data Fitur#######################################################
@komplek.route('/insert_data_regis_admin', methods=['GET','POST'])
def insert_data_regis_admin():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        mycursor = mydb.cursor()
        mycursor.execute('INSERT INTO tb_admin VALUES (%s, %s)', (username,password))
        mydb.commit()
        msg = 'Berhasil Terdaftar!'
    elif request.method == 'POST':
        msg = 'Gagal!'
    print(msg)
    return render_template("komplek/register_admin.html")

@komplek.route("/register_admin",methods=['GET','POST'])
def register_admin():
    return render_template("/komplek/register_admin.html")
########################### Edit Data Fitur#######################################################
@komplek.route("/edit_data_record/<rfid>",methods=['POST','GET'])
def edit_data(rfid):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM tb_record WHERE rfid = %s', (rfid))
    data = mycursor.fetchall()
    mycursor.close()
    return render_template('komplek/edit.html', record=data[0])

@komplek.route("/update_data_record/<rfid>", methods=['POST'])
def update_data(rfid):
    if request.method == 'POST':
        nama = request.form['nama']
        alamat = request.form['alamat']
        mycursor = mydb.cursor()
        query = 'UPDATE tb_record SET nama = %s, alamat = %s WHERE rfid = %s'
        values = (nama,alamat,rfid)
        mycursor.execute(query,values)
        print('Update Succes')
        mydb.commit()
        return redirect(url_for('.get_data'))
########################### Dashboard Data Fitur#######################################################
@komplek.route("/get_dashboard_data", methods=['GET'])
def dashboard_data():
    # Awal Query
    query = "SELECT * FROM tb_visitor ORDER BY tanggal DESC, jam DESC"
	# Mengatur Parameter
    values = ()
    mycursor = mydb.cursor()
    mycursor.execute(query, values)
    #print(mycursor.description)
    row_headers = [x[0] for x in mycursor.description]
    data = mycursor.fetchall()
    json_data = []
    print(row_headers)
    for result in data:
        json_data.append(dict(zip(row_headers, result)))
    print(json_data)
    return json.dumps(json_data, indent=4, sort_keys=False, default=str)

@komplek.route('/dashboard',methods=['GET', 'POST'])
def dashboard_view():
    url = 'http://localhost:5000/komplek/get_dashboard_data'
    df = pd.read_json(url)
    dashboards = df.to_dict('records')
    columnNames = df.columns.values
    print(dashboards)
    print(columnNames[0])
    # kondisi untuk cek session apakah session loggedin valuenya true atau tidak
    # jika iya maka arahkan ke dashboard
    if session.get('loggedin') == True:
        return render_template('/komplek/dashboard.html', dashboards=dashboards, colnames=columnNames)
    # sedangkan jika tidak maka arahkan kembali ke root yaitu index(login)
    else:
        return redirect(url_for('index'))
########################### Endpoint Data Fitur #######################################################
@komplek.route('/visitor_in/<rfid>',methods=['GET','POST'])
def visitor_in(rfid):
    now = datetime.now()
    msg = ''
    rfid = request.form['rfid']
    photo = request.form['photo']
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM tb_record WHERE rfid = %s', (rfid))
    #query = "SELECT * FROM tb_visitor"
    if request.method == 'POST' and 'rfid' and 'photo' in request.form:
        rfid = request.form['rfid']
        data = mycursor.fetchall() 
        record = data[0]
        #print(record[0])
        nama = record[0]
        alamat = record[2]
        #print(alamat)
        tanggal =  now.strftime("%d/%m/%Y")
        jam = now.strftime("%H:%M:%S")
        status = 'masuk'
        photo = request.form['photo']
        #photo = str(photo)
        #print(photo)
        mycursor.execute('INSERT INTO tb_visitor(nama, rfid, alamat,tanggal,jam,status,photo) VALUES (%s, %s, %s,%s,%s,%s,%s)', (nama, rfid, alamat,tanggal,jam,status,photo))
        mydb.commit()
        return make_response(jsonify({'Berhasil': 'Sudah terdaftar','status_code':200}),200)
    if rfid != record[1] :
        return make_response(jsonify({'error': 'Belum terdaftar','status_code':403}), 403)
    return redirect(url_for('.dashboard_view'))
@komplek.route('/visitor_in_button', methods=['POST'])
def visitor_in_button():
    now = datetime.now()
    msg = ''
    rfid = 0
    if request.method == 'POST' :
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM tb_record WHERE rfid = %s', (rfid))
        nama = 'visitor'
        rfid = 000
        alamat = 'visitor' 
        tanggal =  now.strftime("%d/%m/%Y")
        jam = now.strftime("%H:%M:%S")
        status = 'masuk'
        mycursor = mydb.cursor()
        mycursor.execute('INSERT INTO tb_visitor(nama, rfid, alamat,tanggal,jam,status) VALUES (%s, %s, %s,%s,%s,%s)', (nama, rfid, alamat,tanggal,jam,status))
        mydb.commit()
        return redirect(url_for('komplek.dashboard_view'))
    return redirect(url_for('komplek.dashboard_view'))
@komplek.route('/visitor_out/<rfid>',methods=['GET','POST'])
def visitor_out(rfid):
    now = datetime.now()
    msg = ''
    rfid = request.form['rfid']
    photo = request.form['photo']
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM tb_record WHERE rfid = %s', (rfid))
    #query = "SELECT * FROM tb_visitor"
    if request.method == 'POST' and 'rfid' and 'photo' in request.form:
        #rfid = request.form['rfid']
        data = mycursor.fetchall() 
        record = data[0]
        nama = record[0]
        alamat = record[2]
        tanggal =  now.strftime("%d/%m/%Y")
        jam = now.strftime("%H:%M:%S")
        status = 'keluar'
        photo = request.form['photo']
        mycursor.execute('INSERT INTO tb_visitor(nama, rfid, alamat,tanggal,jam,status,photo) VALUES (%s, %s, %s,%s,%s,%s,%s)', (nama, rfid, alamat,tanggal,jam,status,photo))
        mydb.commit()
        return make_response(jsonify({'Berhasil': 'Sudah terdaftar','status_code':200}),200)
    if rfid != record[1] :
            return make_response(jsonify({'error': 'Belum terdaftar','status_code':403}), 403)
    return redirect(url_for('komplek.dashboard_view'))
@komplek.route('/visitor_out_button', methods=['POST'])
def visitor_out_button():
    now = datetime.now()
    msg = ''
    rfid = 0
    if request.method == 'POST' :
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM tb_record WHERE rfid = %s', (rfid))
        nama = 'visitor'
        rfid = 000
        alamat = 'visitor' 
        tanggal =  now.strftime("%d/%m/%Y")
        jam = now.strftime("%H:%M:%S")
        status = 'keluar'
        mycursor = mydb.cursor()
        mycursor.execute('INSERT INTO tb_visitor(nama, rfid, alamat,tanggal,jam,status) VALUES (%s, %s, %s,%s,%s,%s)', (nama, rfid, alamat,tanggal,jam,status))
        mydb.commit()
        return redirect(url_for('komplek.dashboard_view'))
    return redirect(url_for('komplek.dashboard_view'))
   
########################### Delete Data Fitur #######################################################
@komplek.route('/delete_data_record/<rfid>', methods = ['POST','GET'])
def delete_data_record(rfid):
    mycursor = mydb.cursor()
  
    mycursor.execute('DELETE FROM tb_record WHERE rfid = %s',(rfid))
    mydb.commit()
    #flash('Employee Removed Successfully')
    return redirect(url_for('.get_data'))

########################### Visitor Menu #######################################################

@komplek.route('/visitor_in_buttonn', methods=['GET','POST'])
def visitor_in_buttonn():
    now = datetime.now()
    # cek dulu apakah field data yang kita kirim ada di dalam request atau tidak
    if request.method == 'POST' and 'rfid' in request.form and 'nama' in request.form:
        #ambil jika memang ada datanya didalam agar menghindari valuenya kosong
        rfid = "-"
        nama = request.form['nama']
        alamat = request.form['rfid']
        tanggal =  now.strftime("%d/%m/%Y")
        jam = now.strftime("%H:%M:%S")
        status = 'masuk'
        photo = '-'
        mycursor = mydb.cursor()
        mycursor.execute('INSERT INTO tb_visitor(nama, rfid, alamat,tanggal,jam,status,photo) VALUES (%s, %s, %s,%s,%s,%s,%s)', (nama, rfid, alamat,tanggal,jam,status,photo))
        mydb.commit()
    return redirect(url_for('komplek.dashboard_view'))


@komplek.route('/visitor_out_buttonn', methods=['POST'])
def visitor_out_buttonn():
    now = datetime.now()
    # cek dulu apakah field data yang kita kirim ada di dalam request atau tidak
    if request.method == 'POST' and 'rfid' in request.form and 'nama' in request.form:
        # ambil jika memang ada datanya didalam agar menghindari valuenya kosong
        rfid = "-"
        nama = request.form['nama']
        alamat = request.form['rfid']
        tanggal =  now.strftime("%d/%m/%Y")
        jam = now.strftime("%H:%M:%S")
        status = 'keluar'
        photo = '-'
        mycursor = mydb.cursor()
        mycursor.execute('INSERT INTO tb_visitor(nama, rfid, alamat,tanggal,jam,status,photo) VALUES (%s, %s, %s,%s,%s,%s,%s)', (nama, rfid, alamat,tanggal,jam,status,photo))
        mydb.commit()
    return redirect(url_for('komplek.dashboard_view'))
########################### Fitur Photo #######################################################
@komplek.route("/photo_data_visitor/<id>",methods=['GET'])
def photo_data(id):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT photo FROM tb_visitor WHERE id = %s', (id))
    data = mycursor.fetchone()
    print(data[0])
    mycursor.close()
    return render_template('komplek/photo.html', visitor_photo=data[0])
