from app import app
from flask import jsonify,request
from werkzeug.security import check_password_hash,generate_password_hash
import jwt
import datetime
from models import *
from files import *
secret=app.config['SECRET_KEY']
print(secret)
@app.route('/register',methods=['POST'])
def register():
    username=request.json['username']
    email=request.json['email']
    address=request.json['address']
    phone=request.json['phone']
    new_password=request.json['password']
    password=generate_password_hash(new_password,method='sha256')
    usertype='staff'
    validator=Signup.query.filter_by(email=email).first()

    if validator:
        return jsonify({'status':"email already registered"})
    else:
        result=Signup(username,email,address,phone,password,UserWarning)
        print(result)
        db.session.add(result)
        db.session.commit()
        return('sucessfully added')

@app.route('/getuser/<id>',methods=['GET'])
def getuser(id):
    result=Signup.query.get(id)

    return signup_schema.jsonify(result)

@app.route('/getalluser',methods=['GET'])
def getalluser():
    result=Signup.query.all()
    new_result=signups_schema.dump(result)

    return jsonify(new_result)
@app.route('/edituser/<id>',methods=["PUT"])
def edituser(id):
    username=request.json['username']
    address=request.json['address']
    phone=request.json['phone']

    new_user=Signup.query.filter_by(id=id).first()
    new_user.username=username
    new_user.address=address
    new_user.phone=phone

    db.session.commit()
    return ({'status':'sucessfully updated'})
    
@app.route('/deleteuser/<id>',methods=['DELETE'])
def deleteuser(id):
    new_user=Signup.query.get(id)
    db.session.delete(new_user)
    db.session.commit()
@app.route('/addquery',methods=['POST'])
def addquery():
    queryname=request.json['queryname']
    userid=request.json['userid']
    result=Querytable(queryname,userid)

    db.session.add(result)
    db.session.commit()
    return ('sucessfully added')

@app.route('/getquery/<id>',methods=['GET'])
@admin
def getquery(stats,id):
    if stats:
        result=Querytable.query.get(id)
        return query_schema.jsonify(result)

@app.route('/getallquery',methods=['GET'])
@admin
def getallquery(stats):
    if stats:
        result=Querytable.query.all()
        new_result=querys_schema.dump(result)

    return jsonify(new_result)
@app.route('/editquery/<id>',methods=['PUT'])
@admin
def editquery(stats,id):
    if stats:
        new_query=Querytable.query.filter_by(id=id).first()
        queryname=request.json['queryname']
        new_query.queryname=queryname
        db.session.commit()

@app.route('/deletequery/<id>',methods=['DELETE'])
@admin
def deletequery(stats,id):
    if stats:
        result=Querytable.query.get(id)

        db.session.delete(result)
        db.session.commit()

@app.route('/addcategory',methods=['POST'])
def addcategory():
    categoryname=request.json['categoryname']
    userid=request.json['userid']
    result=Category(categoryname,userid)

    db.session.add(result)
    db.session.commit()
    return ('sucessfully added')

@app.route('/getcategory/<id>',methods=['GET'])
@admin
def getcategory(stats,id):
    if stats:
        result=Category.query.get(id)
        return categorys_chema.jsonify(result)
@app.route('/getallcategory',methods=['GET'])
@admin
def getallcategory(stats):
    if stats:
        result=Category.query.all()
        new_result=categorys_schema.dump(result)
        return jsonify(new_result)

@app.route('/editcategory/<id>',methods=['PUT'])
@admin
def editcategory(stats,id):
    if stats:
        new_cat=Category.quuery.get(id)
        categoryname=request.json['categoryname']

        new_cat.categoryname=categoryname

        db.session.commit()
        return ({'status':'sucessfully edited'})

@app.route('/deletecategory/<id>',methods=['DELETE'])
@admin
def deletecategory(stats,id):
    if stats:
        result=Category.quuery.get(id)
        db.session.delete(result)
        db.session.commit()


@app.route('/buyproduct',methods=['POST'])
def buyproduct():
    productname=request.json['productname']
    vendor=request.json['vendor']
    userid=request.json['userid']

    result=Buyout(productname,vendor,userid)
    db.session.add(result)
    db.session.commit()
    return 'added'

@app.route('/getproduct/<id>',methods=['GET'])
def getproduct(id):
    result=Buyout.query.filter_by(id=id).first()
    print(result.userid)
    new_result=buyout_schema.jsonify(result)
    print(new_result)
    return buyout_schema.jsonify(result)

@app.route('/getallproduct',methods=['GET'])
@decorator
def getallproduct(userid):
    user=Signup.query.filter_by(id=userid).first()
    if user.usertype == "admin":

        result=Buyout.query.all()
        new_result=buyouts_schema.dump(result)
        return jsonify(new_result)
    else:
        result=Buyout.query.filter_by(userid=user.id).all()
        new_result=buyouts_schema.dump(result)
        return jsonify(new_result)

@app.route('/editproduct/<id>',methods=['PUT'])
@admin
def editproduct(status,id):
    if status:
        result=Buyout.query.filter_by(id=id).first()
        productname=request.json['productname']
        vendor=request.json['vendor']

        result.productname=productname
        result.vendor=vendor

        db.session.commit()
        return ({'status':'sucessfullty updated'})

@app.route('/deleteproduct/<id>',methods=['DELETE'])
@admin
def deleteproduct(status,id):
    if status:
        result=Buyout.query.get(id)
        db.session.delete(result)
        db.session.commit()

        return ({'status':'sucessfullty deleted'})

@app.route('/addtry',methods=['POST'])
def addtry():
    tryname=request.json['tryname']
    

    result=Try(tryname)
    db.session.add(result)
    db.session.commit()
    return try_schema.jsonify(result)

@app.route('/gettry/<id>',methods=['GET'])
@decorator
def gettry(userid,id):
    res=Try.query.get(id)
    print(userid)
    # print(try_schema.jsonify(res))
    new_res=try_schema.dump(res)
    return try_schema.dump(res)

@app.route('/login')
def login():
    auth_data=request.authorization
    print(auth_data)
    if not auth_data:
        return ({'status':'Please provide authentic email and password'})

    validator=Signup.query.filter_by(email=auth_data.username).first()

    if not validator:
        return({'status':'Your email is not registered'})
    
    if not check_password_hash(validator.password,auth_data.password):
        return ({'status':'Your password does not match'})
    
    else:
        new_token=jwt.encode({'userid':validator.id,'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=4)},secret)
       
        # print(new_token.decode('UTF-8'))
        return({'token':new_token.decode('UTF-8')})
    
    return 'hi'