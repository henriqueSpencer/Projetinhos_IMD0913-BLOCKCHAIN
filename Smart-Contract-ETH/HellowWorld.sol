// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract HellowWorld {

    string dado;

    function set(string memory x) public {
        dado = x;
    }
    function get() public view returns (string memory) {
        return dado;

    }
}