from PIL import Image
import io
from PIL import ImageFile
import cv2
import face_recognition
import numpy as np
from datetime import datetime
import random
def makeconnectiontodtabase(mysql,MySQLdb):
    conn=mysql.connection                    #This function can be used to obtain the cursor and connection objects for executing database queries
    cursor=conn.cursor(MySQLdb)
    return cursor,conn

def getallimagesfromdb(cursor):
    cursor.execute("SELECT image FROM professors")
    user=cursor.fetchall() 
    imglist=[]
    
    for i in user:
    #Each row is represented as a dictionary, 
     #where the keys are column names and the values are the corresponding values for each row.
        for k,v in i.items():
             ImageFile.LOAD_TRUNCATED_IMAGES = True  #setting ImageFile.LOAD_TRUNCATED_IMAGES to True allows the PIL library to load and process truncated(missing data) images without raising an exception.
             image=Image.open(io.BytesIO(v))        
             myImageArr = np.asarray(image)            
             imglist.append(myImageArr)
            
    encodelist=[]      
    for img in imglist:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
   
    return encodelist

def getallidfromdb(cursor):
    cursor.execute("SELECT id FROM professors")
    user=cursor.fetchall()
    ids=[]
    for i in user:
        for k,v in i.items():
            ids.append(v)

    return ids        



def getinformationprofessor(cursor,id):
     cursor.execute(f"SELECT * FROM professors WHERE id={id} ")
     professor=cursor.fetchall()
     if professor:
         name=professor[0]['name']
        #  age=professor[0]['age']
         major=professor[0]['major']
         image=professor[0]['image']
         ImageFile.LOAD_TRUNCATED_IMAGES = True
         image=Image.open(io.BytesIO(image))
         myImageArr = np.asarray(image)
         dataimg = Image.fromarray(myImageArr)
         dataimg.save(f'static/images/professors/{id}.jpg')
         img =f'static/images/professors/{id}.jpg'
         lista=[name,major,img]
     return lista


def insertintodb(cursor,name,major,img,dt):
    cursor.execute(f"insert into attendance(name,major,img,date) values ('{name}','{major}','{img}','{dt}')")
    
def exist_name(cursor,name,d1):
    cursor.execute(f"select name from attendance where date between '{d1} 00:00:00' and '{d1} 23:59:59'")
    row=cursor.fetchall()
    for ro in row:
        if ro["name"]==name:
            return True
    return False

def getallattendaceatdt(cursor,dt):
    cursor.execute(f"select * from attendance where DATE(date)='{dt}' ")
    row=cursor.fetchall()
    names=[]
    majors=[]
    # ages=[]
    imgs=[]
    times=[]
    for ro in row:
        name=ro["name"]
        major=ro["major"]
        # age=ro["age"]
        img=ro["img"]
        date=ro["date"]
        time=date.strftime("%H:%M:%S")
      
        names.append(name)
        majors.append(major)
        # ages.append(age)
        imgs.append(img)
        times.append(time)

    mylist=[names,majors,imgs,times]    
    return mylist

def insert_professor(cursor, id, name, major, year, image):
    # Check if the name already exists in professors table
    select_query = "SELECT name FROM professors WHERE name = %s"
    cursor.execute(select_query, (name,))
    existing_row = cursor.fetchone()

    if not existing_row:
        query = "INSERT INTO professors (id, name, major, yearstart, image) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (id, name, major, year, image))
        return True

    return False



def getallmissingprofessorsatdt(cursor,date):
    cursor.execute(f"SELECT professors.* FROM professors LEFT JOIN attendance ON professors.name = attendance.name and DATE(attendance.date)='{date}' WHERE attendance.name IS NULL and professors.totalattendance !=0;")
    row=cursor.fetchall()
    names=[]
    majors=[]
    ids=[]
    imgs=[]
    for ro in row:
        id=ro["id"]
        name=ro["name"] 
        major=ro["major"]
        # image=ro["image"]
        # image=Image.open(io.BytesIO(image))
        # myImageArr = np.asarray(image)
        # dataimg = Image.fromarray(myImageArr)
        # dataimg.save(f'static/images/professors/{id}.jpg')
        img =f'{id}.jpg'
        

        names.append(name)
        majors.append(major)
        ids.append(id)
        imgs.append(img)
    mylist=[ids,names,majors,imgs]
    return mylist

# def selectinsertrepport(cursor,daterepport,listnames):
#     for name in listnames:
#         query="select name,age,major,lastattendance from professors where name=%s"
#         cursor.execute(query,(name,))
#         result=cursor.fetchone()

#         if result:
#             insert_query="insert into repport (name,age,major,lastattendance,RD) values (%s,%s,%s,%s,%s)"
#             cursor.execute(insert_query, (result["name"],result["age"],result["major"],result["lastattendance"],daterepport))
def select_insert_repport(cursor, daterepport, listnames):
    insertion_success = False  
    for name in listnames:
        query = "SELECT name, major, lastattendance FROM professors WHERE name = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchone()

        if result:
            # Check if the name already exists in repport table
            select_query = "SELECT name FROM repport WHERE name = %s AND RD = %s"
            cursor.execute(select_query, (result["name"], daterepport))
            existing_row = cursor.fetchone()

            if not existing_row:
                insert_query = "INSERT INTO repport (name, major, lastattendance, RD) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_query, (result["name"], result["major"], result["lastattendance"], daterepport))
                insertion_success = True 
             
    return  insertion_success

def selectallrepportatdt(cursor,date):
    query="SELECT * FROM repport where RD=%s"
    cursor.execute(query,(date,))
    row=cursor.fetchall()  
    names=[]
    # ages=[]
    majors=[]
    lastattendances=[]
    rds=[]
    for ro in row:
        name=ro["name"] 
        # age=ro["age"] 
        major=ro["major"] 
        lastattendance=ro["lastattendance"] 
        rd=ro["RD"]
        names.append(name) 
        # ages.append(age)
        majors.append(major) 
        lastattendances.append(lastattendance) 
        rds.append(rd)
    lista=[names,majors,lastattendances,rds]
    return lista