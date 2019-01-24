from typing import Dict
import os
import sys

from jinja2 import Template
import click

from create_tomochain_masternode import __version__, envs,  templates


@click.command(help='Set up a TomoChain masternode by running one command.')
@click.argument('name', type=click.Path(
    file_okay=False,
    resolve_path=True
))
@click.option('--testnet', is_flag=True, help='Testnet instead of mainnet.')
@click.version_option(version=__version__)
def entrypoint(name: click.Path, testnet: bool) -> None:
    """Command line interface entrypoint"""
    env = envs.testnet if testnet else envs.mainnet
    masternode_path = name
    masternode_name = os.path.basename(os.path.normpath(name))
    if not is_folder_empty(masternode_path):
        error('Folder is not empty.')
        sys.exit(1)
    display(
        'Creating a new masternode in '
        f'{click.style(masternode_path, fg="green")}.',
        spacing=1
    )
    answers = ask()
    compose_template = Template(templates.compose)
    compose_content = compose_template.render(
        name=masternode_name,
        **answers,
        **env,
    )
    env_template = Template(templates.env)
    env_content = env_template.render(**answers, **env)
    try:
        if not os.path.exists(masternode_path):
            os.makedirs(masternode_path)
        with open(f'{masternode_path}/docker-compose.yml', 'w') as file:
            print(compose_content, file=file)
        with open(f'{masternode_path}/.env', 'w') as file:
            print(env_content, file=file)
    except Exception:
        error('Could not create files.')
    success(masternode_name, masternode_path)


def is_folder_empty(path: str) -> bool:
    try:
        return False if os.listdir(path) else True
    except FileNotFoundError:
        return True


def display(
    message: str,
    spacing_top: int = 0,
    spacing_bottom: int = 0,
    spacing: int = 0,
    padding: int = 0,
) -> None:
    newlines_top = '\n' * spacing_top if not spacing else '\n' * spacing
    newlines_bottom = '\n' * spacing_bottom if not spacing else '\n' * spacing
    leftpad = ' ' * padding
    click.echo(f'{newlines_top}{leftpad}{message}{newlines_bottom}')


def error(message: str) -> None:
    display(
        f'{click.style("! ", fg="red")}{message}',
        spacing=1
    )


def ask() -> Dict[str, str]:
    """Prompt users for parameters"""
    answers = {}
    bullet = f'{click.style("?", fg="cyan")}'
    answers['private_key'] = click.prompt(
        f'{bullet} Coinbase private key',
        hide_input=True,
    )
    answers['storage'] = click.prompt(
        f'{bullet} Storage',
        type=click.Choice(['docker volume', 'host directory']),
        default='host directory',
    )
    answers['data'] = click.prompt(
        f'{bullet} Chaindata {answers["storage"]}',
        type=click.Path(
            exists=True,
            file_okay=False,
            resolve_path=True,
        ) if answers["storage"] == 'host directory' else click.STRING
    )
    answers['expose_rpc'] = click.confirm(
        f'{bullet} Expose RPC',
    )
    answers['expose_ws'] = click.confirm(
        f'{bullet} Expose WebSocket',
    )
    answers['logging_level'] = click.prompt(
        f'{bullet} Logging level',
        type=click.Choice(['error', 'info', 'debug']),
        default='info',
        value_proc=logging_name_to_int,
    )
    return answers


def success(name: str, masternode_path: str) -> None:
    display(
        f'Success! Created {name} at {masternode_path}\n'
        'Inside that directory you can run several commands:',
        spacing_top=1
    )
    display(
        f'{click.style("docker-compose up|down", fg="cyan")}',
        spacing_top=1,
        padding=2
    )
    display(
        f'Create|remove your masternode\'s containers',
        padding=3
    )
    display(
        f'{click.style("docker-compose ps", fg="cyan")}',
        spacing_top=1,
        padding=2
    )
    display(
        f'List your masternode\'s containers',
        padding=3
    )
    display(
        f'{click.style("docker-compose stop|start [SERVICE...]", fg="cyan")}',
        spacing_top=1,
        padding=2
    )
    display(
        f'Stop|start your masternode\'s containers',
        padding=3
    )
    display(
        f'{click.style("docker-compose logs [SERVICES...]", fg="cyan")}',
        spacing_top=1,
        padding=2
    )
    display(
        f'List your masternode\'s containers',
        padding=3
    )
    display(
        f'We suggest that you begin by typing:',
        spacing_top=1,
    )
    display(
        f'{click.style("cd", fg="cyan")} {name}',
        spacing_top=1,
        padding=2
    )
    display(
        f'{click.style("docker-compose up -d", fg="cyan")}',
        padding=2
    )
    display(
        f'May the rewards be with you!',
        spacing=1
    )


def logging_name_to_int(name: str) -> int:
    if name == 'error':
        return 2
    elif name == 'info':
        return 3
    elif name == 'debug':
        return 4
    else:
        return 5


if __name__ == '__main__':
    # frozen app fix
    if getattr(sys, 'frozen', False):
        entrypoint(sys.argv[1:])
