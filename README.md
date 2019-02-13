# create-tomochain-masternode
Set up a TomoChain masternode by running one command.

## Installation

Requires:
- Docker
- Docker-compose

You may choose one of the following methods:

### Binary

Download `create-tomochain-masternode` from the [latest release](https://github.com/tomochain/create-tomochain-masternode/releases/latest).

```bash
chmod +x create-tomochain-masternode
mv create-tomochain-masternode /usr/local/bin/
```

### Pypi

Requires Python >= 3.6.

```bash
pip3 install --user create-tomochain-masternode
```

## Usage

```
Usage: create-tomochain-masternode [OPTIONS] NAME

  Set up a TomoChain masternode by running one command.

Options:
  --testnet  Testnet instead of mainnet.
  --version  Show the version and exit.
  --help     Show this message and exit.
```

Simply run create-tomochain-masternode with the name of your masternode as arguemnt `NAME`.

```bash
create-tomochain-masternode tomochain09
```

Follow the wizard by replying to the following questions:

- **Coinbase private key**:

  Your masternode coinbase account private key.
  This is the account you configured your masternode with, not the one holding your funds.

- **Storage**:

  Either `docker volume` if you want to use one, or `host directory` if you want to bind mount a specific location of your filesystem.

- **Chaindata**:

  The name of the docker volume that will be used or the path to the directory to bind mount, depending on your answer to the last question.

- **Expose RPC**:

  If you want to expose or not port `8545`.
  It is the RPC api to your node.
  It should be only exposed if you have a specific reason to do so.
  The masternode owner is responsible of proxing and securing the RPC api as it should not be directly exposed to the internet.

- **Expose WebSocket**:

  If you want to expose or not port `8546`.
  It is the WebSocket api to your node.
  It should be only exposed if you have a specific reason to do so.
  The masternode owner is responsible of proxing and securing the WebSocket api as it should not be directly exposed to the internet.

- **Loging level**:

  Set the logging level of the TomoChain container to error, info or debug.
  Info or Error is usually a good logging level.
  Only use the debug level if you have a good reason to do so.
  It will generate a lot of output and increase ressource usage.

Once finished, you will get a folder named after your masternode (in our case "tomochain09") with two files.

`docker-compose.yml`

Which contains the instructions for docker compose to know how to configure your masternode container.

`.env`

Which contains the configuration made from your answers to the question.

Now that we generated the correct initial configuration for docker-compose, we just need to start our node.

```bash
docker-compose up -d
```

You can check that your masternode is running with the `ps` sub-command.

```bash
docker-compose ps
```

For more docker-compose commands, use `docker-compose --help` or refer to their [documentation](https://docs.docker.com/compose/reference/overview/).
