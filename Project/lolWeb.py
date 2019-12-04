from flask import Flask
import config
from flaskr import bp
from ext import db, login, ckeditor


def create_app():
    app = Flask('__name__')
    app.config.from_object(config)

    app.register_blueprint(bp)

    ckeditor.init_app(app)
    db.init_app(app)
    login.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
