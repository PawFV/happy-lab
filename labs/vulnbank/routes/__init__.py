from flask import Blueprint

from . import auth, main, files, admin


def register_routes(app):
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(files.bp)
    app.register_blueprint(admin.bp)
