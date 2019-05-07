from MySQLdb.compat import unicode
from flask import Flask, session, render_template, request, jsonify, redirect, url_for
import main

#importing package to connect flask to mysql database
from flaskext.mysql import MySQL

#flask app
nlpsql = Flask(__name__)
nlpsql.secret_key = 'nlpsql key'

mysql = MySQL(nlpsql)

#database Configuration
nlpsql.config['MYSQL_DATABASE_USER'] = 'root'
nlpsql.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
nlpsql.config['MYSQL_DATABASE_DB'] = 'nlpproj'
nlpsql.config['MYSQL_DATABASE_HOST'] = 'localhost'

#start flask app
mysql.init_app(nlpsql)


#route for home, entry point is defined here
@nlpsql.route('/')
def home():
	if 'error' in session:	
		error = session['error']
		session.pop('error', None)
	else:	
		error = ''
	#return render_template('index.html', error=error)
	return redirect('/index')


#route for getting example pdf	
@nlpsql.route('/results')
def returnResultsPDF():
	file_name = 'results.pdf'
	return redirect(url_for('static', filename='/'.join(['doc', file_name])), code=301)


@nlpsql.route('/logout')
def logout():
	session.pop('error', None)
	session.pop('access', None)
	return redirect('/')


@nlpsql.route('/submitLogin', methods=['POST', 'GET'])
def processLogin():
	username = request.form['username']
	password = request.form['password']
	query = "select access, password from users where userid='"+username+"' ;"
	cursor = mysql.connect().cursor()
	cursor.execute(query)
	data = cursor.fetchall()
	print(data)
	if len(data) > 0:
		access = data[0][0]
		session['access'] = access
		if data[0][1] == password:
			return redirect('/index')
		else:
			session['error'] = 'Invalid Username or password'
			return redirect('/')
	else:		
		session['error'] = 'Invalid Username or password'
		return redirect('/')


@nlpsql.route('/changeAccess', methods=['POST'])
def changeAccess():
	userId = request.form['changeAccess']
	access = request.form['accessMode']
	conn=mysql.connect()
	cursor = conn.cursor()
	cursor.execute('''UPDATE users SET access=%s WHERE userid = %s;''', (access, userId))
	conn.commit()
	return redirect('/admin')


@nlpsql.route('/signup')
def getSignup():
	return render_template('signup.html')


@nlpsql.route('/requestAuthentication', methods=['POST', 'GET'])
def getDetails():
	access = request.form['desig']
	access = '2'
	department = request.form['department']
	password = request.form['password']
	userId = request.form['userId']
	name = request.form['name']
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute('''INSERT INTO users(userid,password,access,name) 
					VALUES (%s,%s,%s,%s);''', (userId, password, access, name))
	conn.commit()
	query = "select * from users"
	cursor.execute(query)
	data = cursor.fetchall()
	print(data)
	return redirect('/index')


@nlpsql.route('/index')
def getConsole():
	if 'access' in session:
		access = session['access']
		session.pop('access', None)
	else:
		access = 1
	return render_template('index.html', access=access)


@nlpsql.route('/admin')
def adminPanel():
	query = 'SELECT * FROM users'
	cursor = mysql.connect().cursor()
	cursor.execute(query)
	data = cursor.fetchall()
	encodedData = []
	for row in data:
		encodedrow = []
		for item in row:
			if isinstance(item, unicode):
				#encodedrow.append(item.encode("utf-8"))
				encodedrow.append(item)
			else:
				encodedrow.append(item)
		encodedData.append(encodedrow)
	return render_template('admin.html', data=encodedData)


#getting mysql result for the input query 
@nlpsql.route('/submitQuery', methods=['POST'])
def getQuery():
	query = request.form['query']
	print(query)
	#processQuery converts the input query to mysql query
	#todo: return column names to show in result table
	query = main.processQuery(query)

	#execute mysql query
	cursor = mysql.connect().cursor()
	cursor.execute(query)
	data = cursor.fetchall()
	
	#converting from unicode to UTF-8
	encodedData = []
	for row in data:
		encodedRow = []
		for item in row:
			if isinstance(item, unicode):
				#encodedRow.append(item.encode("utf-8"))
				encodedRow.append(item)
			else:
				encodedRow.append(item)
		encodedData.append(encodedRow)

	#creating html table for  Query result
	htmlResult = "<span>Query: </span>" \
		"<code class='query'>"+query+"</code><div><img class='tree-image' src='http://www.freeiconspng.com/uploads/computer-desktop-display-monitor-screen-system-wallpaper-icon--13.png'/>" \
		"<table class='table'>"
	#todo: add table head here with column names
	htmlResult = htmlResult+"<thead><tr><th scope=\"col\">column1</th>" \
		"<th scope=\"col\">column2</th>" \
		"<th scope=\"col\">column3</th>" \
		"</tr></thead>"
	for tableRow in encodedData:
		htmlResult = htmlResult+"<tr>"
		for tableCell in tableRow:
			htmlResult = htmlResult+"<td>"+str(tableCell)+"</td>"
		htmlResult = htmlResult+"</tr>"
	htmlResult = htmlResult+"</table>"
	
	#converts html to jason format
	return jsonify(htmlResult)


#to get Student database similar to getQuery
@nlpsql.route('/showStudentDetails', methods=['POST'])
def showStudentDetails():
	query = "select * from student"
	query = main.processQuery(query)
	cursor = mysql.connect().cursor()
	cursor.execute(query)
	data = cursor.fetchall()
	encodedData = []
	for row in data:
		encodedRow = []
		for item in row:
			if isinstance(item, unicode):
				#encodedRow.append(item.encode("utf-8"))
				encodedRow.append(item)
			else:
				encodedRow.append(item)
		encodedData.append(encodedRow)
				
	studentTable = ""
	for row in encodedData:
		studentTable = studentTable+"<tr>"
		for cell in row:
			studentTable = studentTable+"<td>"+str(cell)+"</td>"
		studentTable = studentTable+"</tr>"

	studentTable = studentTable+""

	print(studentTable)
	return jsonify(studentTable)


#to get department database similar to getQuery
@nlpsql.route('/showDepartmentDetails', methods=['POST'])
def showDepartmentDetails():
	query = "select * from department"
	query = main.processQuery(query)
	cursor = mysql.connect().cursor()
	cursor.execute(query)
	data = cursor.fetchall()
	encodedData = []
	for row in data:
		encodedRow = []
		for item in row:
			if isinstance(item, unicode):
				#encodedRow.append(item.encode("utf-8"))
				encodedRow.append(item)
			else:
				encodedRow.append(item)
		encodedData.append(encodedRow)
				
	departmentTable = ""
	for row in encodedData:
		departmentTable = departmentTable+"<tr>"
		for cell in row:
			departmentTable = departmentTable+"<td>"+str(cell)+"</td>"
		departmentTable = departmentTable+"</tr>"

	print(departmentTable)
	return jsonify(departmentTable)


#main function which runs the flask app
if __name__ == '__main__':
	nlpsql.run()
