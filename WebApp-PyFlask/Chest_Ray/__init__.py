import os
from flask import Flask, render_template, request


def create_app(test_config=None):

    """Create and configure the app."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in.
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #Web Pages go below.


    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/check_login", methods = ("POST",))
    def check_login():

        try:
            e = e

        except:
            return "404, can not reach database :C"
        
        return request.form

    return app

app = create_app()