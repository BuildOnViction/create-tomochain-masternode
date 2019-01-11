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
    compose_content = compose_template.render(**answers, **env)
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


def success(masternode_name: str, masternode_path: str) -> None:
    display(
        f'Success! Created {masternode_name} at {masternode_path}\n'
        'Inside that directory you can run several commands:',
        spacing_top=1
    )
    display(
        f'{click.style("docker-compose up|down", fg="cyan")}',
        spacing_top=1,
        padding=2
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
        f'Create|remove your masternode\'s containers',
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
        f'{click.style("cd", fg="cyan")} {masternode_name}',
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


if __name__ == '__main__':
    # frozen app fix
    if getattr(sys, 'frozen', False):
        entrypoint(sys.argv[1:])
