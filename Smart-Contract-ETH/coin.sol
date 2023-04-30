// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract Coin {

    address public minter; //dono do contrato

    mapping(address => uint ) public balances;

    event Transferencia(address from, address to, uint amount);

    constructor(){ //é executado apenas na implantaçnao do contrato na rede
        minter = msg.sender; //pega quem implantou
    }

    function mint(address receiver, uint amount) public {
        require(msg.sender == minter);
        balances[receiver] += amount;
    }

    function sender(address receiver, uint amount) public {
        require(amount <= balances[msg.sender], "Saldo Insuficiente");
        balances[msg.sender] -= amount;
        balances[receiver] += amount;
        emit Transferencia(msg.sender, receiver, amount);
    }
}