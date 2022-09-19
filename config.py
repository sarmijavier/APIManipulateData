
class Config(object):
    database = 'db_thesis'
    server = 'localhost:3306'
    username = 'root'
    password = ''
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://"+username+":"+password+"@"+server+"/"+database
    SQLALCHEMY_TRACK_MODIFICATIONS = False