from brownie import Market, TToken, config, network, accounts


def deploy_market():
    market = Market.deploy(
        {"from": accounts[0]},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"Deployed Market at: {market}")
    return market


def deploy_token():
    token = TToken.deploy(
        {"from": accounts[1]},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"Deployed Token at: {token}")
    return token


def main():
    market = deploy_market()
    token = deploy_token()
    return market, token
