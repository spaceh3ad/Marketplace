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
```
