
import os
import pytest
from flask.cli import FlaskGroup
from flask_migrate import Migrate

from app import flask_app
from app.plugins import db
# flake8: noqa
from app.repositories.models import Ingredient, Order, OrderDetail, Size
from seeder import seeder


manager = FlaskGroup(flask_app)

migrate = Migrate()
migrate.init_app(flask_app, db)


@manager.command('test', with_appcontext=False)
def test():
    return pytest.main(['-v', './app/test'])

@manager.command('cover', with_appcontext=False)
def cover():
    return pytest.main(['--cov-config=.coveragerc', '--cov=app', 'app/test'])

@manager.command('linters')
def run_linters():
    return os.system("flake8 app/")

@manager.command('seed', with_appcontext=True)
def seed():
    return seeder.execute(10, 100)


if __name__ == '__main__':
    manager()
