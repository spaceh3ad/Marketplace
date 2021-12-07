# Marketplace
Soldity Smart Contract that immitates Digital Marketplace where users to trade items.

Featueres:
- issue multiple offers (with incremeting ID)
- see offers by quering `offersArray` with propriete ID to see details of offer
- buy any offer with providing ID with ETH or any ERC20 standard token (price is just wei)
- after the bought funds are frozen on smart contract address until buyer doesn't confirm that he received item
- arbtrage function to solve problematic orders (called by admin of `Marketplace`)
- after the offer is bought it's deleted from smart contract and other information about buyer
- refundig of either ETH or ERC20 while arbitrage


1. Requirements:
- Ensure you have `brownie` - https://eth-brownie.readthedocs.io/en/stable/install.html 
- Ensure you have `ganache-cli` for local development chain

2. Clone this repo
3. Ensure that you have $MNEMONIC envvar (can be ported from any ganache-cli session)
4. `brownie test` to test smart contracts
5. `brownie test -C` for coverage stats


*TEST COVERAGE*:
```
  contract: Market - 100.0%                                                                                                                                                           
    Market.arbitrage - 100.0%                                                                                                                                                         
    Market.buyItemWithEth - 100.0%                                                                                                                                                    
    Market.buyItemWithToken - 100.0%                                                                                                                                                  
    Market.confirmRecive - 100.0%                                                                                                                                                     
    Market.resolveOrder - 100.0%      
    

    tests/test_Market.py::test_marketDeploy PASSED                                                   [  7%]
    tests/test_Market.py::test_issueOffer PASSED                                                     [ 14%]
    tests/test_Market.py::test_buyItemWithEth PASSED                                                 [ 21%]
    tests/test_Market.py::test_buyItemWithToLessEth PASSED                                           [ 28%]
    tests/test_Market.py::test_buyItemWithToken PASSED                                               [ 35%]
    tests/test_Market.py::test_buyItemWithToLessToken PASSED                                         [ 42%]
    tests/test_Market.py::test_confirmReceiveEth PASSED                                              [ 50%]
    tests/test_Market.py::test_confirmReciceToken PASSED                                             [ 57%]
    tests/test_Market.py::test_confirmReceiveEthInvalidAddress PASSED                                [ 64%]
    tests/test_Market.py::test_arbitrageIssuerEth PASSED                                             [ 71%]
    tests/test_Market.py::test_arbitrageBuyerEth PASSED                                              [ 78%]
    tests/test_Market.py::test_arbitrageIssuerToken PASSED                                           [ 85%]
    tests/test_Market.py::test_arbitrageBuyerToken PASSED                                            [ 92%]
    tests/test_Market.py::test_arbitrageNonOwner PASSED                                              [100%]
```
