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
app.app_context().push()
api = Api(app)

CORS(app)

import os
from werkzeug.utils import secure_filename

#send email
import os
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from PIL import Image
import io

filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'db360.sqlite')
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


class UpMsg(Resource):
    def post(self):
        dataname = request.form.get('name')
        datawa = request.form.get('wa_number')
        datadescb = request.form.get('describe')
        dataemail = request.form.get("email")
        datasubject = request.form.get('subject')
        print(dataname)
        dataModel = Email(name = dataname, wanumber = datawa, desc = datadescb , email = dataemail, subject = datasubject)
        db.session.add(dataModel)
        db.session.commit()
        
        # return make_response(jsonify({"msg":"success"}), 200)
        smtp_port = 587                 
        smtp_server = "smtp.gmail.com"  
        email_from = "cretivox.app@gmail.com"
        pswd = "trhnycwpgpjgfomh"
        

        person = ["getpc2022@gmail.com", "cretivox.dev@gmail.com"]
        template = '''
                <html>
                <head>
                <style>
                </style>
                </head>
                <body>
                <h2>Please follow-up this data from Website.</h2>
                <ul>
                <li>Name: <strong>{name}</strong></li>
                <li>Wa: <strong>{wa_number}</strong></li>
                <li>Email: <strong>{email}</strong></li>
                <li>Description: <strong>{description}</strong></li>
                </ul>
                <p>This data will save on database.</p>
                </body>
                </html>
                '''
        body = template.format(
            name=dataname,
            wa_number=datawa,
            email=dataemail,
            description=datadescb
        )

        try:
        # Create a MIME object to define parts of the email
            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = ", ".join(person)
            msg['Subject'] = '(Indo360.id) - ' + datasubject.capitalize() +" - " + dataname.capitalize()

            # Attach the body of the message
            msg.attach(MIMEText(body, 'html'))

            # Create a secure connection with the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

            # Login to the sender's email account
            server.login(email_from, pswd)

            # Send the email
            server.sendmail(email_from, person, msg.as_string())
            print(f"Email sent to: {person}")

            # Close the connection
            server.quit()

            return jsonify({"msg": "Success"})

        except Exception as e:
            print("An error occurred while sending the email:", str(e))
            return jsonify({"msg": "Failed"})
        
        # make a MIME object to define parts of the email
        # msg = MIMEMultipart()
        # msg['From'] = email_from
        # msg['To'] = ", ".join(person)
        # msg['Subject'] = 'Indo360.id-Discuss-' + dataname.capitalize()


        # # Attach the body of the message
        # msg.attach(MIMEText(body, 'html'))

        
        # text = msg.as_string()

        # print("Connecting to server...")
        # TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        # TIE_server.starttls()
        # TIE_server.login(email_from, pswd)
        # print("Succesfully connected to server")
        # print()

        
        # print(f"Sending email to: {person}...")
        # TIE_server.sendmail(email_from, person, text)
        # print(f"Email sent to: {person}")
        # print()

        # TIE_server.quit()
        
        # return jsonify({"msg":"Success"})


class Userall(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = fernet.encrypt(request.form.get('password').encode())
        dataEmail = request.form.get('email')
        existing_user = existing_user = User.query.filter((User.username == dataUsername) | (User.email == dataEmail)).first()
        if existing_user:
            return make_response(jsonify({"msg":"Username already exists"}), 200)
        if dataUsername and dataPassword:
            dataModel = User(username=dataUsername, password=dataPassword, email= dataEmail)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"success"}), 200)
        return jsonify({"msg":"Username / password is empty"})
    @token_api 
    # admin
    def get(self):
        dataQuery = User.query.all()
        output = [{
            "id" : data.id,
            "username" : data.username,
            "email" : data.email
            
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    @token_api 
    # admin
    def delete(self):
        db.session.query(User).delete()
        db.session.commit()
                
        return jsonify({"msg":"Deleted"}) 
    
class Userid(Resource):
    @token_api 
    # all
    def get(self,id):
        data = User.query.filter(User.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "username" : data.username,
                "email" : data.email
            }
        }
        ]
        return make_response(jsonify(output), 200)
    @token_api 
    # all
    def put(self,id):
        dataUsername = request.form.get('username')
        dataPassword = fernet.encrypt(request.form.get('password').encode())
        dataEmail = request.form.get('email')
        # existing_user = User.query.filter((User.username == dataUsername) | (User.email == dataEmail)).first()
        # if existing_user:
        #     return make_response(jsonify({"msg":"Username already exists"}), 200)
        dataUpdate = User.query.filter(User.id == id).first()
        if dataUsername:
            dataUpdate.username = dataUsername
        if dataPassword:
            dataUpdate.password = dataPassword
        if dataEmail:
            dataUpdate.email= dataEmail
        db.session.commit()
        return make_response(jsonify({"msg" : "updated"}),200)
    @token_api 
    # all
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

class LoginAdmin(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')   
        queryUsername = [data.username for data in User.query.all()]
        queryPassword = [fernet.decrypt(bytes(data.password)).decode()  for data in User.query.all()]

        print(dataUsername, " ", dataPassword)
        
        if dataUsername in queryUsername and dataPassword in queryPassword :
            token = jwt.encode(
                {
                    "username":dataUsername, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
                }, app.config['SECRET_KEY'],  algorithm="HS256"
            )
            
            output = [{
                    "msg" : "success",
                    "token" : token
            }
            ]
            return make_response(jsonify(output), 200)
        return jsonify({"msg":"failed"})

class LoginUser(Resource):
    # @token_api 
    # admin
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

class Priceall(Resource):
    def post(self):
        dataname = request.form.get('name')
        dataPrice = request.form.get('price')
        datadesc = request.form.get('description')
        dataModel = Pricing360(name = dataname, price = dataPrice, desc = datadesc)
        db.session.add(dataModel)
        db.session.commit()
        return make_response(jsonify({"msg":"success"}), 200)
    
    # @token_api
    def get(self):
        dataQuery = Pricing360.query.all()
        output = [{
            "id" : data.id,
            "data" :  {
                "name" :data.name,
                "price" : data.price,
                "description" : data.desc            
                
            }
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
    def delete(self):
        db.session.query(Pricing360).delete()
        db.session.commit()
                
        return jsonify({"msg":"Deleted"}) 

class Priceid(Resource):
    def get(self,id):
        data = Pricing360.query.filter(Pricing360.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "name" :data.name,
                "price" : data.price,
                "description" : data.desc
            }
        }
        ]
        return make_response(jsonify(output), 200)
    
    def put(self,id):
        dataname = request.form.get('name')
        dataPrice = request.form.get('price')
        datadesc = request.form.get('description')
        # print(data)
        dataUpdate = Pricing360.query.filter(Pricing360.id == id).first()
        if dataPrice:
            dataUpdate.price = dataPrice
        if dataname:
            dataUpdate.name = dataname
        if datadesc:
            dataUpdate.desc= datadesc
        db.session.commit()
        return make_response(jsonify({"msg" : "updated"}),200)
        # return jsonify({"msg","There is empty data"},200)
    
    def delete(self,id):
        own = Pricing360.query.filter(Pricing360.id == id).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})

class Categoryall(Resource):
    @token_api 
    # admin
    def post(self):
        dataname = request.form.get('name')
        print(dataname)
        dataModel = Category360(name = dataname)
        db.session.add(dataModel)
        db.session.commit()
        return make_response(jsonify({"msg":"success"}), 200)
    
    def get(self):
        dataQuery = Category360.query.all()
        output = [{
            "id" : data.id,
            "data" : {
                "name" : data.name,
            }
                     
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
    @token_api 
    # admin
    def delete(self):
        db.session.query(Category360).delete()
        db.session.commit()
                
        return jsonify({"msg":"Deleted"}) 

    
class Categoryid(Resource):
    def get(self,id):
        data = Category360.query.filter(Category360.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "name" : data.name,
            }
        }
        ]
        return make_response(jsonify(output), 200)
    
    @token_api 
    # admin
    def put(self,id):
        dataname = request.form.get('name')
        # print(data)
        dataUpdate = Category360.query.filter(Category360.id == id).first()
        if dataname:
            dataUpdate.name = dataname
        db.session.commit()
        return make_response(jsonify({"msg" : "updated"}),200)
        # return jsonify({"msg","There is empty data"},200)
    
    @token_api 
    # admin
    def delete(self,id):
        own = Category360.query.filter(Category360.id == id).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})
 
class Clientall(Resource):
    @token_api 
    # admin
    def post(self):
        dataname = request.form.get('name')
        dataemail = request.form.get('email')
        dataphone = request.form.get('phone')
        dataposition = request.form.get('position')
        datacompany = request.form.get('company')
        #image
        pic = request.files['logo']
        if not pic :
            return jsonify({"msg" : "picture not allowed"})
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return jsonify({"msg":"bad upload"})
            
        # image = Image.open(pic)
        # image = image.convert('RGB')
        
        # # Create a BytesIO object to store the WebP image data
        # webp_data = io.BytesIO()
        # image.save(webp_data, format='WEBP')
        # webp_data.seek(0)
        
        # Get the WebP image data as bytes
        # webp_data_bytes = webp_data.getvalue()
        
        
        dataModel = Client360(name = dataname, email = dataemail, phone = dataphone, position = dataposition, company = datacompany,
                              logo_img=pic.read(), logo_name = filename, logo_mimetype=mimetype)
        db.session.add(dataModel)
        db.session.commit()
        return make_response(jsonify({"msg":"success"}), 200)
    
    def get(self):
        dataQuery = Client360.query.all()
        output = [{
            "id" : data.id,
            "data" : {
                "name" : data.name,
                "email" : data.email,
                "phone" : data.phone,
                "position" : data.position,
                "company" : data.company,
                "logo" : "http://192.168.1.253:2024/360/clientimg/"+ str(data.id)
            }       
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
    @token_api 
    # admin
    def delete(self):
        db.session.query(Client360).delete()
        db.session.commit()
                
        return jsonify({"msg":"Deleted"})
    
class Clientid(Resource):
    def get(self,id):
        data = Client360.query.filter(Client360.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "name" : data.name,
                "email" : data.email,
                "phone" : data.phone,
                "position" : data.position,
                "company" : data.company,
                "logo" : "http://192.168.1.253:2024/360/clientimg/"+ str(data.id)
            }
        }
        ]
        return make_response(jsonify(output), 200)
    
    @token_api 
    # admin  
    def put(self,id):
        dataname = request.form.get('name')
        dataemail = request.form.get('email')
        dataphone = request.form.get('phone')
        dataposition = request.form.get('position')
        datacompany = request.form.get('company')
        #image
        pic = request.files['logo']
        if not pic :
            print("None")
            # return jsonify({"msg" : "picture not allowed"})
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            print("None")
            # return jsonify({"msg":"bad upload"})
        # print(data)
        
        dataUpdate = Client360.query.filter(Client360.id == id).first()
        if dataname:
            dataUpdate.name = dataname
        if dataemail:
            dataUpdate.email = dataemail
        if dataphone:
            dataUpdate.phone = dataphone
        if dataposition:
            dataUpdate.position = dataposition
        if datacompany:
            dataUpdate.company = datacompany
        if pic:
            dataUpdate.logo_img = pic.read()
            dataUpdate.logo_name = filename 
            dataUpdate.logo_mimetype = mimetype
        db.session.commit()
        return make_response(jsonify({"msg" : "updated"}),200)
        # return jsonify({"msg","There is empty data"},200)
    
    @token_api 
    # admin
    def delete(self,id):
        own = Client360.query.filter(Client360.id == id).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})
    
class GetImgClient(Resource):
    def get(self, id):
        print(id)
        img = Client360.query.filter(Client360.id == id).first()
        # print(img.img)
        if not img:
           return jsonify({"msg":"bad request"}) 
        # webp_data = io.BytesIO(img.logo_img)
        # return Response(webp_data, mimetype='image/webp')
        return Response(img.logo_img, mimetype=img.logo_mimetype) 
    
class GetImgprothumbnail(Resource):
    def get(self, id):
        print(id)
        img = Project360.query.filter(Project360.id == id).first()
        # print(img.img)
        if not img:
           return jsonify({"msg":"bad request"}) 
        webp_data = io.BytesIO(img.thumbnail_img)
        return Response(webp_data, mimetype='image/webp')
        return Response(img.thumbnail_img, mimetype=img.thumbnail_mimetype) 
    
class GetImgprologo(Resource):
    def get(self, id):
        print(id)
        img = Project360.query.filter(Project360.id == id).first()
        # print(img.img)
        if not img:
           return jsonify({"msg":"bad request"}) 
        # webp_data = io.BytesIO(img.logo_img)
        # return Response(webp_data, mimetype='image/webp')
        return Response(img.logo_img, mimetype=img.logo_mimetype) 
    
class GetImgprocover(Resource):
    def get(self, id):
        print(id)
        img = Project360.query.filter(Project360.id == id).first()
        # print(img.img)
        if not img:
           return jsonify({"msg":"bad request"}) 
        webp_data = io.BytesIO(img.cover_img)
        return Response(webp_data, mimetype='image/webp')
        # return Response(img.cover_img, mimetype=img.cover_mimetype) 
    
class Projectall(Resource):
    @token_api 
    # admin
    def post(self):
        today = date.today()
        d2 = today.strftime("%B %d, %Y")
        dataname = request.form.get('name')
        datadomain = request.form.get('domain')
        datarating = request.form.get('rating')
        datatestimoni = request.form.get('testimoni')
        datareview = request.form.get('review')
        datacinematic = request.form.get('cinematic')
        dataaddress = request.form.get('address')
        datagmaps = request.form.get('link_gmaps')
        dataig = request.form.get('instagram')
        #relation_db
        datacategory = request.form.get('category')
        dataclient = request.form.get('client')
        
        #relation_id_category
        dbcategory = Category360.query.all()
        querycategory = [data.name for data in Category360.query.all()]
        
        #relation_id_client
        dbclient = Client360.query.all()
        queryclient = [data.name for data in Client360.query.all()]
        
  
        if datacategory in querycategory and dataclient in queryclient:
            for i in range(len(dbcategory)):
                if dbcategory[i].name == datacategory:
                    id_category= dbcategory[i].id
                    print(id_category)
            for i in range(len(dbclient)):
                if dbclient[i].name == dataclient:
                    id_client = dbclient[i].id
                    print(id_client)    
        else:
            return {"msg":"there is no Category or client name"} 
        
        #img_thumbnail
        pic_thumbnail = request.files['thumbnail']
        if not pic_thumbnail :
            return jsonify({"msg" : "picture not allowed"})
        filename_thumbnail = secure_filename(pic_thumbnail.filename)
        mimetype_thumbnail = pic_thumbnail.mimetype
        if not filename_thumbnail or not mimetype_thumbnail:
            return jsonify({"msg":"bad upload"})
        
        image = Image.open(pic_thumbnail)
        image = image.convert('RGB')
        
        # Create a BytesIO object to store the WebP image data
        webp_data = io.BytesIO()
        image.save(webp_data, format='WEBP')
        webp_data.seek(0)
        
        # Get the WebP image data as bytes
        webp_data_bytes_thumbnail = webp_data.getvalue()
        
        #img_logo
        pic_logo = request.files['logo']
        if not pic_logo :
            return jsonify({"msg" : "picture not allowed"})
        filename_logo = secure_filename(pic_logo.filename)
        mimetype_logo = pic_logo.mimetype
        if not filename_logo or not mimetype_logo:
            return jsonify({"msg":"bad upload"})
        
        # image = Image.open(pic_logo)
        # image = image.convert('RGB')
        
        # # Create a BytesIO object to store the WebP image data
        # webp_data = io.BytesIO()
        # image.save(webp_data, format='WEBP')
        # webp_data.seek(0)
        
        # # Get the WebP image data as bytes
        # webp_data_bytes_logo = webp_data.getvalue()
        
        #img_cover
        pic_cover = request.files['cover']
        if not pic_cover :
            return jsonify({"msg" : "picture not allowed"})
        filename_cover = secure_filename(pic_cover.filename)
        mimetype_cover = pic_cover.mimetype
        if not filename_cover or not mimetype_cover:
            return jsonify({"msg":"bad upload"})
            
        image = Image.open(pic_cover)
        image = image.convert('RGB')
        
        # Create a BytesIO object to store the WebP image data
        webp_data = io.BytesIO()
        image.save(webp_data, format='WEBP')
        webp_data.seek(0)
        
        # Get the WebP image data as bytes
        webp_data_bytes_cover = webp_data.getvalue()
        
        dataModel = Project360(
            datadate = d2,
            name = dataname,
            domain = datadomain,
            rating = datarating,
            testimoni = datatestimoni,
            review = datareview,
            cinematic = datacinematic,
            address = dataaddress,
            gmaps = datagmaps,
            ig = dataig,
            
            thumbnail_img = webp_data_bytes_thumbnail,
            thumbnail_name = filename_thumbnail,
            thumbnail_mimetype = 'image/webp',
            
            logo_img = pic_logo.read(),
            logo_name = filename_logo,
            logo_mimetype = mimetype_logo,
            
            cover_img = webp_data_bytes_cover,
            cover_name = filename_cover,
            cover_mimetype = 'image/webp',
            
            category360_id = id_category,
            client360_id = id_client
            
        )
        db.session.add(dataModel)
        db.session.commit()
        return make_response(jsonify({"msg":"success"}), 200)
    
    def get(self):
        dataQuery = Project360.query.all()
        output = [{
            "id" : data.id,
            "data" : {
                "name" : data.name,
                "date" : data.datadate,
                "domain" : data.domain,
                "rating" : data.rating,
                "testimoni" : data.testimoni,
                "review" : data.review,
                "cinematic" : data.cinematic,
                "instagram" : data.ig,
                "link_gmaps" : data.gmaps,
                "address" : data.address,
                "thumbnail" : "http://192.168.1.253:2024/360/project-thumbnail/"+ str(data.id),
                "logo" : "http://192.168.1.253:2024/360/project-logo/"+ str(data.id),
                "cover" : "http://192.168.1.253:2024/360/project-cover/"+ str(data.id)
            }        
        } for data in dataQuery
        ]

        return make_response(jsonify(output), 200)
    
    @token_api 
    # admin
    def delete(self):
        db.session.query(Project360).delete()
        db.session.commit()
                
        return jsonify({"msg":"Deleted"}) 
    
class Projectid(Resource):

    def get(self,id):
        data = Project360.query.filter(Project360.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "name" : data.name,
                "date" : data.datadate,
                "domain" : data.domain,
                "rating" : data.rating,
                "testimoni" : data.testimoni,
                "review" : data.review,
                "cinematic" : data.cinematic,
                "instagram" : data.ig,
                "link_gmaps" : data.gmaps,
                "address" : data.address,
                "thumbnail" : "http://192.168.1.253:2024/360/project-thumbnail/"+ str(data.id),
                "logo" : "http://192.168.1.253:2024/360/project-logo/"+ str(data.id),
                "cover" : "http://192.168.1.253:2024/360/project-cover/"+ str(data.id)
            }        
        }
        ]
        return make_response(jsonify(output), 200)
    
    @token_api 
    # admin
    def put(self,id):
        dataname = request.form.get('name')
        datadomain = request.form.get('domain')
        datarating = request.form.get('rating')
        datatestimoni = request.form.get('testimoni')
        datareview = request.form.get('review')
        datacinematic = request.form.get('cinematic')
        dataaddress = request.form.get('address')
        datagmaps = request.form.get('link_gmaps')
        dataig = request.form.get('instagram')
        
        
        #img_thumbnail
        pic_thumbnail = request.files['thumbnail']
        if not pic_thumbnail :
            print("None")
            # return jsonify({"msg" : "picture not allowed"})
        filename_thumbnail = secure_filename(pic_thumbnail.filename)
        mimetype_thumbnail = pic_thumbnail.mimetype
        if not filename_thumbnail or not mimetype_thumbnail:
            print("None")
            # return jsonify({"msg":"bad upload"})
        
        #img_logo
        pic_logo = request.files['logo']
        if not pic_logo :
            print("None")
            # return jsonify({"msg" : "picture not allowed"})
        filename_logo = secure_filename(pic_logo.filename)
        mimetype_logo = pic_logo.mimetype
        if not filename_logo or not mimetype_logo:
            print("None")
            # return jsonify({"msg":"bad upload"})
        
        #img_logo
        pic_cover = request.files['cover']
        if not pic_cover :
            print("None")
            # return jsonify({"msg" : "picture not allowed"})
        filename_cover = secure_filename(pic_cover.filename)
        mimetype_cover = pic_cover.mimetype
        if not filename_cover or not mimetype_cover:
            print("None")
            # return jsonify({"msg":"bad upload"})
        
        # print(dataname,datadomain,datarating,datatestimoni)
        
        #relation_db
        datacategory = request.form.get('category')
        dataclient = request.form.get('client')
        
        #relation_id_category
        dbcategory = Category360.query.all()
        querycategory = [data.name for data in Category360.query.all()]
        
        #relation_id_client
        dbclient = Client360.query.all()
        queryclient = [data.name for data in Client360.query.all()]
        
        if datacategory in querycategory or dataclient in queryclient:
            for i in range(len(dbcategory)):
                if dbcategory[i].name == datacategory:
                    id_category= dbcategory[i].id
                    # print(id_category)
            for i in range(len(dbclient)):
                if dbclient[i].name == dataclient:
                    id_client = dbclient[i].id
                    # print(id_client) 
        else:
            print(datacategory, " " , dataclient)  
        
        dataUpdate = Project360.query.filter(Project360.id == id).first()
        if dataname:
            dataUpdate.name = dataname
        if datadomain:
            dataUpdate.domain = datadomain
        if datarating:
            dataUpdate.rating = datarating
        if datatestimoni:
            dataUpdate.testimoni = datatestimoni
        if datareview:
            dataUpdate.review = datareview
        if datacinematic:
            dataUpdate.cinematic = datacinematic
        if dataaddress:
            dataUpdate.address = dataaddress
        if datagmaps:
            dataUpdate.gmaps = datagmaps
        if dataig:
            dataUpdate.ig = dataig
        if pic_thumbnail:
            dataUpdate.thumbnail_img = pic_thumbnail.read()
            dataUpdate.thumbnail_name = filename_thumbnail
            dataUpdate.thumbnail_mimetype = mimetype_thumbnail
        if pic_logo:    
            dataUpdate.logo_img = pic_logo.read()
            dataUpdate.logo_name = filename_logo
            dataUpdate.logo_mimetype = mimetype_logo
        if pic_cover:
            dataUpdate.cover_img = pic_cover.read()
            dataUpdate.cover_name = filename_cover
            dataUpdate.cover_mimetype = mimetype_cover
            
            #relation_db
        if datacategory:
            dataUpdate.category360_id =  id_category
        if dataclient:
            dataUpdate.client360_id = id_client
            
        db.session.commit()
        return make_response(jsonify({"msg" : "updated"}),200)
        # return jsonify({"msg","There is empty data"},200)
    
    @token_api 
    # admin
    def delete(self,id):
        own = Project360.query.filter(Project360.id == id).first()
        db.session.delete(own)
        db.session.commit()
        return jsonify({"msg":"Deleted"})

class ProjectRelation(Resource):
    def get(self):
        dataQuery = Project360.query.all()
        # print(dataQuery)
        output = []
        # print(dataQuery[0].client360.name)
        for i in range(len(dataQuery)):
            val = {
                "id" : dataQuery[i].id,
                "data" : {
                "name" : dataQuery[i].name,
                "date" : dataQuery[i].datadate,
                "domain" : dataQuery[i].domain,
                "rating" : dataQuery[i].rating,
                "testimoni" : dataQuery[i].testimoni,
                "review" : dataQuery[i].review,
                "cinematic" : dataQuery[i].cinematic,
                "instagram" : dataQuery[i].ig,
                "link_gmaps" : dataQuery[i].gmaps,
                "address" : dataQuery[i].address,
                "thumbnail" : "http://192.168.1.253:2024/360/project-thumbnail/"+ str(dataQuery[i].id),
                "logo" : "http://192.168.1.253:2024/360/project-logo/"+ str(dataQuery[i].id),
                "cover" : "http://192.168.1.253:2024/360/project-cover/"+ str(dataQuery[i].id),
                "category" :  {
                    "name" : dataQuery[i].category360.name
                },
                "client" : {
                    "name" : dataQuery[i].client360.name,
                    "email" : dataQuery[i].client360.email,
                    "phone" : dataQuery[i].client360.phone,
                    "position" : dataQuery[i].client360.position,
                    "company" : dataQuery[i].client360.company,
                    "logo" : "http://192.168.1.253:2024/360/clientimg/"+ str(dataQuery[i].client360.id)
                }
            } 
            }  
            output.append(val)
        return make_response(jsonify(output), 200)

class ProjectRelationid(Resource):
    def get(self,id):
        dataQuery = Project360.query.filter(Project360.id == id).first()
        # print(dataQuery)
        output = []
        # print(dataQuery[0].client360.name)
        val = {
            "id" : dataQuery.id,
            "data" : {
            "name" : dataQuery.name,
            "date" : dataQuery.datadate,
            "domain" : dataQuery.domain,
            "rating" : dataQuery.rating,
            "testimoni" : dataQuery.testimoni,
            "review" : dataQuery.review,
            "cinematic" : dataQuery.cinematic,
            "instagram" : dataQuery.ig,
            "link_gmaps" : dataQuery.gmaps,
            "address" : dataQuery.address,
            "thumbnail" : "http://192.168.1.253:2024/360/project-thumbnail/"+ str(dataQuery.id),
            "logo" : "http://192.168.1.253:2024/360/project-logo/"+ str(dataQuery.id),
            "cover" : "http://192.168.1.253:2024/360/project-cover/"+ str(dataQuery.id),
            "category" :  {
                "name" : dataQuery.category360.name
            },
            "client" : {
                "name" : dataQuery.client360.name,
                "email" : dataQuery.client360.email,
                "phone" : dataQuery.client360.phone,
                "position" : dataQuery.client360.position,
                "company" : dataQuery.client360.company,
                "logo" : "http://192.168.1.253:2024/360/clientimg/"+ str(dataQuery.client360.id)
            }
        } 
        }  
        output.append(val)
        return make_response(jsonify(output), 200)

class ClientRelation(Resource):
    def get(self):
        dataQuery = Client360.query.all()
        # print(dataQuery)
        output, datcl = [],[]
        # print(dataQuery[0].project360[1].name)
        for i in range(len(dataQuery)):
            projectdata = []
            for x in range(len(dataQuery[i].project360)):
                print(dataQuery[i].project360, " " , dataQuery[i].name, " " , dataQuery[i].project360[x].name)
                projectval = {
                # "id" : dataQuery[i].id,
                "name" : dataQuery[i].project360[x].name,
                "date" : dataQuery[i].project360[x].datadate,
                "domain" : dataQuery[i].project360[x].domain,
                "rating" : dataQuery[i].project360[x].rating,
                "testimoni" : dataQuery[i].project360[x].testimoni,
                "review" : dataQuery[i].project360[x].review,
                "cinematic" : dataQuery[i].project360[x].cinematic,
                "instagram" : dataQuery[i].project360[x].ig,
                "link_gmaps" : dataQuery[i].project360[x].gmaps,
                "address" : dataQuery[i].project360[x].address,
                "thumbnail" : "http://192.168.1.253:2024/360/project-thumbnail/"+ str(dataQuery[i].project360[x].id),
                "logo" : "http://192.168.1.253:2024/360/project-logo/"+ str(dataQuery[i].project360[x].id),
                "cover" : "http://192.168.1.253:2024/360/project-cover/"+ str(dataQuery[i].project360[x].id),
                "category" :  {
                    "name" : dataQuery[i].project360[x].category360.name
                } 
                
                }   
                projectdata.append(projectval)
            val = {
                "id" : dataQuery[i].id,
                "data" : {
                    "name" : dataQuery[i].name,
                    "email" : dataQuery[i].email,
                    "phone" : dataQuery[i].phone,
                    "position" : dataQuery[i].position,
                    "company" : dataQuery[i].company,
                    "logo" : "http://192.168.1.253:2024/360/clientimg/"+ str(dataQuery[i].id),
                    "project" : projectdata
            }       
            }  
            output.append(val)
        return make_response(jsonify(output), 200)
    
class ClientRelationid(Resource):
    def get(self,id):
        dataQuery = Client360.query.filter(Client360.id == id).first()
        # print(dataQuery)
        output = []
        # print(dataQuery[0].project360[1].name)
        
        projectdata = []
        for x in range(len(dataQuery.project360)):
            print(dataQuery.project360, " " , dataQuery.name, " " , dataQuery.project360[x].name)
            projectval = {
            # "id" : dataQuery.id,
            "name" : dataQuery.project360[x].name,
            "date" : dataQuery.project360[x].datadate,
            "domain" : dataQuery.project360[x].domain,
            "rating" : dataQuery.project360[x].rating,
            "testimoni" : dataQuery.project360[x].testimoni,
            "review" : dataQuery.project360[x].review,
            "cinematic" : dataQuery.project360[x].cinematic,
            "instagram" : dataQuery.project360[x].ig,
            "link_gmaps" : dataQuery.project360[x].gmaps,
            "address" : dataQuery.project360[x].address,
            "thumbnail" : "http://192.168.1.253:2024/360/project-thumbnail/"+ str(dataQuery.project360[x].id),
            "logo" : "http://192.168.1.253:2024/360/project-logo/"+ str(dataQuery.project360[x].id),
            "cover" : "http://192.168.1.253:2024/360/project-cover/"+ str(dataQuery.project360[x].id),
            "category" :  {
                "name" : dataQuery.project360[x].category360.name
            } 
            
            }   
            projectdata.append(projectval)
        val = {
            "id" : dataQuery.id,
            "data" : {
                "name" : dataQuery.name,
                "email" : dataQuery.email,
                "phone" : dataQuery.phone,
                "position" : dataQuery.position,
                "company" : dataQuery.company,
                "logo" : "http://192.168.1.253:2024/360/clientimg/"+ str(dataQuery.id),
                "project" : projectdata
        }       
        }  
        output.append(val)
        return make_response(jsonify(output), 200)

class CategoryRelation(Resource):
    def get(self):
        dataQuery = Category360.query.all()
        # print(dataQuery)
        output = []
        # print(dataQuery[0].project360[1].name)
        for i in range(len(dataQuery)):
            projectdata = []
            for x in range(len(dataQuery[i].project360)):
                # print(dataQuery[i].project360, " " , dataQuery[i].name, " " , dataQuery[i].project360[x].name)
                projectval = {
                # "id" : dataQuery[i].id,
                "name" : dataQuery[i].project360[x].name,
                "date" : dataQuery[i].project360[x].datadate,
                "domain" : dataQuery[i].project360[x].domain,
                "rating" : dataQuery[i].project360[x].rating,
                "testimoni" : dataQuery[i].project360[x].testimoni,
                "review" : dataQuery[i].project360[x].review,
                "cinematic" : dataQuery[i].project360[x].cinematic,
                "instagram" : dataQuery[i].project360[x].ig,
                "link_gmaps" : dataQuery[i].project360[x].gmaps,
                "address" : dataQuery[i].project360[x].address,
                "thumbnail" : "http://192.168.1.253:2024/360/project-thumbnail/"+ str(dataQuery[i].project360[x].id),
                "logo" : "https://api.indo360.id/project-logo/"+ str(dataQuery[i].project360[x].id),
                "cover" : "http://192.168.1.253:2024/360/project-cover/"+ str(dataQuery[i].project360[x].id),
                "client" : {
                    "name" : dataQuery[i].project360[x].client360.name,
                    "email" : dataQuery[i].project360[x].client360.email,
                    "phone" : dataQuery[i].project360[x].client360.phone,
                    "position" : dataQuery[i].project360[x].client360.position,
                    "company" : dataQuery[i].project360[x].client360.company,
                    "logo" : "http://192.168.1.253:2024/360/clientimg/"+ str(dataQuery[i].project360[x].client360.id)
                }
                
                }   
                projectdata.append(projectval)
            val = {
                "id" : dataQuery[i].id,
                "data" : {
                    "name" : dataQuery[i].name,
                    "project" : projectdata
            }       
            }  
            output.append(val)
        return make_response(jsonify(output), 200)    
    
class CategoryRelationid(Resource):
    def get(self, id):
        dataQuery = Category360.query.filter(Category360.id == id).first()
        # print(dataQuery)
        output = []
        # print(dataQuery[0].project360[1].name)
        
        projectdata = []
        for x in range(len(dataQuery.project360)):
            # print(dataQuery.project360, " " , dataQuery.name, " " , dataQuery.project360[x].name)
            projectval = {
            # "id" : dataQuery.id,
            "name" : dataQuery.project360[x].name,
            "date" : dataQuery.project360[x].datadate,
            "domain" : dataQuery.project360[x].domain,
            "rating" : dataQuery.project360[x].rating,
            "testimoni" : dataQuery.project360[x].testimoni,
            "review" : dataQuery.project360[x].review,
            "cinematic" : dataQuery.project360[x].cinematic,
            "instagram" : dataQuery.project360[x].ig,
            "link_gmaps" : dataQuery.project360[x].gmaps,
            "address" : dataQuery.project360[x].address,
            "thumbnail" : "http://192.168.1.253:2024/360/project-thumbnail/"+ str(dataQuery.project360[x].id),
            "logo" : "http://192.168.1.253:2024/360/project-logo/"+ str(dataQuery.project360[x].id),
            "cover" : "http://192.168.1.253:2024/360/project-cover/"+ str(dataQuery.project360[x].id),
            "client" : {
                "name" : dataQuery.project360[x].client360.name,
                "email" : dataQuery.project360[x].client360.email,
                "phone" : dataQuery.project360[x].client360.phone,
                "position" : dataQuery.project360[x].client360.position,
                "company" : dataQuery.project360[x].client360.company,
                "logo" : "http://192.168.1.253:2024/360/clientimg/"+ str(dataQuery.project360[x].client360.id)
            }
            
            }   
            projectdata.append(projectval)
        val = {
            "id" : dataQuery.id,
            "data" : {
                "name" : dataQuery.name,
                "project" : projectdata
        }       
        }  
        output.append(val)
        return make_response(jsonify(output), 200)  
    
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
                "logo" : "http://192.168.1.253:2024/360/linktree-logo/"+ str(data.id),
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
    
class LinkIndoid(Resource):
    def get(self,id):
        data = Link360.query.filter(Link360.id == id).first()
        output = [{
            "id" : data.id,
            "data" : {
                "name" : data.name,
                "bio" : data.bio,
                "logo" : "http://192.168.1.253:2024/360/linktree-logo/"+ str(data.id),
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
                
        return jsonify({"msg":"Delet ed"}) 
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
                "logo" : "http://192.168.1.253:2024/360/linktree-logo/"+ str(dataQuery.id),
                "domain" : dataQuery.domain,
                "list" : listar
            }
        }
        output.append(val)
        return make_response(jsonify(output), 200) 

@app.route('/') 
def index():
    
    return 'Welcome To the Club'

api.add_resource(Forgot_Password, "/360/forgot-password", methods=['POST'])
api.add_resource(Reset_Password, "/360/reset-password/<tokenreset>", methods=['POST'])

api.add_resource(Userall, "/360/register", methods=["POST","GET","DTE"])
api.add_resource(Userid,"/360/register/<id>", methods=["GET","PUT","DELETE"])


api.add_resource(LinkRelationid, "/360/profile/all/<id>", methods=["GET"])

api.add_resource(GetImgLink,"/360/linktree-logo/<id>", methods=["GET"])

api.add_resource(LoginUser, "/360/login", methods=["POST"])
api.add_resource(LoginAdmin, "/360/login/admin", methods=["POST"])

api.add_resource(LinkIndoall, "/360/profile", methods=["POST", "GET", "DELETE"])
api.add_resource(LinkIndoid, "/360/profile/<id>", methods=["GET", "PUT", "DELETE"])

api.add_resource(InputLinkall, "/360/list", methods=["POST", "GET", "DELETE"])
api.add_resource(InputLinkid, "/360/list/<id>", methods=["GET", "PUT", "DELETE"])

api.add_resource(Priceall, "/360/price", methods=["POST","GET","DELETE"])
api.add_resource(Priceid,"/360/price/<id>", methods=["GET", "PUT",  "DELETE"])

api.add_resource(Categoryall, "/360/category", methods=["POST","GET","DELETE"])
api.add_resource(Categoryid,"/360/category/<id>", methods=["GET", "PUT",  "DELETE"])
api.add_resource(CategoryRelation, "/360/category/all", methods=["GET"])
api.add_resource(CategoryRelationid, "/360/category/all/<id>", methods=["GET"])


api.add_resource(Clientall, "/360/client", methods=["POST","GET","DELETE"])
api.add_resource(Clientid,"/360/client/<id>", methods=["GET", "PUT",  "DELETE"])
api.add_resource(ClientRelation, "/360/client/all", methods=["GET"])
api.add_resource(ClientRelationid, "/360/client/all/<id>", methods=["GET"])

api.add_resource(Projectall, "/360/project", methods=["POST","GET","DELETE"])
api.add_resource(Projectid,"/360/project/<id>", methods=["GET", "PUT",  "DELETE"])
api.add_resource(ProjectRelation, "/360/project/all", methods=["GET"])
api.add_resource(ProjectRelationid, "/360/project/all/<id>", methods=["GET"])

api.add_resource(GetImgClient,"/360/clientimg/<id>", methods=["GET"])
api.add_resource(GetImgprothumbnail,"/360/project-thumbnail/<id>", methods=["GET"])
api.add_resource(GetImgprologo,"/360/project-logo/<id>", methods=["GET"])
api.add_resource(GetImgprocover,"/360/project-cover/<id>", methods=["GET"])

api.add_resource(UpMsg, "/360/contact", methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True,port=2024, host="0.0.0.0")