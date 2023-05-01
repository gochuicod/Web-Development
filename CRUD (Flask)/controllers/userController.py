#--------------------------------------------------------------------------------
# 2023 IT-ELPYTH Python Programming
#--------------------------------------------------------------------------------
#
#  File Name: app.py
#  Author: Darelle Gochuico
#
#  Methods:
#      +authenticate                    - Generate a new student via formdata.
#      +getAllUsers                     - Update a student via formdata.
#      +setUser                         - Get a student via formdata.

import mysql.connector, bcrypt
from controllers.studentController import getAll, get
from controllers.fileController import getUserFiles

pythondb = mysql.connector.connect(
    host="localhost",
    user="gochuicod",
    password="20259388",
    database="pythondb"
)
cursor = pythondb.cursor()

#--------------------------------------------------------------------------------
# Method Name: authenticate
# Description: authenticates the presumed user.
# Arguments  : username
#              password
# Return     : boolean/array
#--------------------------------------------------------------------------------
def authenticate(username,password):
    users = getAllUsers()

    for user in users:
        if username == user[1] and bcrypt.checkpw(password.encode("utf-8"),user[2].encode("utf-8")):
            if user[1] == "admin": return [getAll(), users]
            else: return [get(user[3]), getUserFiles(user[3])]
    return False

#--------------------------------------------------------------------------------
# Method Name: getAllUsers
# Description: retrieves all the users
# Arguments  : none
# Return     : tuple
#--------------------------------------------------------------------------------
def getAllUsers():
    cursor.execute(f"select * from users")
    return cursor.fetchall()

#--------------------------------------------------------------------------------
# Method Name: setUser
# Description: creates a new user
# Arguments  : username
#              password
#              student_id
# Return     : none
#--------------------------------------------------------------------------------
def setUser(username,password,student_id):
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt(14))

    cursor.execute(
        "insert into users (username,password,student_id) values(%s,%s,%s)",
        [username,hashedPassword.decode('utf-8'),student_id]
    )
    pythondb.commit()