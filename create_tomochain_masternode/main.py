from typing import Dict
import os
import sys

from jinja2 import Template
import click

from create_tomochain_masternode import __version__, envs,  templates


@click.command(help='Set up a TomoChain masternode by running one command.')
@click.argument('masternode_name', type=click.Path(
    file_okay=False,
    resolve_path=True
))
@click.option('--testnet', is_flag=True, help='Testnet instead of mainnet.')
@click.version_option(version=__version__)
def entrypoint(masternode_name: click.Path, testnet: bool) -> None:
    """Command line interface entrypoint"""
    env = envs.testnet if testnet else envs.mainnet
    masternode_path = os.path.join(os.getcwd(), masternode_name)
    display(
        'Creating a new masternode in '
        f'{click.style(masternode_path, fg="green")}.',
        spacing=1
    )
    answers = ask()
    compose_template = Template(templates.compose)
    compose_content = compose_template.render(**answers, **env)
    env_template = Template(templates.env)
    env_content = env_template.render(**answers, **env)
    if not os.path.exists(masternode_path):
        os.makedirs(masternode_path)
    with open(f'{masternode_path}/docker-compose.yml', 'w') as compose_file:
        print(compose_content, file=compose_file)
    with open(f'{masternode_path}/.env', 'w') as env_file:
        print(env_content, file=env_file)


def display(message: str, spacing: int = 0) -> None:
    newlines = '\n' * spacing
    click.echo(f'{newlines}{message}{newlines}')


def ask() -> Dict[str, str]:
    """Prompt users for parameters"""
    answers = {}
    bullet = f'{click.style("?", fg="cyan")}'
    answers['name'] = click.prompt(f'{bullet} Name')
    answers['private_key'] = click.prompt(
        f'{bullet} Private key',
        hide_input=True
    )
    answers['address'] = click.prompt(
        f'{bullet} Address',
        value_proc=lambda x: x.strip('0x')
    )
    answers['storage'] = click.prompt(
        f'{bullet} Storage',
        type=click.Choice(['volume', 'path']),
        default='path'
    )
    answers['data'] = click.prompt(
        f'{bullet} Chaindata {answers["storage"]}',
        type=click.Path(
            exists=True,
            file_okay=False,
            resolve_path=True
        ) if answers["storage"] == 'path' else click.STRING
    )
    answers['expose_rpc'] = click.confirm(
        f'{bullet} Expose RPC',
    )
    answers['expose_ws'] = click.confirm(
        f'{bullet} Expose WebSocket',
    )
    return answers


if __name__ == '__main__':
    # frozen app fix
    if getattr(sys, 'frozen', False):
        entrypoint(sys.argv[1:])
