from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from app.constants.vote_type import VoteType
from app.helpers.formatters import (
    format_date,
    format_datetime,
    format_number,
    format_party,
    format_support,
    format_title,
    format_vote_type,
    na_if_none,
)
from settings import settings

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Use the same database URL from settings
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url.replace(
        "+aiosqlite",
        "",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Register template filters and globals
    app.jinja_env.filters["na"] = na_if_none
    app.jinja_env.filters["number"] = format_number
    app.jinja_env.filters["datetime"] = format_datetime
    app.jinja_env.filters["date"] = format_date
    app.jinja_env.filters["title"] = format_title
    app.jinja_env.filters["party"] = format_party
    app.jinja_env.filters["support"] = format_support
    app.jinja_env.filters["vote_type"] = format_vote_type
    app.jinja_env.filters["vote_type_label"] = lambda value: VoteType.label(value)
    app.jinja_env.globals.update(
        na_if_none=na_if_none,
        format_number=format_number,
        format_datetime=format_datetime,
        format_date=format_date,
        format_title=format_title,
        format_party=format_party,
        format_support=format_support,
        format_vote_type=format_vote_type,
        vote_type_label=lambda value: VoteType.label(value),
    )

    # Global navigation context processor
    from app.helpers.navigation import inject_navigation

    app.context_processor(inject_navigation)

    # Dynamically register all blueprints in app.routes
    import importlib
    import pkgutil

    from . import routes

    for _, module_name, _ in pkgutil.iter_modules(routes.__path__):
        module = importlib.import_module(f"app.routes.{module_name}")
        if hasattr(module, "bp"):
            app.register_blueprint(module.bp)

    # Static file serving
    @app.route("/static/<path:filename>")
    def static_files(filename):
        return app.send_static_file(filename)

    # Register root route
    @app.route("/")
    def index():
        return redirect(url_for("legislators.list_legislators"))

    return app
