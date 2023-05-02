#--------------------------------------------------------------------------------
# 2023 IT-ELPYTH Python Programming
#--------------------------------------------------------------------------------
#
#  File Name: app.py
#  Author: Darelle Gochuico
#
#  Methods:
#      +addStudent                      - Generate a new student via formdata.
#      +updateStudent                   - Update a student via formdata.
#      +findStudent                     - Get a student via formdata.
#      +deleteStudent                   - Remove a student via formdata.
#      +userAuthentication              - Authenticates a user.
#      +userRegistration                - Registers a new user.
#      +uploadImage                     - Lets the user upload an image.
#      +logout                          - Logs the user out of the session.
#  Utility:
#      -refresh                         - Refreshes student data after a query.
#  Attributes:
#      -app                             - Initializes the Flask framework.
#      -SECRET_KEY                      - The app's secret key.
#  Routes:
#      -index                           - Route for the login page.
#      -home                            - Route for the main page.
#      -register                        - Route for the registration page.

from flask import Flask, render_template, redirect, url_for, request, session
from controllers.userController import authenticate, getAllUsers, setUser
from controllers.studentController import add, getAll, delete, find, update, get
from controllers.fileController import getUserFiles, addNewFile, addWebcamImage

#--------------------------------------------------------------------------------
# INITIALIZATIONS
#--------------------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'oS1BCq0wk@QQFOi7pp0ykCk5R@1nX4^MDPFThthI4Hlo8Ki8Ds'

#--------------------------------------------------------------------------------
# CORE FUNCTIONS
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method Name: addStudent
# Description: creates a new student
# Arguments  : none
# Return     : none
#--------------------------------------------------------------------------------
@app.route('/home/student/add',methods=['POST'])
def addStudent():
    add(
        request.form['student_id'],
        request.form['firstname'],
        request.form['lastname'],
        request.form['course'],
        request.form['level']
    ) ; refresh()

    return redirect(url_for('home'))

#--------------------------------------------------------------------------------
# Method Name: updateStudent
# Description: updates a student's data
# Arguments  : none
# Return     : none
#--------------------------------------------------------------------------------
@app.route('/home/student/update',methods=['POST'])
def updateStudent():
    update(
        request.form['id'],
        request.form['firstname'],
        request.form['lastname'],
        request.form['course'],
        request.form['level']
    ) ; refresh()
    
    return redirect(url_for('home'))

#--------------------------------------------------------------------------------
# Method Name: findStudent
# Description: finds a student
# Arguments  : none
# Return     : none
#--------------------------------------------------------------------------------
@app.route('/home/student/find',methods=['POST'])
def findStudent():
    search_box_data = request.form['search']

    if search_box_data == "": session['student_data'] = [getAll(), getAllUsers()]
    else: session['student_data'] = [find(search_box_data), getAllUsers()]

    return redirect(url_for('home'))

#--------------------------------------------------------------------------------
# Method Name: deleteStudent
# Description: deletes a student
# Arguments  : none
# Return     : redirect
#--------------------------------------------------------------------------------
@app.route('/home/student/delete',methods=['POST'])
def deleteStudent()->None:
    id = request.form['id']

    delete(id); refresh()

    return redirect(url_for("home"))

#--------------------------------------------------------------------------------
# Method Name: userAuthentication
# Description: authenticates a user from input
# Arguments  : none
# Return     : redirect
#--------------------------------------------------------------------------------
@app.route('/user_auth',methods=['POST'])
def userAuthentication():
    username = request.form['username']
    password = request.form['password']

    session['student_data'] = authenticate(username,password)
    if session.get('student_data') != False:
        session['images'] = session.get('student_data')[1]
        session['username'] = username
        session['user_id'] = session.get('student_data')[0][0][0]
        return redirect(url_for('home'))
    
    return redirect(url_for('index'))

#--------------------------------------------------------------------------------
# Method Name: userRegistration
# Description: registers a user
# Arguments  : none
# Return     : redirect
#--------------------------------------------------------------------------------
@app.route('/user_register',methods=['POST'])
def userRegistration():
    setUser(
        request.form['username'],
        request.form['password'],
        request.form['student_id']
    )
    add(
        request.form['student_id'],
        request.form['firstname'],
        request.form['lastname'],
        "",""
    )

    return redirect(url_for('register'))

#--------------------------------------------------------------------------------
# Method Name: uploadImage
# Description: uploads an Image
# Arguments  : none
# Return     : redirect
#--------------------------------------------------------------------------------
@app.route('/home/upload',methods=['POST'])
def uploadImage():
    file = request.files['image_file']
    student_id = request.form['id']

    addNewFile(file,student_id)

    session['images'] = list(getUserFiles(session.get('user_id')))

    return redirect(url_for("home"))

#--------------------------------------------------------------------------------
# Method Name: uploadWebcamImage
# Description: uploads a webcam image
# Arguments  : none
# Return     : redirect
#--------------------------------------------------------------------------------
@app.route('/home/webcam/upload',methods=['POST'])
def uploadWebcamImage():
    image_data = request.form['image_data']
    filename = request.form['filename']
    student_id = session.get('user_id')

    addWebcamImage(image_data,filename,student_id)

    session['images'] = list(getUserFiles(session.get('user_id')))

    return redirect(url_for("home"))

#--------------------------------------------------------------------------------
# Method Name: logout
# Description: logs the user out of the session
# Arguments  : none
# Return     : redirect
#--------------------------------------------------------------------------------
@app.route('/home/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#--------------------------------------------------------------------------------
# TEMPLATE ROUTES
#--------------------------------------------------------------------------------
@app.route('/')
def index(): return render_template('index.html')

@app.route('/home')
def home(): return render_template('home.html')

@app.route('/registration')
def register(): return render_template('registration.html')

#--------------------------------------------------------------------------------
# UTILITY FUNCTIONS
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method Name: refresh
# Description: refreshes the data after a query
# Arguments  : none
# Return     : none
#--------------------------------------------------------------------------------
def refresh():
    if session.get('username') == "admin":
        session['student_data'] = [getAll(), getAllUsers()]
    else: session['student_data'] = [get(session.get('user_id')), getUserFiles(session.get('user_id'))]

if __name__ == '__main__': app.run(debug=True)