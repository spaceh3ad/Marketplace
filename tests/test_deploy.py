from brownie import Market, TToken

from scripts.helpful_scripts import get_accounts
import pytest


@pytest.fixture
def load_accounts():
    return get_accounts()


@pytest.fixture
def market(load_accounts):
    return load_accounts[0].deploy(Market)


@pytest.fixture
def token(load_accounts):
    return load_accounts[1].deploy(TToken)


@pytest.fixture
def issueOffer(market, load_accounts):
    tx = market.issueOffer(100000000000, "bike", "mtb", 1, {"from": load_accounts[1]})
    tx.wait(1)


def test_market(market, accounts):
    assert market.owner() == accounts[0], "Wrong owner"


def test_issueOffer(market, accounts, issueOffer):
    expected = (0, 100000000000, "bike", "mtb", 1, accounts[1])
    assert market.offersArray(0) == expected, "Can't issue an offer"


def test_buyItemWithEth(market, accounts, issueOffer):
    tx = market.buyItemWithEth(0, {"from": accounts[4], "amount": 100000000000})
    tx.wait(1)
    assert market.buyersMapping(0)[1] == accounts[4]
    assert market.balance() == 100000000000


def test_buyItemWithToken(market, token, accounts, issueOffer):
    token.approve(market.address, 100000000000)
    tx = market.buyItemWithToken(0, token, 100000000000, {"from": accounts[1]})
    tx.wait(1)
    assert token.balanceOf(market.address) == 100000000000
    assert market.buyersMapping(0)[1] == accounts[1]


# def test_confirmReceive(market, accounts, issueOffer)
