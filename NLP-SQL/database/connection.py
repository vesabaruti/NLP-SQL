import mysql.connector

config = {
  'user': 'root',
  'password': 'admin',
  'host': '127.0.0.1',
  'database': 'nlpproj',
  'raise_on_warnings': True,
  'charset': 'utf8'
}

cnx = mysql.connector.connect(**config)
#print('Successful connection')
cursor = cnx.cursor()

# Add department details
add_department = "INSERT INTO department (dId,name,buildingCode) VALUES (%s,%s,%s)"
data_department = [(23, 'Civil', 101),
                   (29, 'Chemical', 203),
                   (31, 'CS', 104),
                   (37, 'IT', 302),
                   (41, 'Mining', 101),
                   (43, 'Mechanical', 102)]
for i in range(6):
    cursor.execute(add_department, data_department[i])

#Add student details
add_student = "INSERT INTO student (sId,name,sex,address,phone,cgpa,dId) VALUES (%s,%s,%s,%s,%s,%s,%s)"
data_student = [(1, 'Dwayne', 'M', 'Los Angeles', '9562033255', 7, 23),
                (2, 'Harvey', 'M', 'California', '8109502625', 10, 37),
                (3, 'Rachel', 'F', 'Los Angeles', '9845913946', 9, 23),
                (4, 'Mike', 'M', 'Los Angeles', '9962234444', 10, 41),
                (5, 'Jessica', 'F', 'Texas', '9463688542', 8, 37), (6, 'Louis', 'M', 'New Jersey', '8558098383', 7, 41),
                (7, 'Donna', 'F', 'California', '9501188856', 8, 29), (8, 'Trevor', 'F', 'Hawaii', '9717366117', 4, 23),
                (9, 'Daniel', 'M', 'Georgia', '9223237016', 6, 37),
                (10, 'Dwayne', 'M', 'New York', '7219560267', 9, 41)]
for i in range(10):
    cursor.execute(add_student, data_student[i])

#Add users tables
add_user = "INSERT INTO users (userid, password, access, name) VALUES (%s,%s,%s,%s)"
data_user = [('admin', 'admin', 1, 'Admin'),
             ('user', 'user', 2, 'User')]
for i in range(2):
    cursor.execute(add_user, data_user[i])

cnx.commit()
cursor.close()
cnx.close()
