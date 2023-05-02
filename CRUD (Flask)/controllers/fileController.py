#--------------------------------------------------------------------------------
# 2023 IT-ELPYTH Python Programming
#--------------------------------------------------------------------------------
#
#  File Name: app.py
#  Author: Darelle Gochuico
#
#  Methods:
#      +getUserFiles                    - Retrieve all the user's files.
#      +addNewFile                      - Adds a new file for the user.
#      +addWebcamImage                  - Adds a webcam image from the user.
#  Utility:
#      +allowed_file                    - Determines the allowed file types.

import mysql.connector, os, time, base64
from werkzeug.utils import secure_filename

pythondb = mysql.connector.connect(
    host="localhost",
    user="gochuicod",
    password="20259388",
    database="pythondb"
)
cursor = pythondb.cursor()

#--------------------------------------------------------------------------------
# Method Name: getUserFiles
# Description: Retrieves all user files
# Arguments  : id
# Return     : none
#--------------------------------------------------------------------------------
def getUserFiles(id):
    cursor.execute(f"select * from filepaths where student_id={id}")
    return cursor.fetchall()

#--------------------------------------------------------------------------------
# Method Name: addNewFile
# Description: adds a new file for a user
# Arguments  : file
#              student_id
# Return     : none
#--------------------------------------------------------------------------------
def addNewFile(file,student_id):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.',1)[1]
        new_filename = f"{int(time.time())}_{student_id}.{file_ext}"
        file.save(os.path.join('static/images',new_filename))
        cursor.execute(f"insert into filepaths (filepath,student_id) values('{new_filename}','{student_id}')")
        pythondb.commit()

#--------------------------------------------------------------------------------
# Method Name: addWebcamImage
# Description: stores a webcam image to the database
# Arguments  : image_data
#              filename
#              student_id
# Return     : none
#--------------------------------------------------------------------------------
def addWebcamImage(image_data,filename,student_id):
    if image_data and allowed_file(filename):
        image_data = image_data.rsplit(',')[1]
        filename = secure_filename(filename)
        file_ext = filename.rsplit('.',1)[1]
        new_filename = f"{int(time.time())}_{student_id}.{file_ext}"

        with open(os.path.join('static/images',new_filename), 'wb') as fh:
            fh.write(base64.b64decode(image_data))

        cursor.execute(f"insert into filepaths (filepath,student_id) values('{new_filename}','{student_id}')")
        pythondb.commit()

#--------------------------------------------------------------------------------
# UTILITY FUNCTIONS
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Method Name: allowed_file
# Description: defines the allowed files
# Arguments  : filename
# Return     : String
#--------------------------------------------------------------------------------
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'jpg','jpeg','png'}