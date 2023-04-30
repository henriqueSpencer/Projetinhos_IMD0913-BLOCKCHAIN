// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

import "./Owned.sol";

contract  Poupanca  is Mortal{
    // de 1 a 30 dias
    // multa de 10% se sacar antes
    event Debug(string fala, uint numero);

    mapping(address => uint ) public valorDepositado;
    uint public data_saque;
    //uint public auctionEndTime;

    // constructor(
    //     uint _biddingTime
    // ) public {
    //     auctionEndTime = block.timestamp + _biddingTime;
    // }


    //Função para depositar um valor definindo o tempo (em dias) em que o valor ficará bloqueado.
    function set_data(uint256 segundos) public {
        require(segundos >= 86400, "Valor em segundos menor do que um dia");
        require(segundos <= (30*86400), "Valor em segundos maior que 30 dias");
        data_saque = block.timestamp + segundos;

    }
    receive() external payable{
        emit Debug("Valor Depositado em ETH:",msg.value);
        valorDepositado[msg.sender] += (msg.value); //em wei
    }
    //Função para consultar o valor depositado pelo remetente da transação.
    function depositado_por(address conta) public view returns (uint) {
        return valorDepositado[conta];//retorno em wei
    }
    //Função para consultar o tempo restante para resgatar meu depósito sem multas.
    function get_tempo_restante() public view returns (uint) {
        return data_saque - block.timestamp;
    }
    //Função para consultar o valor da multa caso queira sacar o valor antes do tempo.
    function multal() public view returns (uint) {
        return address(this).balance/10; //retorno em wei- Multa =1/10 do balanço
    }
    //Função para resgatar o valor depositado em sua totalidade.
    function sacar() public onlyOwner{
        //Enviar
        if (block.timestamp >= data_saque){
            payable(msg.sender).transfer(address(this).balance);
        }
        else{
            payable(msg.sender).transfer((address(this).balance*9)/10);
        }




    }
    //Função para transferir a propriedade de um depósito para outro endereço.
    // Ja tem no Owened

}