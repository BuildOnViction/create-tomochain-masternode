import yaml

import pytest

from create_tomochain_masternode import __version__
from create_tomochain_masternode import main


@pytest.fixture
def runner():
    from click.testing import CliRunner
    runner = CliRunner()
    return runner


def test_version():
    assert __version__ == '1.2.2'


def test_produced_yml(runner):
    input = (
        "123456123456\n"
        "123456123456\n"
        "\n"
        "/tmp\n"
        "\n"
        "\n"
        "\n"
    )
    with runner.isolated_filesystem():
        runner.invoke(main.entrypoint, ['test-node'], input=input)
        with open('test-node/docker-compose.yml') as file:
            assert yaml.load(file)
