from brownie import (
    accounts,
    network,
    config,
    LinkToken,
    Contract,
)
from web3 import Web3

FORKED_LOCAL_ENVIROMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development", "ganache-local"]


def get_accounts(index=None, id=None):
    return accounts.from_mnemonic(config["wallets"]["from_mnemonic"], 10)
