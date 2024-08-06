from flask import Flask, request, make_response, jsonify, Response
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy 
from functools import wraps


import jwt 
import os 
import datetime 

app = Flask(__name__)
api = Api(app)

CORS(app)

application = app

#setting database
filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "cretivoxtechnology22"

#make database and column
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nameClient = db.Column(db.String(255))
    title = db.Column(db.String(255))
    img = db.Column(db.Text)
    name = db.Column(db.Text)
    mimetype = db.Column(db.Text)

class Profesional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    desc = db.Column(db.Text)
    link = db.Column(db.String(255))
    
class Graduate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    desc = db.Column(db.Text)
    link = db.Column(db.String(255))
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    desc = db.Column(db.Text)
    link = db.Column(db.String(255))


#db.drop_all()
db.create_all()

def token_api(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.args.get('token') 
        if not token:
            return make_response(jsonify({"msg":"there is no token"}), 401)
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return make_response(jsonify({"msg":"invalid token"}), 401)
        return f(*args, **kwargs)
    return decorator

class RegisterUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')
        

        if dataUsername and dataPassword:
            dataModel = User(username=dataUsername, password=dataPassword)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"success"}), 200)
        return jsonify({"msg":"Username / password is empty"})
    
    def get(self):
        dataQuery = User.query.all()
        output = [{
            "id" : data.id,
            "username" : data.username
            
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
class Account(Resource):
    def delete(self, username):
        print(username)
        own = User.query.filter(User.username == username).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})
        
class LoginUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        queryUsername = [data.username for data in User.query.all()]
        queryPassword = [data.password for data in User.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword :
            token = jwt.encode(
                {
                    "username":queryUsername, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
                }, app.config['SECRET_KEY'],  algorithm="HS256"
            )
            return make_response(jsonify({"msg":"Content de te revoir " + dataUsername + "!", "token":token}), 200)
        return jsonify({"msg":"failed"})
    
class ClientCRUD(Resource):
    @token_api
    def post(self):
        dataName = request.form.get('name')
        dataTitle = request.form.get('title')     
        #get image
        pic = request.files['pic']
        if not pic :
            return jsonify({"msg" : "picture not allowed"})
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return jsonify({"msg":"bad upload"})
        
        if dataName and dataTitle:
            dataModel = Client(nameClient=dataName, title=dataTitle,img=pic.read(), 
                               name = filename , mimetype = mimetype)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"success"}), 200)
        return jsonify({"msg":"Name/Title is empty"})
    
    def get(self):
        dataQuery = Client.query.all()
        output = [{
            "id" : data.id,
            "name" : data.nameClient,
            "title" : data.title,
            "image" : "https://api.yourtyper.com/api/client/" + str(data.id)
            
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
        

class GetImg(Resource):
    def get(self, data):
        print(data)
        img = Client.query.filter(Client.id == data).first()
        print(img)
        if not img:
           return jsonify({"msg":"bad request"}) 
        return Response(img.img, mimetype=img.mimetype)
    @token_api
    def put(self,data):
        dataName = request.form.get('name')
        dataTitle = request.form.get('title')
        pic = request.files['pic']
        # print(data)
        dataUpdate = Client.query.filter(Client.id == data).first()
        # print(dataUpdate.nameClient)
        if not pic :
            return jsonify({"msg" : "picture not allowed"})
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return jsonify({"msg":"bad upload"})
        
        if dataName and dataTitle:
            dataUpdate.nameClient = dataName
            dataUpdate.title = dataTitle
            dataUpdate.img=pic.read()
            dataUpdate.name = filename 
            dataUpdate.mimetype = mimetype
            db.session.commit()
            return make_response(jsonify({"msg":"updated"}), 200)
        return jsonify({"msg":"Name/Title is empty"})
    @token_api
    def delete(self, data):
        print(data)
        own =Client.query.filter(Client.id == data).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})
    
class ProCRUD(Resource):
    @token_api
    def post(self):
        dataTitle = request.form.get('title')
        dataDesc = request.form.get('desc')
        dataLink = request.form.get('link')  
        
        if dataTitle and dataDesc and dataLink:
            dataModel = Profesional(title = dataTitle, desc = dataDesc, link= dataLink)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg" : "success"}),200)
        return jsonify({"msg","data has empty value"})  
    
    def get(self):
        dataQuery = Profesional.query.all()
        output = [{
            "id" : data.id,
            "title" : data.title,
            "desc" : data.desc,
            "link" : data.link
            
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)

    
    
class GetPro(Resource):
    def get(self, title):
        # print(data)
        data = Profesional.query.filter(Profesional.id == title).first()
        output = [{
            "id" : data.id,
            "title" : data.title,
            "desc" : data.desc,
            "link" : data.link
        }
        ]
        return make_response(jsonify(output), 200)
        
    @token_api
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
    @token_api    
    def delete(self, title):
        print(title)
        own =Profesional.query.filter(Profesional.id == title).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"}) 
    
class GradCRUD(Resource):
    @token_api
    def post(self):
        dataTitle = request.form.get('title')
        dataDesc = request.form.get('desc')
        dataLink = request.form.get('link')  
        
        if dataTitle and dataDesc and dataLink:
            dataModel = Graduate(title = dataTitle, desc = dataDesc, link= dataLink)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg" : "success"}),200)
        return jsonify({"msg","data has empty value"})  
    
    def get(self):
        dataQuery = Graduate.query.all()
        output = [{
            "id" : data.id,
            "title" : data.title,
            "desc" : data.desc,
            "link" : data.link
            
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
class GetGrad(Resource):
    def get(self, title):
        # print(data)
        data = Graduate.query.filter(Graduate.id == title).first()
        output = [{
            "id" : data.id,
            "title" : data.title,
            "desc" : data.desc,
            "link" : data.link
        }
        ]
        return make_response(jsonify(output), 200)
        
    @token_api
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
    
    @token_api    
    def delete(self, title):
        print(title)
        own =Graduate.query.filter(Graduate.id== title).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})
    
class StuCRUD(Resource):
    # @token_api
    def post(self):
        dataTitle = request.form.get('title')
        dataDesc = request.form.get('desc')
        dataLink = request.form.get('link')  
        
        if dataTitle and dataDesc and dataLink:
            dataModel = Student(title = dataTitle, desc = dataDesc, link= dataLink)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg" : "success"}),200)
        return jsonify({"msg","data has empty value"})  
    
    def get(self):
        dataQuery = Student.query.all()
        output = [{
            "id" : data.id,
            "title" : data.title,
            "desc" : data.desc,
            "link" : data.link
            
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
class GetStu(Resource):
    def get(self, title):
        # print(data)
        data = Student.query.filter(Student.id == title).first()
        output = [{
            "id" : data.id,
            "title" : data.title,
            "desc" : data.desc,
            "link" : data.link
        }
        ]
        return make_response(jsonify(output), 200)
        
    @token_api
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
    
    @token_api    
    def delete(self, title):
        print(title)
        own =Student.query.filter(Student.id == title).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})
    
class AllJob(Resource):
    def get(self):
        dataPro = Profesional.query.all()
        pro = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "desc" : data.desc,
                "link" : data.link
            }
            
            
        } for data in dataPro
        ]
        
        dataGrad = Graduate.query.all()
        grad = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "desc" : data.desc,
                "link" : data.link
            }
            
        } for data in dataGrad
        ]
        
        dataStu= Student.query.all()
        stu = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "desc" : data.desc,
                "link" : data.link
            }
            
        } for data in dataStu
        ]
        
        output = [{
            "Profesional" : pro,
            "Graduate" : grad,
            "Student" : stu
        }]
        
        return make_response(jsonify(output), 200)

        
        
        
    

       
    
    

#REGISTER USER (POST, GET, DELETE)        
api.add_resource(RegisterUser, "/api/register", methods=["POST","GET"])
api.add_resource(Account,"/api/register/<username>", methods=["DELETE"])

#Login
api.add_resource(LoginUser, "/api/login", methods=["POST"])

#CLIENT 
api.add_resource(ClientCRUD, "/api/client", methods=["POST","GET"])
api.add_resource(GetImg,"/api/client/<data>", methods=["GET","PUT", "DELETE"])

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

    


if __name__ == "__main__":
    app.run(debug=True)
    