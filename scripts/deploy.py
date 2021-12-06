from brownie import (
    Market,
    TToken,
    config,
    network,
)
from scripts.helpful_scripts import (
    get_accounts,
)


def deploy_market():
    accounts = get_accounts()
    market = Market.deploy(
        {"from": accounts[0]},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"Deployed Market at: {market}")
    return market


def deploy_token():
    accounts = get_accounts()
    token = TToken.deploy(
        {"from": accounts[1]},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"Deployed Token at: {token}")
    return token


def main():
    pass
    # market = deploy_market()
    # token = deploy_token()
    # account = get_account()
