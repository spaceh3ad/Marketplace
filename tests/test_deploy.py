from brownie import reverts, Market, TToken
import time

import pytest


@pytest.fixture
def market(accounts):
    return accounts[0].deploy(Market)


@pytest.fixture
def token(accounts):
    return accounts[1].deploy(TToken)


@pytest.fixture
def issueOffer(market, accounts):
    market.issueOffer(100000000000, "bike", "mtb", 1, {"from": accounts[6]})


def test_marketDeploy(market, accounts):
    assert market.admin() == accounts[0], "Wrong owner"


def test_issueOffer(market, accounts, issueOffer):
    expected = (0, 100000000000, "bike", "mtb", 1, accounts[6])
    assert market.offersArray(0) == expected, "Can't issue an offer"


def test_buyItemWithEth(market, accounts, issueOffer):
    market.buyItemWithEth(0, {"from": accounts[4], "amount": 100000000000})
    assert market.buyersMapping(0)[1] == accounts[4]
    assert market.balance() == 100000000000


def test_buyItemWithToLessEth(market, accounts, issueOffer):
    with reverts("Incorrect amount"):
        market.buyItemWithEth(0, {"from": accounts[4], "amount": 100000000})


def test_buyItemWithToken(market, token, accounts, issueOffer):
    token.approve(market.address, 100000000000)
    market.buyItemWithToken(0, token, 100000000000, {"from": accounts[1]})
    assert token.balanceOf(market.address) == 100000000000
    assert market.buyersMapping(0)[1] == accounts[1]


def test_buyItemWithToLessToken(market, token, accounts, issueOffer):
    token.approve(market.address, 1000000000)
    with reverts("Wrong amount approved"):
        market.buyItemWithToken(0, token, 1000000000, {"from": accounts[1]})


def test_confirmReceiveEth(market, accounts, issueOffer):
    market.buyItemWithEth(0, {"from": accounts[4], "amount": 100000000000})

    assert market.buyersMapping(0)[1] == accounts[4]
    issuer = market.offersArray(0)[5]

    assert issuer == accounts[6]

    _balance = accounts[6].balance()

    market.confirmRecive(0, {"from": accounts[4]})

    assert accounts[6].balance() == _balance + 100000000000


def test_confirmReciceToken(market, token, accounts, issueOffer):
    offerIssuer = market.offersArray(0)[5]
    token.approve(market.address, 100000000000, {"from": accounts[1]})
    market.buyItemWithToken(0, token.address, 100000000000, {"from": accounts[1]})
    market.confirmRecive(0, {"from": accounts[1]})
    assert token.balanceOf(offerIssuer) == 100000000000


def test_confirmReceiveEthInvalidAddress(market, accounts, issueOffer):
    market.buyItemWithEth(0, {"from": accounts[4], "amount": 100000000000})
    with reverts():
        market.confirmRecive(0, {"from": accounts[9]})


def test_arbitrageIssuerEth(market, accounts, issueOffer):
    test_buyItemWithEth(market, accounts, issueOffer)
    _balance = accounts[6].balance()
    market.arbitrage(market.offersArray(0)[5], 0, {"from": accounts[0]})
    assert accounts[6].balance() == _balance + 100000000000


def test_arbitrageBuyerEth(market, accounts, issueOffer):
    test_buyItemWithEth(market, accounts, issueOffer)
    _balance = accounts[4].balance()
    market.arbitrage(market.buyersMapping(0)[1], 0, {"from": accounts[0]})
    assert accounts[4].balance() == _balance + 100000000000


def test_arbitrageIssuerToken(market, token, accounts, issueOffer):
    test_buyItemWithToken(market, token, accounts, issueOffer)
    _balance = token.balanceOf(accounts[6])
    market.arbitrage(market.offersArray(0)[5], 0, {"from": accounts[0]})
    assert token.balanceOf(accounts[6]) == _balance + 100000000000


def test_arbitrageBuyerToken(market, token, accounts, issueOffer):
    test_buyItemWithToken(market, token, accounts, issueOffer)
    _balance = token.balanceOf(accounts[1])
    market.arbitrage(market.buyersMapping(0)[1], 0, {"from": accounts[0]})
    assert token.balanceOf(accounts[1]) == _balance + 100000000000


def test_arbitrageNonOwner(market, token, accounts, issueOffer):
    test_buyItemWithToken(market, token, accounts, issueOffer)
    with reverts("Only owner can call arbitrage."):
        market.arbitrage(market.buyersMapping(0)[1], 0, {"from": accounts[8]})
