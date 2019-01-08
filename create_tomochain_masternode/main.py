import re
import os

import click
import inquirer

from create_tomochain_masternode import __version__

WORKING_PATH = os.getcwd()
QUESTIONS = [
    inquirer.Text(
        'name',
        message='What\'s your masternode name? (a to z, 0 to 9 and -)',
        validate=lambda _, x: re.match(r'^[a-z0-9][a-z0-9\-]+[a-z0-9]$', x),
    ),
    inquirer.Password(
        'private_key',
        message="What's your coinbase private key? (64char hex string)",
        validate=lambda _, x: len(x) == 64,
    ),
    inquirer.Text(
        'data_path',
        message=("Where should the data be located? (docker volume name or "
                 "absolute path)"),
    ),
    inquirer.Confirm(
        'expose_rpc',
        message="Do you want to expose the RPC endpoint? (advanced use)",
    ),
    inquirer.Confirm(
        'expose_ws',
        message="Do you want to expose the WebSocket endpoint? (advanced use)",
    ),
]


@click.command(help='Set up a TomoChain masternode by running one command.')
@click.argument('project')
@click.option('--testnet', is_flag=True, help='Use testnet settings')
@click.version_option(version=__version__)
def entrypoint(project, testnet) -> None:
    """Command line interface entrypoint"""
    answers = inquirer.prompt(QUESTIONS)
    print(answers)
