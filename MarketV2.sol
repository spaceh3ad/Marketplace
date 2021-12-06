// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Market is Ownable {
    uint256 offerId = 0;
    uint256 constant NULL = 0;

    enum itemCondition {
        BAD,
        USED,
        BRAND_NEW
    }

    struct Offer {
        uint256 offerId;
        uint256 price;
        string item;
        string description;
        itemCondition condition;
        address issuer;
    }

    struct Buy {
        address token;
        address buyer;
    }

    Offer[] public offersArray;
    mapping(uint256 => Buy) public buyersMapping;

    event OfferIssuance(
        uint256 offerId,
        uint256 _priceInWei,
        string _item,
        string _description,
        itemCondition _itemCondition,
        address _issuer
    );
    event OfferPurchase(uint256 offerId, uint256 _priceInWei, address _buyer);
    event Arbitrage(address _arbitrageWinner, uint256 _itemId);

    function issueOffer(
        uint256 _priceInWei,
        string memory _item,
        string memory _description,
        itemCondition _itemCondition
    ) external returns (bool) {
        Offer memory newOffer = Offer(
            offerId,
            _priceInWei,
            _item,
            _description,
            _itemCondition,
            msg.sender
        );
        offersArray.push(newOffer);
        emit OfferIssuance(
            offerId,
            _priceInWei,
            _item,
            _description,
            _itemCondition,
            msg.sender
        );
        offerId++;
        return true;
    }

    function buyItemWithEth(uint256 itemId) public payable returns (bool) {
        uint256 price = offersArray[itemId].price;
        require(msg.value >= price, "Incorrect amount");

        Buy memory newBuy = Buy(address(this), msg.sender);
        buyersMapping[itemId] = newBuy;
        emit OfferPurchase(itemId, price, msg.sender);
        return true;
    }

    function buyItemWithToken(
        uint256 itemId,
        IERC20 token,
        uint256 amount
    ) public returns (bool) {
        uint256 price = offersArray[itemId].price;
        require(
            token.allowance(msg.sender, address(this)) >= price,
            "Wrong amount approved"
        );
        token.transferFrom(msg.sender, address(this), amount);

        Buy memory newBuy = Buy(address(token), msg.sender);

        emit OfferPurchase(itemId, price, msg.sender);
        return true;
    }

    function confirmRecive(uint256 _itemId) public {
        require(
            msg.sender == buyersMapping[_itemId].buyer || msg.sender == owner()
        );
        address _recipient = offersArray[_itemId].issuer;
        resolveOrder(_recipient, _itemId);
    }

    function resolveOrder(address _recipient, uint256 _itemId) internal {
        uint256 _amount = offersArray[_itemId].price;
        if (_recipient != address(this)) {
            _recipient = buyersMapping[_itemId].buyer;
        }

        address token = buyersMapping[_itemId].token;

        if (token == address(this)) {
            fullfillOrderPayment(_recipient, _amount);
        } else {
            fullfillTokenPayment(_recipient, _amount, IERC20(token));
        }

        delete offersArray[_itemId];
        delete buyersMapping[_itemId];
    }

    function fullfillOrderPayment(address _recipient, uint256 _amount)
        internal
    {
        payable(_recipient).transfer(_amount);
    }

    function fullfillTokenPayment(
        address _recipient,
        uint256 _amount,
        IERC20 _token
    ) public {
        _token.transfer(_recipient, _amount);
    }

    function arbitrage(address _winner, uint256 _itemId) public {
        require(msg.sender == owner(), "Only owner can call arbitrage.");
        resolveOrder(_winner, _itemId);
        emit Arbitrage(_winner, _itemId);
    }
}
