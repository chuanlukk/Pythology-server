# 自定义flask命令
# 当我们安装Flask后，会自动添加一个flask命令脚本，
# 我们可以通过flask命令执行内置命令、拓展提供的命令或是我们自己定义的命令
import click
from flask import current_app
from .extensions import db
from .models import User

@current_app.cli.command()
@click.option('--count', default=20, help='Number of greetings.')
def forge(count):
    """Generate fake data."""
    from faker import Faker
    fake = Faker('zh_CN')
    for i in range(count):
        click.echo('generating %d message' % i)
        click.echo(fake.name())


@current_app.cli.command()
def initdb():
    """Initialize the database."""
    click.echo('Initializing the database...')
    db.create_all()
    click.echo('Done.')