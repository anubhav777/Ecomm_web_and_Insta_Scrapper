import os
class Production(object):
    DEBUG=False
    basedir=os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir,'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATION=False
    SECRET_KEY='secret'

class Deploy(Production):
    pass

class Development(Production):
    DEBUG=True