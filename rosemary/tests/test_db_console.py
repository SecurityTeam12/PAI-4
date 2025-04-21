# import os
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from rosemary.commands.db_console import db_console


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
def test_db_console(mock_run, mock_getenv, mock_env_vars):
    mock_getenv.side_effect = lambda key: mock_env_vars.get(key)
    mock_run.return_value = None

    runner = CliRunner()
    result = runner.invoke(db_console)

    assert result.exit_code == 0
    mock_run.assert_called_once_with(
        'mysql -hlocalhost -uuvlhubdb_user -puvlhubdb_password uvlhubdb_test',
        check=True,
    )
