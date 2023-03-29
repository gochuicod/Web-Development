from flask import Flask, render_template, redirect, url_for, request, session
import mysql.connector, bcrypt

pythondb = mysql.connector.connect(
    host="localhost",
    user="gochuicod",
    password="20259388",
    database="pythondb"
)
cursor = pythondb.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oS1BCq0wk@QQFOi7pp0ykCk5R@1nX4^MDPFThthI4Hlo8Ki8Ds'

# These are for template routing
@app.route('/')
def index(): return render_template('index.html')

@app.route('/home')
def home(): return render_template('home.html', student_data=session.get('student_data'), user_data=session.get('user_data'))

# These are for system functions
@app.route('/user_auth',methods=['POST'])
def userAuthentication():
    username = request.form['username']
    password = request.form['password']

    cursor.execute(f"select * from users")
    users = cursor.fetchall()

    for user in users:
        if username == user[1] and bcrypt.checkpw(password.encode("utf-8"),user[2].encode("utf-8")):
            session['username'] = username
            session['student_data'] = list(getStudents())
            session['user_data'] = list(getUsers())
            return redirect(url_for('home'))
    return redirect(url_for("index"))

@app.route('/home/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

# These comprise the CRUD functionality of this system
@app.route('/home/student/add',methods=['POST'])
def addStudent()->None:
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    course = request.form['course']
    level = request.form['level']
    cursor.execute(
        "insert into students (firstname,lastname,course,level) values(%s,%s,%s,%s)",
        [firstname.title(),lastname.title(),course.upper(),level]
    )
    try:
        pythondb.commit()
        session['student_data'] = list(getStudents())
        return redirect(url_for("home"))
    except: return redirect(url_for("home"))

@app.route('/home/students/get')
def getStudents()->tuple:
    cursor.execute("select * from students")
    return cursor.fetchall()

@app.route('/home/users/get')
def getUsers()->tuple:
    cursor.execute("select * from users")
    return cursor.fetchall()

@app.route('/home/student/update',methods=['POST'])
def updateStudent():
    id = request.form['id']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    course = request.form['course']
    level = request.form['level']

    cursor.execute(f"update students set firstname='{firstname.title()}', lastname='{lastname.title()}', course='{course.upper()}', level='{level}' where id={id}")
    pythondb.commit()
    session['student_data'] = list(getStudents())
    
    return redirect(url_for('home'))

@app.route('/home/student/find',methods=['POST'])
def findStudent():
    search_box_data = request.form['search']
    if(search_box_data == "all"): session['student_data'] = list(getStudents())
    else:
        cursor.execute(f"select * from students where firstname='{search_box_data.title()}' or lastname='{search_box_data.title()}'")
        session['student_data'] = list(cursor.fetchall())
    return redirect(url_for('home'))

@app.route('/home/student/delete',methods=['POST'])
def deleteStudent()->None:
    id = request.form['id']
    cursor.execute(f"delete from students where id={id}")
    try:
        pythondb.commit()
        session['student_data'] = list(getStudents())
        return redirect(url_for("home"))
    except: return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)