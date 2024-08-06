from flask import Flask, request, make_response, jsonify, Response
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy 
from functools import wraps


import jwt 
import os 
from datetime import date
from cryptography.fernet import Fernet
import datetime
import secrets


app = Flask(__name__)
api = Api(app)

CORS(app)

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

#send email
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image
import io


filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'db360indo.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "cretivoxtechnology22"
key = b'qXkOeccBROMqPi3MCFrNc6czJDrEJopBOpoWWYBKdpE='
fernet = Fernet(key)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    wanumber = db.Column(db.Text)
    desc = db.Column(db.Text)
    email = db.Column(db.Text)
    subject = db.Column(db.Text)

class Project360(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    datadate = db.Column(db.String(255))
    name = db.Column(db.String(255))
    domain = db.Column(db.Text)
    rating = db.Column(db.Integer)
    testimoni = db.Column(db.Text)
    review = db.Column(db.Text)
    cinematic = db.Column(db.Text)
    address = db.Column(db.Text)
    gmaps = db.Column(db.Text)
    ig = db.Column(db.Text)
    #thumbnail image
    thumbnail_img = db.Column(db.Text)
    thumbnail_name = db.Column(db.Text)
    thumbnail_mimetype = db.Column(db.Text)
    #logo image
    logo_img = db.Column(db.Text)
    logo_name = db.Column(db.Text)
    logo_mimetype = db.Column(db.Text)
    #cover image
    cover_img = db.Column(db.Text)
    cover_name = db.Column(db.Text)
    cover_mimetype = db.Column(db.Text)
    #category_relation
    category360_id = db.Column(db.Integer, db.ForeignKey('category360.id'))
    category360 = db.relationship("Category360", back_populates='project360')
    #client_relation
    client360_id = db.Column(db.Integer, db.ForeignKey('client360.id'))
    client360 = db.relationship("Client360", back_populates='project360')
    

class Client360(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    name = db.Column(db.Text)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    position = db.Column(db.String(255))
    company = db.Column(db.String(255))
     #logo image
    logo_img = db.Column(db.Text)
    logo_name = db.Column(db.Text)
    logo_mimetype = db.Column(db.Text)
    #project_relation
    project360 = db.relationship('Project360', back_populates="client360")
    
class Category360(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    name = db.Column(db.Text)
    #project_relation
    project360 = db.relationship('Project360', back_populates="category360")
    
class Pricing360(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    name = db.Column(db.Text)
    desc = db.Column(db.Text)
    price = db.Column(db.Integer)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(255))
    reset_token = db.Column(db.Text)
    reset_exp = db.Column(db.Text)
    email = db.Column(db.Text)
    
    link360 = db.relationship("Link360", back_populates='user')
    
    
class Link360(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    name = db.Column(db.Text)
    bio = db.Column(db.Text)
    domain = db.Column(db.Text)
    #logo image
    logo_img = db.Column(db.Text)
    logo_name = db.Column(db.Text)
    logo_mimetype = db.Column(db.Text)
    
    #InputLink_relation
    
    input360 = db.relationship("Input360", back_populates='link360')
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates="link360")
    
class Input360(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    title = db.Column(db.Text)
    url = db.Column(db.Text)
    status = db.Column(db.Text)
    count = db.Column(db.Integer)
    
    link360_id = db.Column(db.Integer, db.ForeignKey('link360.id'))
    link360 = db.relationship('Link360', back_populates="input360")

db.create_all()

def token_api(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = ""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        
        # token = request.args.get('token') 
        if not token:
            return make_response(jsonify({"msg":"there is no token"}), 401)
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return make_response(jsonify({"msg":"invalid token"}), 401)
        return f(*args, **kwargs)
    return decorator


class LinkIndoall(Resource):
    @token_api
    def post(self):
        datauser = request.form.get('username')
        dataname = request.form.get('name')
        databio = request.form.get('bio')
        datadomain = request.form.get("domain")
        
        dbuser = User.query.all()
        queryuser = [data.username for data in User.query.all()]
        
        if datauser in queryuser :
            for i in range(len(dbuser)):
                if dbuser[i].username == datauser:
                    id_user= dbuser[i].id
        
        #image
        pic = request.files['logo']
        print(pic)
        if not pic :
            print("")
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            print("")

        dataModel = Link360(name = dataname, bio = databio, logo_img = pic.read(), domain = datadomain,
                            logo_name = filename, logo_mimetype = mimetype, user_id = id_user)
        db.session.add(dataModel)
        db.session.commit()
        return make_response(jsonify({"msg":"success"}), 200)

    def get(self):
        dataQuery = Link360.query.all()
        output = [{
            "id" : data.id,
            "data" : {
                "name" : data.name,
                "bio" : data.bio,
                "logo" : "http://192.168.1.253:2022/360/linktree-logo/"+ str(data.id),
                "domain" : data.domain
                
            }        
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
    @token_api
    def delete(self):
        # token = ""
        # auth_header = request.headers.get('Authorization')
        # if auth_header:
        #     token = auth_header.split(" ")[1]
        # decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        # if decoded_token["username"] == "admin":
        db.session.query(Link360).delete()
        db.session.commit()
            
        return jsonify({"msg":"Deleted"}) 
        # else:
        #     return jsonify({"msg" : "Only Admin"})

class LinkIndoid(Resource):
    def get(self,id):
        data = Link360.query.filter(Link360.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "name" : data.name,
                "bio" : data.bio,
                "logo" : "http://192.168.1.253:2022/360/linktree-logo/"+ str(data.id),
                "domain" : data.domain
            }        
        }
        ]
        return make_response(jsonify(output), 200)
    
    @token_api
    def put(self,id):
        dataUpdate = Link360.query.filter(Link360.id == id).first()
        dataname = request.form.get('name')
        databio = request.form.get('bio')
        datauser = request.form.get('username')
        datadomain = request.form.get('domain')
        
        dbuser = User.query.all()
        queryuser = [data.username for data in User.query.all()]
        
        if datauser in queryuser :
            for i in range(len(dbuser)):
                if dbuser[i].username == datauser:
                    id_user= dbuser[i].id
        # token = ""
        # auth_header = request.headers.get('Authorization')
        # if auth_header:
        #     token = auth_header.split(" ")[1]
        # decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        # print(decoded_token["username"])
        # if decoded_token["username"] == "admin" :
        #image
        pic = request.files['logo']
        if not pic :
            print("not pic")
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        print(filename)
        if not filename or not mimetype:
            print("not filename and mimetype")
        
        if dataname:
            dataUpdate.name = dataname
        if databio:
            dataUpdate.bio = databio
        if pic:
            dataUpdate.logo_img = pic.read()
            dataUpdate.logo_name = filename
            dataUpdate.logo_mimetype = mimetype
        if datauser:
            dataUpdate.user_id = id_user
        if datadomain:
            dataUpdate.domain = datadomain

        db.session.commit()
        return make_response(jsonify({"msg" : "updated"}),200)
        # else:
        #     return jsonify({"msg" : "Failed"})
    @token_api
    def delete(self,id):
        own = Link360.query.filter(Link360.id == id).first()
        # token = ""
        # auth_header = request.headers.get('Authorization')
        # if auth_header:
        #     token = auth_header.split(" ")[1]
        # decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        # print(decoded_token["username"])
        # if decoded_token["username"] == "admin" or decoded_token["username"] == own.username:
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})
        # else:
        #     return jsonify({"msg" , "Failed"})
    
class GetImgLink(Resource):
    def get(self, id):
        print(id)
        img = Link360.query.filter(Link360.id == id).first()
        # print(img.img)
        if not img:
           return jsonify({"msg":"bad request"}) 
       
        # webp_data = io.BytesIO(img.logo_img)
        # return Response(webp_data, mimetype='image/webp')
        return Response(img.logo_img, mimetype=img.logo_mimetype) 

class InputLinkall(Resource):
    @token_api
    def post(self):
        datatitle = request.form.get('title')
        dataurl = request.form.get('url')
        datalist= request.form.get('id_profile')
        datastatus = request.form.get('status')
       
        
        dataModel = Input360(title = datatitle , url = dataurl, status= datastatus, link360_id=datalist, count = 0)
        db.session.add(dataModel)
        db.session.commit()
        return make_response(jsonify({"msg":"success"}), 200)
    
    def get(self):
        dataQuery = Input360.query.all()
        output = []
        for data in dataQuery:
            status = False if data.status == "false" else True
            out = {
                "id" : data.id,
                "data" : {
                    "title" : data.title,
                    "url" : data.url,   
                    "status" : status,
                    "count" : data.count   
                }        
            } 
            output.append(out)
            

        return make_response(jsonify(output), 200)
    @token_api
    def delete(self):
        # token = ""
        # auth_header = request.headers.get('Authorization')
        # if auth_header:
        #     token = auth_header.split(" ")[1]
        # decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        # if decoded_token["username"] == "admin":
        db.session.query(Input360).delete()
        db.session.commit()
                
        return jsonify({"msg":"Deleted"}) 
        # else:
        #     return jsonify({"msg" : "Only Admin"})
        
class InputLinkid(Resource):
    def get(self,id):
        data = Input360.query.filter(Input360.id == id).first()
        dataUpdate = Input360.query.filter(Input360.id == id).first()
        datacount = dataUpdate.count + 1
        print(dataUpdate.count)
        dataUpdate.count = datacount
        db.session.commit()
        status = False if data.status == "false" else True
        output = [{
            "id" : data.id,
            "data" : {
                "title" : data.title,
                "url" : data.url,
                "status" : status,
                "count" : data.count
            }        
        }
        ]
        return make_response(jsonify(output), 200)
    @token_api
    def put(self, id):
        dataUpdate = Input360.query.filter(Input360.id == id).first()
        datatitle = request.form.get('title')
        dataurl = request.form.get('url')
        datalink = request.form.get('id_profile')
        datastatus = request.form.get('status')
        
        print(datastatus)
        
        # token = ""
        # auth_header = request.headers.get('Authorization')
        # if auth_header:
        #     token = auth_header.split(" ")[1]
        # decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        # print(decoded_token["username"])
        # if decoded_token["username"] == "admin" :     
        if datatitle:
            dataUpdate.title = datatitle
        if dataurl:
            dataUpdate.url = dataurl
        if datalink:
            dataUpdate.link360_id = datalink
        if datastatus:
            dataUpdate.status = datastatus
        db.session.commit()
        return make_response(jsonify({"msg" : "updated"}), 200)
        # else:
        #     return jsonify({"msg" : "Failed"})
    @token_api
    def delete(self,id):
        own = Input360.query.filter(Input360.id == id).first()
        # token = ""
        # auth_header = request.headers.get('Authorization')
        # if auth_header:
        #     token = auth_header.split(" ")[1]
        # decoded_token = jwt.decode(token, "cretivoxtechnology22", algorithms=['HS256'])
        # print(decoded_token["username"])
        # if decoded_token["username"] == "admin" or decoded_token["username"] == own.username:
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})
        # else:
        #     return jsonify({"msg" : "Failed"})
    
class LinkRelationid(Resource):
    def get(self, id):
        dataQuery = Link360.query.filter(Link360.id == id).first()
        output, listar = [], []
        for x in range(len(dataQuery.input360)):
            status = False if dataQuery.input360[x].status == "false" else True
            listval = {
                "id" : dataQuery.input360[x].id,
                "title" : dataQuery.input360[x].title,
                "url" : dataQuery.input360[x].url,
                "status" : status,
                "count" : dataQuery.input360[x].count
                
            }
            listar.append(listval)
        val = {
            "id" : dataQuery.id,
            "data" : {
                "name" : dataQuery.name,
                "bio" : dataQuery.bio,
                "logo" : "http://192.168.1.253:2022/360/linktree-logo/"+ str(dataQuery.id),
                "domain" : dataQuery.domain,
                "list" : listar
            }
        }
        output.append(val)
        return make_response(jsonify(output), 200) 
    
        
class Userall(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = fernet.encrypt(request.form.get('password').encode())
        dataEmail = request.form.get('email')
        if dataUsername and dataPassword:
            dataModel = User(username=dataUsername, password=dataPassword, email= dataEmail)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"success"}), 200)
        return jsonify({"msg":"Username / password is empty"})
    
    def get(self):
        dataQuery = User.query.all()
        output = [{
            "id" : data.id,
            "username" : data.username,
            "email" : data.email
            
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
    def delete(self):
        db.session.query(User).delete()
        db.session.commit()
                
        return jsonify({"msg":"Deleted"}) 
    
class LoginUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')   
        queryUsername = [data.username for data in User.query.all()]
        queryPassword = [fernet.decrypt(bytes(data.password)).decode()  for data in User.query.all()]

        dblink = User.query.all()
        querylink = [data.username for data in User.query.all()]
        
        if dataUsername in querylink:
            for i in range(len(dblink)):
                if dblink[i].username == dataUsername:
                    id_link= dblink[i].id
        
        data = User.query.filter(User.id == id_link).first()
        
        if dataUsername in queryUsername and dataPassword in queryPassword :
            token = jwt.encode(
                {
                    "username":dataUsername
                }, app.config['SECRET_KEY'],  algorithm="HS256"
            )
            print(data.link360[0].domain)
            output = [{
                "id" : data.link360[0].id,
                "data" : {
                    "name" : data.link360[0].name,
                    "bio" : data.link360[0].bio,
                    "logo" : "http://192.168.1.253:2022/360/linktree-logo/"+ str(data.link360[0].id),
                    "username" : data.username,
                    "token" : token,
                    "domain" : data.link360[0].domain
                }        
            }
            ]
            return make_response(jsonify(output), 200)
        return jsonify({"msg":"failed"})

class Userid(Resource):
    @token_api
    def delete(self,id):
        own = User.query.filter(User.id == id).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})


class Forgot_Password(Resource):
    def post(self):
        datausername = request.form.get('username')
        if not datausername:
            return jsonify({"msg" : "Username is empty"})
        
        dbuser = User.query.all()
        queryuser = [data.username for data in User.query.all()]
        
        if datausername in queryuser:
            token = secrets.token_urlsafe(32)
            expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            for i in range(len(dbuser)):
                if dbuser[i].username == datausername:
                    dbuser[i].reset_token = token
                    dbuser[i].reset_exp = expiration_time
                    db.session.commit()
                    SMTP_SERVER = 'mail.indo360.id'
                    SMTP_PORT = 587
                    SENDER_EMAIL = 'noreply@indo360.id'
                    SENDER_PASSWORD = 'Aku664329#'
                    
                    msg = MIMEMultipart()
                    msg['From'] = SENDER_EMAIL
                    msg['To'] = dbuser[i].email
                    msg['Subject'] = 'Reset Password - Indo360'
                    
                    message = f"Click the following link to reset your password: http://192.168.1.251:4200/recovery/{token}"
                    
                    msg.attach(MIMEText(message, 'plain'))
                    
                    
                    try:
                        # Create a secure connection to the SMTP server
                        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                        server.starttls()
                        
                        # Login to your email account
                        server.login(SENDER_EMAIL, SENDER_PASSWORD)
                        
                        # Send the email
                        server.sendmail(SENDER_EMAIL, dbuser[i].email, msg.as_string())

                        print("Email sent successfully!")
                        server.quit()
                        return jsonify({"msg": "Reset password instructions sent to your email."})
                    except Exception as e:
                        print("An error occurred while sending the email:", str(e))
                        return jsonify({"msg": "Failed"})
                    
                    
                    
            
            
        else:
            return jsonify({"msg" : "User does not exist"})
        
class Reset_Password(Resource):
    def post(self,tokenreset):
        datapassword = fernet.encrypt(request.form.get('password').encode())
        if not datapassword:
            return jsonify({"msg" : "password is empty"})
        
        dbuser = User.query.all()

        # if tokenreset in queryuser:
        for i in range(len(dbuser)):
            print(i)
            print(dbuser[i].reset_token, " ", dbuser[i].reset_exp)
            reset_exp = datetime.datetime.strptime(dbuser[i].reset_exp, '%Y-%m-%d %H:%M:%S.%f')
            if dbuser[i].reset_token == tokenreset and reset_exp > datetime.datetime.utcnow():
                dbuser[i].password = datapassword
                dbuser[i].reset_token = None
                dbuser[i].reset_exp = None
                db.session.commit() 
                return jsonify({"msg": "Password successfully reset."})
        return jsonify({"msg": "Invalid or expired reset token."})
    
        
        
        
        
        


api.add_resource(Forgot_Password, "/360/forgot-password", methods=['POST'])
api.add_resource(Reset_Password, "/360/reset-password/<tokenreset>", methods=['POST'])

api.add_resource(Userall, "/360/register", methods=["POST","GET","DELETE"])
api.add_resource(Userid,"/360/register/<id>", methods=["GET", "PUT", "DELETE"])

api.add_resource(LinkRelationid, "/360/profile/all/<id>", methods=["GET"])

api.add_resource(GetImgLink,"/360/linktree-logo/<id>", methods=["GET"])

api.add_resource(LoginUser, "/360/login", methods=["POST"])

api.add_resource(LinkIndoall, "/360/profile", methods=["POST", "GET", "DELETE"])
api.add_resource(LinkIndoid, "/360/profile/<id>", methods=["GET", "PUT", "DELETE"])

api.add_resource(InputLinkall, "/360/list", methods=["POST", "GET", "DELETE"])
api.add_resource(InputLinkid, "/360/list/<id>", methods=["GET", "PUT", "DELETE"])



if __name__ == "__main__":
    app.run(debug=True,port=2022, host="0.0.0.0")
