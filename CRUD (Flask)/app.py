from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.utils import secure_filename
import mysql.connector, bcrypt, os

pythondb = mysql.connector.connect(
    host="localhost",
    user="gochuicod",
    password="20259388",
    database="pythondb"
)
cursor = pythondb.cursor()

app = Flask(__name__)
app.config['IMAGES_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'jpg','jpeg','png'}
app.config['SECRET_KEY'] = 'oS1BCq0wk@QQFOi7pp0ykCk5R@1nX4^MDPFThthI4Hlo8Ki8Ds'

# These are for template routing
@app.route('/')
def index(): return render_template('index.html')

@app.route('/home')
def home(): return render_template('home.html')

# These are for system functions
@app.route('/user_auth',methods=['POST'])
def userAuthentication():
    username = request.form['username']
    password = request.form['password']

    cursor.execute(f"select * from users")
    users = cursor.fetchall()

    for user in users:
        if username == user[1] and bcrypt.checkpw(password.encode("utf-8"),user[2].encode("utf-8")):
            if user[1] == "admin":
                session['student_data'] = list(get("select * from students"))
                session['user_data'] = list(get("select * from users"))
            else:
                session['student_data']:list = list(get(f"select * from students where student_id={user[3]}"))
                session['images']:list = list(get(f"select * from filepaths where student_id={user[3]}"))
            session['username'] = username
            session['user_id'] = user[3]
            return redirect(url_for('home'))
    return redirect(url_for("index"))

@app.route('/home/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route('/home/upload',methods=['POST'])
def uploadImage():
    file = request.files['image_file']
    student_id = request.form['id']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['IMAGES_FOLDER'],filename))
        image_path = os.path.join(app.config['IMAGES_FOLDER'],filename)
        cursor.execute(f"insert into filepaths (filepath,student_id) values('{filename}','{student_id}')")
        pythondb.commit()
        session['images']:list = list(get(f"select * from filepaths where student_id={session.get('user_id')}"))
    return redirect(url_for("home"))

# These are utility modules
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
        session['student_data'] = list(get("select * from students"))
        return redirect(url_for("home"))
    except: return redirect(url_for("home"))

@app.route('/home/get')
def get(query:str)->tuple:
    cursor.execute(query)
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
    session['student_data'] = list(get("select * from students"))
    
    return redirect(url_for('home'))

@app.route('/home/student/find',methods=['POST'])
def findStudent():
    search_box_data = request.form['search']
    if(search_box_data == "all"): session['student_data'] = list(get("select * from students"))
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
        session['student_data'] = list(get("select * from students"))
        return redirect(url_for("home"))
    except: return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)