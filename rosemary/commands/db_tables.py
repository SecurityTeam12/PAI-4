import os
import subprocess

import click
from dotenv import load_dotenv


@click.command('db:tables', help="Shows every table within the database.")
def db_tables():
    load_dotenv()
    
    mariadb_hostname = os.getenv('MARIADB_HOSTNAME')
    mariadb_user = os.getenv('MARIADB_USER')
    mariadb_password = os.getenv('MARIADB_PASSWORD')
    mariadb_database = os.getenv('MARIADB_DATABASE')
    
    sql_command = "SHOW tables;"
        
    # Execute the command securely
    try:
        subprocess.run([
            'mysql',
            '-h', mariadb_hostname,
            '-u', mariadb_user,
            f'-p{mariadb_password}',
            mariadb_database,
            '-e', sql_command
        ], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error opening MariaDB console: {e}", fg='red'))

