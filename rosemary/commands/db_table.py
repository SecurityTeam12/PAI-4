import os
import re
import subprocess

import click
from dotenv import load_dotenv


@click.command('db:table', help="Select the first 5 rows from the table given as a parameter.")
@click.argument('table')
def db_table(table):
    load_dotenv()

    if not is_valid_table_name(table):
        click.echo(click.style("Invalid table name.", fg='red'))
        return

    mariadb_hostname = os.getenv('MARIADB_HOSTNAME')
    mariadb_user = os.getenv('MARIADB_USER')
    mariadb_password = os.getenv('MARIADB_PASSWORD')
    mariadb_database = os.getenv('MARIADB_DATABASE')

    sql_command = f"SELECT * FROM {table} LIMIT 5;"
    
    try:
        subprocess.run([
    'mysql',
    f'-h{mariadb_hostname}',
    f'-u{mariadb_user}',
    f'-p{mariadb_password}',
    mariadb_database,
    '-e',
    sql_command
], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error opening MariaDB console: {e}", fg='red'))


def is_valid_table_name(table_name):
    return re.match(r'^[a-zA-Z0-9_]+$', table_name) is not None
