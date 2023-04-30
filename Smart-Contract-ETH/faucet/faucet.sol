// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

import "./Owned.sol";

contract  Faucet  is Mortal{

    event Withdraw(address to, uint amount);
    event Deposit(address from, uint amount);

    receive() external payable{
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint amount) public{
        require(amount <= 0.1 ether, "Quantidade maxima atingida.");
        require( address(this).balance >= amount, "Saldo do faucet insuficiente");
        payable(msg.sender).transfer(amount);
        emit Withdraw(msg.sender, amount);
    }

}