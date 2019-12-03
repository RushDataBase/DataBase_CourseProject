
class Config:
    FLASK_DEBUG = True

    SECRET_KEY = 'ASFGDSGSDGFH'
    CKEDITOR_SERVE_LOCAL = True

    DB_USERNAME = 'yuxin'
    DB_PASSWORD = 'maoyuxin123/'
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    DB_NAME = 'lolbbs'

    DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD,
                                                                    DB_HOST, DB_PORT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False