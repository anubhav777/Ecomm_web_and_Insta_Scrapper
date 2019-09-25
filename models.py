from app import db,ma
from datetime import date
class Signup(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    address=db.Column(db.String(100),nullable=False)
    phone=db.Column(db.String(100),nullable=False)
    date=db.Column(db.Date,default=date.today())
    password=db.Column(db.String(100),nullable=False)
    usertype=db.Column(db.String(100),nullable=False)
    querytable=db.relationship('Querytable',backref='userquery',lazy='dynamic')
    category=db.relationship('Category',backref='usercat',lazy='dynamic')
    buyout=db.relationship('Buyout',backref='userbuyout',lazy='dynamic')


    def __init__(self,username,email,address,phone,password,usertype):
        self.username=username
        self.email=email
        self.address=address
        self.phone=phone
        self.password=password
        self.usertype=usertype


class Category(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    categoryname=db.Column(db.String(100),nullable=False)
    date=db.Column(db.Date,default=date.today())
    userid=db.Column(db.Integer,db.ForeignKey('signup.id'))

    def __init__(self,categoryname,userid):
        self.categoryname=categoryname
        self.userid=userid


class Buyout(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    productname=db.Column(db.String(100),nullable=False)
    vendor=db.Column(db.String(100),nullable=False)
    date=db.Column(db.Date,default=date.today())
    userid=db.Column(db.Integer,db.ForeignKey('signup.id'))

    def __init__(self,productname,vendor,userid):
        self.productname=productname
        self.vendor=vendor
        self.userid=userid

class Try(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    tryname=db.Column(db.String(100),nullable=False)

    def __init__(self,tryname):
        self.tryname=tryname


class Querytable(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    queryname=db.Column(db.String(100),nullable=False)
    date=db.Column(db.Date(),default=date.today())
    userid=db.Column(db.Integer,db.ForeignKey('signup.id'))

    def __init__(self,queryname,userid):
        self.queryname=queryname
        self.userid=userid



class QuerySchema(ma.Schema):
    class Meta:
        fields=('id','queryname','date','userid')

class CategorySchema(ma.Schema):
    class Meta:
        fields=('id','categoryname','date','userid')

class BuyoutSchema(ma.Schema):
    class Meta:
        fields=('id','productname','vendor','date','userid')

class TrySchema(ma.Schema):
    class Meta:
        fields=('id','tryname')

class SignupSchema(ma.Schema):
    class Meta:
        fields=('id','username','email','address','password','date','phone','usertype')

signup_schema=SignupSchema()
signups_schema=SignupSchema(many=True)

query_schema=QuerySchema()
querys_schema=QuerySchema(many=True)

categorys_chema=CategorySchema()
categorys_schema=CategorySchema(many=True)

buyout_schema=BuyoutSchema()
buyouts_schema=BuyoutSchema(many=True)

try_schema=TrySchema()
trys_schema=TrySchema(many=True)