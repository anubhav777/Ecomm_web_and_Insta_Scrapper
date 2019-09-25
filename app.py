from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)
db=SQLAlchemy(app)
ma=Marshmallow(app)
app.config.from_object('config.Development')
from routes import *

if __name__ == "__main__":
    app.run(debug=True)