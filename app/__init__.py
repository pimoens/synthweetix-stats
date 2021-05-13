from flask import Flask


def init_app(app_):
    import app.routes

    return app_


app = Flask(__name__)
init_app(app)

