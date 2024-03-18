from flask import Flask,render_template,request,url_for,redirect,jsonify,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import cvzone
from preprocessimages import *
from datetime import datetime
import os
import cv2
import cv2
from werkzeug.routing import BaseConverter
import urllib.parse




app=Flask(__name__,static_folder='static')


class DateConverter(BaseConverter):
    def to_python(self, value):
        # The value is already a string, so no need for conversion
        return value
                                                                              
    def to_url(self, value):
        return value


app.url_map.converters['date'] = DateConverter
#This allows Flask to recognize and use the DateConverter for any URL route that specifies a variable of type 'date'. For example, if a
# route is defined as @app.route('/date/<date:date>'), 
# the DateConverter will be used to handle the conversion of the <date> variable in the URL.






app.app_context().push()
app.secret_key='Jadissa123!@$' #securely sign cookies and other session-related data
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'                #configuration values for connecting to a MySQL database
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='university'




mysql=MySQL(app)
cursor,conn=makeconnectiontodtabase(mysql,MySQLdb.cursors.DictCursor)
encodings=getallimagesfromdb(cursor)
ids=getallidfromdb(cursor)
encodelistwithid=[encodings,ids]
known_face_encodings,professorid=encodelistwithid

def checkname(name,major,img): 
      now=datetime.now()
      d1=now.strftime("%Y/%m/%d")
      if(not exist_name(cursor,name,d1)):
            dfstring=now.strftime("%Y/%m/%d %H:%M:%S")
            insertintodb(cursor,name,major,img,dfstring)
            cursor.execute(f"update professors set lastattendance='{dfstring}' where name='{name}'")
            cursor.execute(f"update professors set totalattendance=totalattendance+1 where name='{name}'")
            conn.commit()
def gennn(): 
     camera = cv2.VideoCapture(0)
     face_locations = []
     face_encodings = []
     face_names=[]
     majors=[]
    #  ages=[]
     idmatches=[]
     images=[]
     while True:
             success, frame = camera.read()  # read the camera frame
              # Resize frame of video to 1/4 size for faster face recognition processing
             small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
             rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
             rgb_small_frame = small_frame[:, :, ::-1] #same(rgb)
             face_locations = face_recognition.face_locations(rgb_small_frame)
             face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
             face_names=[]
             majors=[]
            #  ages=[]
             idmatches=[]
             images=[]
             # Set the confidence threshold for face recognition predictions
             confidence_threshold = 0.5
             for face_encoding,faceloc in zip(face_encodings,face_locations):
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.6)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]and face_distances[best_match_index] <= confidence_threshold:
                    id=professorid[best_match_index]
                    idmatches.append(id)    
                    name,major,img=getinformationprofessor(cursor,id)
                    
                    face_names.append(name)
                    majors.append(major)
                    # ages.append(age) 
                    images.append(img)
                    y1,x2,y2,x1 = faceloc # in the other code we risize the face
                    y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                    # bbox=1+y1,1+y1,y1-x1,y2-y1
                    bbox=1+x1,1+y1,x2-x1,y2-y1
                    cvzone.cornerRect(frame,bbox,rt=0)
                    cv2.putText(frame,str(name),(300,400),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)                    
                    checkname(name,major,img)
                elif not matches[best_match_index] :
                      cv2.putText(frame,"unknown",(300,400),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
              

             cv2.imshow("webcam",frame)
             key = cv2.waitKey(1)
             if key == 27:
                 break
#      mylist=[idmatches,face_names,majors,ages,images]        
#      return mylist



@app.route('/')
def index():
        # gennn()
        # lista=gennn()
        # profinfo=list(zip(*lista))
        # date=request.form.get('date')
        
        return render_template('index.html')

@app.route('/process_form', methods=['GET', 'POST'])
def process_form():
    if request.method == 'POST':
        date_inputstr = request.form.get('date_input')
        # dt=type(date_input)
        date_input=datetime.strptime(date_inputstr, "%Y-%m-%d")
        mylist=getallattendaceatdt(cursor,date_input)
        profinfo=list(zip(*mylist))
        return render_template('result.html',date_input=date_inputstr,profinfo=profinfo)
    else:
        return 'Invalid request method'
    

@app.route('/mywebcam')  
def webcam():
     gennn()          
     return render_template('index.html')

@app.route("/addemployee",methods=["GET", "POST"])
def addemployee():
     msg=""
     alert_type=""
     if request.method =="POST": 
          
          name=request.form.get("name")
        #   age=request.form.get("age")
          major=request.form.get("major")
          year=request.form.get("year")
          image=request.files["image"]
          image_data = image.read()
          imagefilename=image.filename
          id= os.path.splitext(imagefilename)[0]
        #   insert_professor(cursor,id,name,age,major,year,image_data)
          
          if insert_professor(cursor,id,name,major,year,image_data):
                 msg="New Employee Added successfully"
                 alert_type = "success" 
          else:
                 msg="Employee already exists"
                 alert_type = "danger"
          conn.commit()    
                 
                 

     return render_template('employee.html',msg=msg,alert_type=alert_type)


      

@app.route('/missing/<date:date_value>')
def missing(date_value):
    # Pass the date_value directly to the template
    mylist=getallmissingprofessorsatdt(cursor,date_value)
    profinfo=list(zip(*mylist))  
    session['date_value'] = date_value
    msg = session.pop('msg', None)
    alert_type = session.pop('alert_type', None) 
    return render_template('missing.html', date_value=date_value,profinfo=profinfo,msg=msg,alert_type=alert_type)


@app.route('/repport/<date:date_value>')
def repport(date_value):
    #  date=session.pop('date_value', None)
     lista=selectallrepportatdt(cursor,date_value)
     profinfo=list(zip(*lista))
     return render_template('repport.html',date_value=date_value,profinfo=profinfo)


@app.route('/saved', methods=['POST'])
def update_names():
    if request.method == 'POST':
        # Retrieve the updated names from the request
        updated_names = request.form.getlist('updated_names')
     
       
        date_value = session.get('date_value')
        
        if select_insert_repport(cursor, date_value, updated_names):   
             msg="Report Done Successfully"
             alert_type = "success" 
        else:
                 msg="Report already exists"
                 alert_type = "danger"
        conn.commit() 
               
        session['msg'] = msg
        session['alert_type'] = alert_type 
        # Add the message as a query parameter in the redirect URL
        redirect_url = url_for('missing', date_value=date_value)
        # # Redirect to the other route
        return redirect(redirect_url)
   


        
if __name__ == '__main__':
        app.run(debug=True)

