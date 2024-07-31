from flask import Flask
from flask.cli import with_appcontext
import click
from backend.models import db

@click.command(name='init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')

def register_commands(app: Flask):
    app.cli.add_command(init_db_command)
