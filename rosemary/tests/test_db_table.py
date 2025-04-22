from unittest.mock import patch

import pytest
from click.testing import CliRunner

from rosemary.commands.db_table import db_table


@pytest.fixture
def mock_env_vars():
    return {
        "MARIADB_HOSTNAME": "localhost",
        "MARIADB_USER": "uvlhubdb_user",
        "MARIADB_PASSWORD": "uvlhubdb_password",
        "MARIADB_DATABASE": "uvlhubdb_test",
    }


@patch("os.getenv")
@patch("subprocess.run")
def test_db_table_valid_table(mock_run, mock_getenv, mock_env_vars):

    mock_getenv.side_effect = lambda key: mock_env_vars.get(key)
    mock_run.return_value = None

    runner = CliRunner()
    result = runner.invoke(db_table, ["user"])

    assert result.exit_code == 0
    mock_run.assert_called_once_with(
        ['mysql', '-hlocalhost', '-uuvlhubdb_user', '-puvlhubdb_password', 'uvlhubdb_test', '-e', 'SELECT * FROM user LIMIT 5;'],
        check=True,
    )


@patch("os.getenv")
def test_db_table_invalid_name(mock_getenv, mock_env_vars):
    mock_getenv.side_effect = lambda key: mock_env_vars.get(key)

    runner = CliRunner()
    result = runner.invoke(db_table, ["invalid-table!"])

    assert result.exit_code == 0
    assert "Invalid table name." in result.output


@patch("os.getenv")
def test_db_table_valid_name_invalid_table(mock_getenv, mock_env_vars):
    mock_getenv.side_effect = lambda key: mock_env_vars.get(key)

    runner = CliRunner()
    result = runner.invoke(db_table, ["unexisted_table"])

    assert result.exit_code == 0
    assert "Error opening MariaDB console" in result.output
