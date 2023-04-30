#http://127.0.0.1:8000/docs
#uvicorn api:app --port 8086  --reload
#curl http://127.0.0.1:8000/person/1
#curl http://127.0.0.1:8000 -X POST
from fastapi import FastAPI, Query, HTTPException, Path #gera documentação
from pydantic import BaseModel
from typing import Optional
import json
from blockchain import Blockchain
import hashlib, json, copy, time, random, time



'''
Rotas:
    1- Criar uma transacao
    2- Retorno o memory Pool
    3- Minerar
    4- Get chain
    5- Add um no a lista 
    6- solicitar aos nos suas blockchais e subscrever a sua

    /transactions/create
    /transactions/mempool
    /mine
    /chain
    /nodes/register
    /nodes/resolve
'''

app = FastAPI()
blockchain = Blockchain()

class Transacao(BaseModel):
    sender: str
    recipient: str
    amount: float
    timestamp: int
    privWifKey: str

#blockchain.createTransaction(
# '19sXoSbfcQD9K66f5hwP5vLwsaRyKLPgXF',
# '1MxTkeEP2PmHSMze5tUZ1hAV3YTKu2Gh1N',
# 0.1,
# 1637953954,
# 'L1US57sChKZeyXrev9q7tFm2dgA2ktJe2NP3xzXRv6wizom5MN1U')
# 1- Criar uma transacao
@app.post('/transactions/create', status_code=201)
def add_transaction(transacao: Transacao):
    retorno = blockchain.createTransaction(transacao.sender,  # remetente da transação;
                                 transacao.recipient,  # destinatário da transação;
                                 transacao.amount,  # valor a ser transferido do endereço do sender para o endereço do recipient;
                                 transacao.timestamp,  # data (formato unix) de criação da transação;
                                 transacao.privWifKey)
    return retorno

# 2- Retorno o memory Pool
@app.get('/transactions/mempool', status_code=200)
def get_mempool():
    return blockchain.memPool

# 3- Minerar
@app.get('/mine', status_code=200)
def run_mine():
    #get_true_chain()
    block = blockchain.createBlock()
    nonce = blockchain.mineProofOfWork(blockchain.prevBlock)
    return True

# 4- Get chain
@app.get('/chain', status_code=200)
def get_chain():
    return blockchain.chain


# 5- Add um no a lista
@app.post('/nodes/register', status_code=201)
def add_node(no: str):
    blockchain.nodes.add(no)
    return no

# 6- solicitar aos nos suas blockchais e subscrever a sua
@app.get('/nodes/resolve', status_code=200)
def get_true_chain():
    return blockchain.resolveConflicts()


# 7- get nodes
@app.get('/nodes/get', status_code=200)
def get_nodes():
    return blockchain.nodes

# 8- add random transactions
@app.get('/addRandomTransactions', status_code=200)
def add_randomTransaction():
    sender = '19sXoSbfcQD9K66f5hwP5vLwsaRyKLPgXF' # Você pode gerar novos endereços BTC em https://www.bitaddress.org/
    recipient = '1MxTkeEP2PmHSMze5tUZ1hAV3YTKu2Gh1N' # Você pode gerar novos endereços BTC em https://www.bitaddress.org/
    for x in range(0, 4):
        for y in range(0, random.randint(1,4)) :
            timestamp = int(time.time())
            amount = random.uniform(0.00000001, 100)
            transacao = blockchain.createTransaction(sender, # remetente da transação;
                                        recipient, # destinatário da transação;
                                        amount, # valor a ser transferido do endereço do sender para o endereço do recipient;
                                        timestamp, # data (formato unix) de criação da transação;
                                        'L1US57sChKZeyXrev9q7tFm2dgA2ktJe2NP3xzXRv6wizom5MN1U') # chave privada WIF de quem envia

    return True

# 9- add random blocks
@app.get('/addRandomBlock', status_code=200)
def add_randomBlock():
    add_randomTransaction()
    run_mine()
    return True