#--------------------------------------------------------------------------------
# 2023 IT-ELPYTH Python Programming
#--------------------------------------------------------------------------------
#
#  File Name: app.py
#  Author: Darelle Gochuico
#
#  Methods:
#      +add                             - Generate a new student from parameters.
#      +getAll                          - Retrieves all students.
#      +get                             - Retrieves a specific student.
#      +update                          - Updates a student's data.
#      +find                            - Finds a student with multiple parameters.
#      +delete                          - Deletes a student.

import mysql.connector

pythondb = mysql.connector.connect(
    host="localhost",
    user="gochuicod",
    password="20259388",
    database="pythondb"
)
cursor = pythondb.cursor()

#--------------------------------------------------------------------------------
# Method Name: add
# Description: adds a student to the database
# Arguments  : student_id
#              firstname
#              lastname
#              course
#              level
# Return     : none
#--------------------------------------------------------------------------------
def add(student_id,firstname,lastname,course,level):
    cursor.execute(
        "insert into students (student_id,firstname,lastname,course,level) values(%s,%s,%s,%s,%s)",
        [student_id,firstname.title(),lastname.title(),course.upper(),level]
    )
    pythondb.commit()

#--------------------------------------------------------------------------------
# Method Name: getAll
# Description: retrieves all students
# Arguments  : none
# Return     : tuple
#--------------------------------------------------------------------------------
def getAll():
    cursor.execute("select * from students")
    return cursor.fetchall()

#--------------------------------------------------------------------------------
# Method Name: get
# Description: retrieves a specific student
# Arguments  : id
# Return     : tuple
#--------------------------------------------------------------------------------
def get(id):
    cursor.execute(f"select * from students where student_id={id}")
    return cursor.fetchall()

#--------------------------------------------------------------------------------
# Method Name: update
# Description: replaces existing student data with a new one
# Arguments  : id
#              firstname
#              lastname
#              course
#              level
# Return     : none
#--------------------------------------------------------------------------------
def update(id,firstname,lastname,course,level):
    cursor.execute(f"update students set firstname='{firstname.title()}', lastname='{lastname.title()}', course='{course.upper()}', level='{level}' where student_id={id}")
    pythondb.commit()

#--------------------------------------------------------------------------------
# Method Name: find
# Description: retrieves a specific student with multiple params
# Arguments  : search_box_data
# Return     : none
#--------------------------------------------------------------------------------
def find(search_box_data):
    cursor.execute(f"select * from students where firstname='{search_box_data.title()}' or lastname='{search_box_data.title()}' or student_id='{search_box_data}'")
    return cursor.fetchall()

#--------------------------------------------------------------------------------
# Method Name: delete
# Description: deletes student data
# Arguments  : id
# Return     : none
#--------------------------------------------------------------------------------
def delete(id):
    cursor.execute(f"delete from students where student_id={id}")
    pythondb.commit()