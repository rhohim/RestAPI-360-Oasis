from flask import Flask, request, make_response, jsonify, Response
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy 
from functools import wraps


import jwt 
import os 
import datetime 
from cryptography.fernet import Fernet

app = Flask(__name__)
api = Api(app)

CORS(app)

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders


UPLOAD_FOLDER = 'G:/CrevHim/Code/software/test/project2/cv'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#setting database
filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "cretivoxtechnology22"
key = b'qXkOeccBROMqPi3MCFrNc6czJDrEJopBOpoWWYBKdpE='
fernet = Fernet(key)

#ADMIN (REGISTER & LOGIN)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(255))

#CLIEN => PROJECT => LOCATION    
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nameClient = db.Column(db.String(255))
    img = db.Column(db.Text)
    name = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    project = db.relationship('Project', back_populates="client")
    
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nameProject = db.Column(db.String(255))
    desc = db.Column(db.String(255))
    img = db.Column(db.Text)
    name = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship("Location", back_populates='project')
    
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship("Client", back_populates='project')

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    lon = db.Column(db.Text)
    lat = db.Column(db.String(255))
    project = db.relationship('Project', back_populates="location")    
    
#ALL JOB (PROFESIONAL, GRADUATE, STUDENT)
class Profesional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    desc = db.Column(db.Text)
    link = db.Column(db.String(255))
    location = db.Column(db.String(255))
    
class Graduate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    desc = db.Column(db.Text)
    link = db.Column(db.String(255))
    location = db.Column(db.String(255))
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    desc = db.Column(db.Text)
    link = db.Column(db.String(255))
    location = db.Column(db.String(255))
    
class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    desc = db.Column(db.Text)
    link = db.Column(db.String(255))
    location = db.Column(db.String(255))
    typejob = db.Column(db.String(255))


# db.drop_all()
db.create_all()

def token_api(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.args.get('token') 
        print("token ",token)
        if not token:
            return make_response(jsonify({"msg":"there is no token"}), 401)
        # jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return make_response(jsonify({"msg":"invalid / Expired token "}), 401)
        return f(*args, **kwargs)
    return decorator

class RegisterUser(Resource):
    #Create User
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = fernet.encrypt(request.form.get('password').encode())
        

        
        if dataUsername and dataPassword:
            dataModel = User(username=dataUsername, password=dataPassword)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"success"}), 200)
        return jsonify({"msg":"Username / password is empty"})
    
    #Read All User 
    def get(self):
        dataQuery = User.query.all()
        output = [{
            "id" : data.id,
            "username" : data.username
            
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
class Account(Resource):
    #Delete User by id
    def delete(self, username):
        print(username)
        own = User.query.filter(User.id == username).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})
        
class LoginUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')   
        queryUsername = [data.username for data in User.query.all()]
        queryPassword = [fernet.decrypt(bytes(data.password)).decode()  for data in User.query.all()]

        if dataUsername in queryUsername and dataPassword in queryPassword :
            token = jwt.encode(
                {
                    "username":queryUsername, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
                }, app.config['SECRET_KEY'],  algorithm="HS256"
            )
            return make_response(jsonify({"msg":"Content de te revoir " + dataUsername + "!", "token":token}), 200)
        return jsonify({"msg":"failed"})
          

class ProCRUD(Resource):
    #Create Profesional
    # @token_api
    def post(self):
        dataTitle = request.form.get('title')
        dataDesc = request.form.get('desc')
        dataLink = request.form.get('link')  
        dataLoc = request.form.get('location')
        
        if dataTitle and dataDesc and dataLink and dataLoc:
            dataModel = Profesional(title = dataTitle, desc = dataDesc, link= dataLink, location = dataLoc)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg" : "success"}),200)
        return jsonify({"msg","data has empty value"})  
    
    #Read All Profesional
    def get(self):
        typejob = "pro"
        datatest = Jobs.query.filter(Jobs.typejob == typejob).all()
        # print(datatest)
        dataQuery = Profesional.query.all()
        output = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "desc" : data.desc,
                "link" : data.link,
                "location" : data.location
            }
            
            
        } for data in datatest
        ]

        return make_response(jsonify(output), 200)
  
class GetPro(Resource):
    #Read Profesional by id
    def get(self, title):
        # print(data)
        data = Profesional.query.filter(Profesional.id == title).first()
        output = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "desc" : data.desc,
                "link" : data.link,
                "location" : data.location
            }
        }
        ]
        return make_response(jsonify(output), 200)
    #Update Profesional by id    
    # @token_api
    def put(self,title):
        dataTitle = request.form.get('title')
        dataDesc = request.form.get('desc')
        dataLink = request.form.get('link') 
        # print(data)
        dataUpdate = Profesional.query.filter(Profesional.id == title).first()
        if dataTitle and dataDesc and dataLink:
            dataUpdate.title = dataTitle
            dataUpdate.desc= dataDesc
            dataUpdate.link = dataLink
            db.session.commit()
            return make_response(jsonify({"msg" : "updated"}),200)
        return jsonify({"msg","There is empty data"},200)
    
    #Delete Profesional by id
    # @token_api    
    def delete(self, title):
        print(title)
        own =Profesional.query.filter(Profesional.id == title).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"}) 
    
class GradCRUD(Resource):
    #Create Graduate
    # @token_api
    def post(self):
        dataTitle = request.form.get('title')
        dataDesc = request.form.get('desc')
        dataLink = request.form.get('link')  
        dataLoc = request.form.get('location')
        
        if dataTitle and dataDesc and dataLink and dataLoc:
            dataModel = Graduate(title = dataTitle, desc = dataDesc, link= dataLink, location=dataLoc)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg" : "success"}),200)
        return jsonify({"msg","data has empty value"})  
    
    #Read All Graduate
    def get(self):
        dataQuery = Graduate.query.all()
        output = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "desc" : data.desc,
                "link" : data.link,
                "location" : data.location
            }
            
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
class GetGrad(Resource):
    #Read Graduate by id
    def get(self, title):
        # print(data)
        data = Graduate.query.filter(Graduate.id == title).first()
        output = [{
            "id" : data.id,
            "data" : {
                    "title" : data.title,
                    "desc" : data.desc,
                    "link" : data.link,
                    "location" : data.location
                }
        }
        ]
        return make_response(jsonify(output), 200)
    
    #Update Graduate by id    
    # @token_api
    def put(self,title):
        dataTitle = request.form.get('title')
        dataDesc = request.form.get('desc')
        dataLink = request.form.get('link') 
        # print(data)
        dataUpdate = Graduate.query.filter(Graduate.id == title).first()
        if dataTitle and dataDesc and dataLink:
            dataUpdate.title = dataTitle
            dataUpdate.desc= dataDesc
            dataUpdate.link = dataLink
            db.session.commit()
            return make_response(jsonify({"msg" : "updated"}),200)
        return jsonify({"msg","There is empty data"},200)
    
    #Delete Graduate by id
    # @token_api    
    def delete(self, title):
        print(title)
        own =Graduate.query.filter(Graduate.id== title).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})
    
class StuCRUD(Resource):
    #Create Student
    # @token_api
    def post(self):
        dataTitle = request.form.get('title')
        dataDesc = request.form.get('desc')
        dataLink = request.form.get('link')  
        dataLoc = request.form.get('location')
        
        if dataTitle and dataDesc and dataLink and dataLoc:
            dataModel = Student(title = dataTitle, desc = dataDesc, link= dataLink, location =dataLoc)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg" : "success"}),200)
        return jsonify({"msg","data has empty value"})  
    #Read All Student
    def get(self):
        dataQuery = Student.query.all()
        output = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "desc" : data.desc,
                "link" : data.link,
                "location" : data.location
            }
            
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
class GetStu(Resource):
    #Read Student by id
    def get(self, title):
        # print(data)
        data = Student.query.filter(Student.id == title).first()
        output = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "desc" : data.desc,
                "link" : data.link,
                "location" : data.location
            }
        }
        ]
        return make_response(jsonify(output), 200)
    #Update Student by id    
    # @token_api
    def put(self,title):
        dataTitle = request.form.get('title')
        dataDesc = request.form.get('desc')
        dataLink = request.form.get('link') 
        # print(data)
        dataUpdate = Student.query.filter(Student.id == title).first()
        if dataTitle and dataDesc and dataLink:
            dataUpdate.title = dataTitle
            dataUpdate.desc= dataDesc
            dataUpdate.link = dataLink
            db.session.commit()
            return make_response(jsonify({"msg" : "updated"}),200)
        return jsonify({"msg","There is empty data"},200)
    #Delete Student by id
    # @token_api    
    def delete(self, title):
        print(title)
        own =Student.query.filter(Student.id == title).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})
    
class JobCRUD(Resource):
    #Create Jobs
    # @token_api
    def post(self):
        dataTitle = request.form.get('title')
        dataDesc = request.form.get('desc')
        dataLink = request.form.get('link')  
        dataLoc = request.form.get('location')
        datatype = request.form.get('type')
        
        if dataTitle and dataDesc and dataLink and dataLoc and datatype:
            dataModel = Jobs(title = dataTitle, desc = dataDesc, link= dataLink, location =dataLoc, typejob = datatype)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg" : "success"}),200)
        return jsonify({"msg","data has empty value"})  
    #Read All Student
    def get(self):
        dataQuery = Jobs.query.all()
        output = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "desc" : data.desc,
                "link" : data.link,
                "location" : data.location,
                "type" : data.typejob
            }
            
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
class GetJob(Resource):
    #Read Job by id
    def get(self, title):
        # print(data)
        data = Jobs.query.filter(Jobs.id == title).first()
        print(data)
        output = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "desc" : data.desc,
                "link" : data.link,
                "location" : data.location,
                "type" : data.typejob
            }
        }
        ]
        return make_response(jsonify(output), 200)
    #Update Student by id    
    # @token_api
    def put(self,title):
        dataTitle = request.form.get('title')
        dataDesc = request.form.get('desc')
        dataLink = request.form.get('link') 
        dataLoc = request.form.get('location')
        datatype = request.form.get('type')
        # print(data)
        dataUpdate = Jobs.query.filter(Jobs.id == title).first()
        if dataTitle and dataDesc and dataLink:
            dataUpdate.title = dataTitle
            dataUpdate.desc= dataDesc
            dataUpdate.link = dataLink
            dataUpdate.location = dataLoc
            dataUpdate.typejob =  datatype
            db.session.commit()
            return make_response(jsonify({"msg" : "updated"}),200)
        return jsonify({"msg","There is empty data"},200)
    #Delete Student by id
    # @token_api    
    def delete(self, title):
        print(title)
        own =Jobs.query.filter(Jobs.id == title).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})
    
class AllJob(Resource):
    #Read All Jobs
    def get(self):
        dataPro = Profesional.query.all()
        pro = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "desc" : data.desc,
                "link" : data.link,
                "location" : data.location
            }
            
            
        } for data in dataPro
        ]
        
        dataGrad = Graduate.query.all()
        grad = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "desc" : data.desc,
                "link" : data.link,
                "location" : data.location
            }
            
        } for data in dataGrad
        ]
        
        dataStu= Student.query.all()
        stu = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "desc" : data.desc,
                "link" : data.link,
                "location" : data.location
            }
            
        } for data in dataStu
        ]
        
        output = [{
            "Profesional" : pro,
            "Graduate" : grad,
            "Student" : stu
        }]
        
        return make_response(jsonify(output), 200)

class loc(Resource):
    #AS LOCATION
    # Create Location
    def post(self):
        dataName = request.form.get('name')
        dataLon = request.form.get('lon')
        dataLat = request.form.get('lat')
        
        con1 = Location(name=dataName, lon= dataLon, lat=dataLat)

        db.session.add(con1)
        db.session.commit()
        return make_response(jsonify({"msg":"success"}), 200)
    # Read Relation Location    
    def get(self):
        dataQuery = Location.query.all()
        output = [] 
        for i in range(len(dataQuery)):
            loc = []
            for x in range(len(dataQuery[i].project)):
                # print(dataQuery[i].project[x].client.name)
                if len(dataQuery[i].project) > 1:
                    valpro = {
                        "id" : dataQuery[i].project[x].id,
                        "project" : dataQuery[i].project[x].nameProject,
                        "project desc" : dataQuery[i].project[x].desc,
                        "client" : dataQuery[i].project[x].client.nameClient
                    }
                    loc.append(valpro)
                else:
                    loc.append({
                        "id" : dataQuery[i].project[x].id,
                        "project" : dataQuery[i].project[x].nameProject,
                        "project desc" : dataQuery[i].project[x].desc,
                        "client" : dataQuery[i].project[x].client.nameClient
                    })
                    
            val = {
                "id" : dataQuery[i].id,
                "data" : {
                    "location" : dataQuery[i].name,
                    "lng" : dataQuery[i].lon,
                    "lat" : dataQuery[i].lat,
                    "project" : loc
                }
            }
            output.append(val)
        return make_response(jsonify(output), 200)  
        
class project(Resource):
    #AS PROJECTTTTTTT
    #Create Project
    def post(self):
        dataName = request.form.get('name')
        dataDesc = request.form.get('desc')
        dataLoc = request.form.get('loc')
        dataclient= request.form.get('client')
        pic = request.files['pic']
        if not pic :
            return jsonify({"msg" : "picture not allowed"})
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return jsonify({"msg":"bad upload"})
        
        dbLoc= Location.query.all()
        dbClient= Client.query.all()
        queryowner = [data.name for data in Location.query.all()]
        queryclient = [data.nameClient for data in Client.query.all()]
        if dataLoc in queryowner and dataclient in queryclient:
            for i in range(len(dbLoc)):
                if dbLoc[i].name == dataLoc:
                    id_loc= dbLoc[i].id
                    print(id_loc)
            for i in range(len(dbClient)):
                if dbClient[i].nameClient == dataclient:
                    id_client = dbClient[i].id
                    print(id_client)    
        else:
            return {"msg":"there is no location or client name"} 
               
        con1 = Project(nameProject = dataName, desc = dataDesc, location_id = id_loc, client_id = id_client, img=pic.read(), 
                               name = filename , mimetype = mimetype)

        # db.session.add(own)
        db.session.add(con1)
        # db.session.add(con2)
        # db.session.add(con3)

        db.session.commit()
        return make_response(jsonify({"msg":"success"}), 200)
    #Read all Project 
    def get(self):
        dataQuery = Project.query.all()
        # print(dataQuery)
        output = [{
            "id" : data.id,
            "data" : {
                "name" : data.nameProject,
                "desc" : data.desc,
                "image" : "http://50.50.50.220:2022/api/projects/" + str(data.id) ,
            }
        } for data in dataQuery
        ]
        return make_response(jsonify(output), 200)
    
class projectto(Resource):
    #Read Project by id
    def get(self, id):
        # print(data)
        data = Project.query.filter(Project.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "name" : data.nameProject,
                "desc" : data.desc,
                "image" : "http://50.50.50.220:2022/api/projects/" + str(data.id) ,
            }
        }
        ]
        return make_response(jsonify(output), 200)
    
    # Update Client by id
    # @token_api
    def put(self,id):
        dataName = request.form.get('name')
        dataDesc = request.form.get('desc')
        dataLoc = request.form.get('loc')
        dataclient= request.form.get('client')
        pic = request.files['pic']
        # print(id)
        dataUpdate = Project.query.filter(Project.id == id).first()
        # print(dataUpdate.nameClient)
        if not pic :
            return jsonify({"msg" : "picture not allowed"})
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return jsonify({"msg":"bad upload"})
        
        dbLoc= Location.query.all()
        dbClient= Client.query.all()
        queryowner = [data.name for data in Location.query.all()]
        queryclient = [data.nameClient for data in Client.query.all()]
        if dataLoc in queryowner and dataclient in queryclient:
            for i in range(len(dbLoc)):
                if dbLoc[i].name == dataLoc:
                    id_loc= dbLoc[i].id
                    print(id_loc)
            for i in range(len(dbClient)):
                if dbClient[i].nameClient == dataclient:
                    id_client = dbClient[i].id
                    print(id_client)    
        else:
            return {"msg":"there is no location or client name"}
        
        if dataName and pic:
            dataUpdate.nameProject = dataName
            dataUpdate.desc = dataDesc
            dataUpdate.location_id = id_loc
            dataUpdate.client_id = id_client
            dataUpdate.img = pic.read()
            dataUpdate.name = filename 
            dataUpdate.mimetype = mimetype
            db.session.commit()
            return make_response(jsonify({"msg":"updated"}), 200)
        return jsonify({"msg":"Name/Title is empty"})
    
    #Delete Project by id
    def delete(self, id):
        # print(id)
        # own2 = None
        own = Project.query.filter(Project.id == id).first()
        db.session.delete(own)
        db.session.commit()
        
        return jsonify({"msg":"Deleted"})

class projectrel(Resource):
    #Read Relation Project 
    def get(self):
        dataQuery = Project.query.all()
        # print(dataQuery)
        output = []
        for i in range(len(dataQuery)):
            val = {
                "id" : dataQuery[i].id,
                "data" : {
                    "name" : dataQuery[i].nameProject,
                    "desc" : dataQuery[i].desc,
                    "image" : "http://50.50.50.220:2022/api/projects/" + str(dataQuery[i].id) ,
                    "location" : {
                        "id" : dataQuery[i].location.id,
                        "location" : dataQuery[i].location.name
                    },
                    "client" : dataQuery[i].client.nameClient 
                }
            }   
            output.append(val)
        return make_response(jsonify(output), 200)

class projectrelid(Resource):
    def get(self, id):
        dataQuery = Project.query.filter(Project.id == id).first()
        # print(dataQuery)
        # print(dataQuery.client.nameClient)
        output = []
        val = {
            "id" : dataQuery.id,
            "data" : {
                "name" : dataQuery.nameProject,
                "desc" : dataQuery.desc,
                "image" : "http://50.50.50.220:2022/api/projects/" + str(dataQuery.id) ,
                "location" : {
                    "id" : dataQuery.location.id,
                    "location" : dataQuery.location.name
                },
                "client" : dataQuery.client.nameClient 
            }
        }   
        output.append(val)
        return make_response(jsonify(output), 200)
        
class GetImgProject(Resource):
    def get(self, data):
        print(data)
        img = Project.query.filter(Project.id == data).first()
        # print(img.img)
        if not img:
           return jsonify({"msg":"bad request"}) 
        return Response(img.img, mimetype=img.mimetype)   
    
class clientto(Resource):
    #Create Client
    @token_api
    def post(self):
        dataClient = request.form.get('client')
        pic = request.files['pic']
        if not pic :
            return jsonify({"msg" : "picture not allowed"})
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return jsonify({"msg":"bad upload"})
        
        if dataClient:
            dataModel = Client(nameClient=dataClient, img=pic.read(), 
                               name = filename , mimetype = mimetype)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"success"}), 200)
        return jsonify({"msg":"Name/Title is empty"})
    #Read Relation Client    
    def get(self):
        dataQuery = Client.query.all()
        # print(dataQuery[0].consumable)
        output = output = [{
            "id" : data.id,
            "data" : {
                "client name" : data.nameClient,
                "image" : "http://50.50.50.220:2022/api/clients/" + str(data.id) ,
            }
        } for data in dataQuery
        ]
        return make_response(jsonify(output), 200)
    
class clientto2(Resource):
    #Read Client by id
    def get(self, id):
        # print(data)
        data = Client.query.filter(Client.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "client name" : data.nameClient,
                "image" : "http://50.50.50.220:2022/api/clients/" + str(data.id) ,
            }
        }
        ]
        return make_response(jsonify(output), 200)
    
    # Update Client by id
    # @token_api
    def put(self,id):
        dataName = request.form.get('client')
        pic = request.files['pic']
        # print(id)
        dataUpdate = Client.query.filter(Client.id == id).first()
        # print(dataUpdate.nameClient)
        if not pic :
            return jsonify({"msg" : "picture not allowed"})
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return jsonify({"msg":"bad upload"})
        
        if dataName and pic:
            dataUpdate.nameClient = dataName
            dataUpdate.img = pic.read()
            dataUpdate.name = filename 
            dataUpdate.mimetype = mimetype
            db.session.commit()
            return make_response(jsonify({"msg":"updated"}), 200)
        return jsonify({"msg":"Name/Title is empty"})
    
    # Delete Client by id
    # @token_api
    def delete(self, id):
        # print(id)
        # own2 = None
        own = Client.query.filter(Client.id == id).first()
        own2 = Project.query.filter(Project.client_id == id).first()
        if own2 != None :
            db.session.delete(own2)
        
        db.session.delete(own)
        db.session.commit()
        
        return jsonify({"msg":"Deleted"})
    
class clientrel(Resource):
    #Read Relation Client    
    def get(self):
        dataQuery = Client.query.all()
        # print(dataQuery[0].consumable)
        output, datcl = [],[]
        for i in range(len(dataQuery)):
            datpro = []
            for x in range(len(dataQuery[i].project)):
                # print(dataQuery[i].project[x].chemical)
                # print(dataQuery[i].project[x].owner.username)
                val = {
                    "id" : dataQuery[i].project[x].id,
                    "data" : {
                        "project name" :dataQuery[i].project[x].nameProject,
                        "location" : {
                            "id" : dataQuery[i].project[x].location.id,
                            "data" : {
                                "location" : dataQuery[i].project[x].location.name
                            }
                        }
                    }
                    
                }
                datpro.append(val)
            # print(dataQuery[i].name)
            cl = {
                "id" : dataQuery[i].id,
                "data" : {
                    "client name" : dataQuery[i].nameClient,
                    "image" : "http://50.50.50.220:2022/api/clients/" + str(dataQuery[i].id) ,
                    "project" : datpro
                }
                
            }
            datcl.append(cl)
        output.append(datcl)
        return make_response(jsonify(output), 200)
    
class clientrelid(Resource):
    #Read Relation Client    
    def get(self,id):
        data = Client.query.filter(Client.id == id).first()
        print(data.project)
        output, datcl = [],[]
        # for i in range(len(dataQuery)):
        datpro = []
        for x in range(len(data.project)):
            # print(data.project[x].chemical)
            # print(data.project[x].owner.username)
            val = {
                "id" : data.project[x].id,
                "data" : {
                    "project name" :data.project[x].nameProject,
                    "location" : {
                        "id" : data.project[x].location.id,
                        "data" : {
                            "location" : data.project[x].location.name
                        }
                    }
                }
                
            }
            datpro.append(val)
        #     # print(dataQuery[i].name)
        cl = {
            "id" : data.id,
            "data" : {
                "client name" : data.nameClient,
                "image" : "http://50.50.50.220:2022/api/clients/" + str(data.id) ,
                "project" : datpro
            }
            
        }
        #     datcl.append(cl)
        output.append(cl)
        return make_response(jsonify(output), 200)

class GetImg(Resource):
    def get(self, data):
        print(data)
        img = Client.query.filter(Client.id == data).first()
        if not img:
           return jsonify({"msg":"bad request"}) 
        return Response(img.img, mimetype=img.mimetype)
    
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/api/upload', methods=['GET', 'POST'])
class UpPdf(Resource):
    def post(self):
        datasub = request.form.get('subject')
        databod = request.form.get('body')
        file = request.files['file']
        if file.filename == '':
            return jsonify({"msg":"empty file"})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(file.filename)
            
        
        smtp_port = 587                 
        smtp_server = "smtp.gmail.com"  
        email_from = "getpc2022@gmail.com"
        pswd = "ogjnoeylpyxgqxrb"
        

        # Define the email function (dont call it email!)
        person = "rhohim27@gmail.com"
        # Make the body of the email
        body = f'''
        {''.join(databod)}
        '''

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = datasub

        # Define the file to attach
        filename = 'G:/CrevHim/Code/software/test/project2/cv/'+file.filename

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        attachment= open(filename, 'rb')  # r for read and b for binary

        # Encode as base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)

        # Cast as string
        text = msg.as_string()

        # Connect with the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Succesfully connected to server")
        print()


        # Send emails to "person" as list is iterated
        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

        # Close the port
        TIE_server.quit()
        
        return "success"


        # Run the function
        
   


        
      
        
        
    


#Upload PDF
api.add_resource(UpPdf, "/api/upload", methods=["POST"])      
    
    
#REGISTER USER (POST, GET, DELETE)        
api.add_resource(RegisterUser, "/api/register", methods=["POST","GET"])
api.add_resource(Account,"/api/register/<username>", methods=["DELETE"])

#Login
api.add_resource(LoginUser, "/api/login", methods=["POST"])

#CLIENT 
api.add_resource(clientto, "/api/client", methods=["POST","GET"]) 
api.add_resource(clientto2, "/api/client/<id>", methods=["GET", "PUT" , "DELETE"])
api.add_resource(clientrel,"/api/client/populate", methods=["GET"])
api.add_resource(clientrelid,"/api/client/populate/<id>", methods=["GET"])
api.add_resource(GetImg,"/api/clients/<data>", methods=["GET"])


#Pro
api.add_resource(ProCRUD, "/api/job/profesional", methods=["POST", "GET"])
api.add_resource(GetPro,"/api/job/profesional/<title>", methods=["GET", "PUT", "DELETE"])

#Grad
api.add_resource(GradCRUD, "/api/job/graduate", methods=["POST", "GET"])
api.add_resource(GetGrad, "/api/job/graduate/<title>", methods=["GET", "PUT", "DELETE"])

#Stud
api.add_resource(StuCRUD, "/api/job/student", methods=["POST", "GET"])
api.add_resource(GetStu, "/api/job/student/<title>", methods=["GET", "PUT", "DELETE"])

#AllJob
api.add_resource(AllJob, "/api/job/all", methods=[ "GET"])

#Location
api.add_resource(loc, "/api/location", methods=["POST","GET"])

#Project
api.add_resource(project, "/api/project", methods=["POST","GET"]) 
api.add_resource(projectto,"/api/project/<id>", methods=["GET","PUT", "DELETE"])
api.add_resource(projectrel, "/api/project/populate", methods=["GET"]) 
api.add_resource(projectrelid, "/api/project/populate/<id>", methods=["GET"]) 
api.add_resource(GetImgProject,"/api/projects/<data>", methods=["GET","PUT", "DELETE"])


#Jobs
api.add_resource(JobCRUD, "/api/job", methods=["POST", "GET"])
api.add_resource(GetJob,"/api/job/<title>", methods=["GET", "PUT", "DELETE"])



if __name__ == "__main__":
    app.run(debug=True,port=2022, host="0.0.0.0")
    