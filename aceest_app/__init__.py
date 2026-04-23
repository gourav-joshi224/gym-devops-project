from flask import Flask

from .db import close_db, init_app, init_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE="aceest_fitness.db",
    )

    if test_config is not None:
        app.config.update(test_config)

    init_app(app)

    from .routes import bp

    app.register_blueprint(bp)

    with app.app_context():
        init_db()

    app.teardown_appcontext(close_db)
    return app
