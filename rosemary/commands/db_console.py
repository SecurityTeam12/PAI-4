import click
import subprocess
from dotenv import load_dotenv
import os


@click.command('db:console', help="Opens a MariaDB console with credentials from .env.")
def db_console():
    load_dotenv()

    mariadb_hostname = os.getenv('MARIADB_HOSTNAME')
    mariadb_user = os.getenv('MARIADB_USER')
    mariadb_password = os.getenv('MARIADB_PASSWORD')
    mariadb_database = os.getenv('MARIADB_DATABASE')

    # Execute the command securely
    try:
        subprocess.run([
            'mysql',
            '-h', mariadb_hostname,
            '-u', mariadb_user,
            f'-p{mariadb_password}',
            mariadb_database
        ], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error opening MariaDB console: {e}", fg='red'))
