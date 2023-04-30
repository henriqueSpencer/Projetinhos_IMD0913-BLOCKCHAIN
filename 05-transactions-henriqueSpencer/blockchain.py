import hashlib, json, copy, time, random, time
import bitcoinlib 

DIFFICULTY = 4 # Quantidade de zeros (em hex) iniciais no hash valido.

class Blockchain(object):
    '''Classe utilizada para representar um blockchain privado baseado no protocolo Bitcoin.'''

    def __init__(self):
        self.chain = []
        self.memPool = []
        self.createGenesisBlock()

    def createGenesisBlock(self):
        '''Cria, minera e retorna o bloco gênesis do blockchain. Chamado somente no construtor.'''
        genesis_block = self.createBlock()
        self.mineProofOfWork(self.prevBlock)
        return genesis_block

    def createBlock(self):
        '''Cria um novo bloco, inclui todas as transações pendentes e adiciona ao chain. O bloco ainda não tem nonce válido.'''
        block = {
            'index': len(self.chain),
            'timestamp': int(time.time()),
            'transactions': self.memPool,
            'merkleRoot': self.generateMerkleRoot(self.memPool),
            'nonce': 0,
            'previousHash': self.getBlockID(self.chain[-1]) if (len(self.chain)) else '0'*64
        }
        self.memPool = []
        self.chain.append(block)
        return block

    def mineProofOfWork(self, block):
        '''Retorna um nonce válido para o bloco passado como argumento.'''
        nonce = 0
        while self.isValidProof(block, nonce) is False:
            nonce += 1
        return nonce

    @staticmethod
    def isValidProof(block, nonce):
        '''Retorna `True` caso o nonce passado como argumento seja válido para o block passado como argumento, `False` caso contrário.'''
        block['nonce'] = nonce
        return Blockchain.getBlockID(block)[:DIFFICULTY] == '0' * DIFFICULTY

    def createTransaction(self, sender, recipient, amount, timestamp, privWifKey):
        '''Cria, insere no mempool e retorna uma nova transação, assinada pela chave privada WIF do remetente.'''
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": timestamp
        }
        mensagem = json.dumps(transaction, sort_keys=True)
        transaction["signature"] = Blockchain.sign(privWifKey, mensagem)
        self.memPool.append(transaction)
        return transaction

    @staticmethod
    def generateMerkleRoot(transactions):
        '''Retorna a Merkle Root de um conjunto de transações.'''
        if len(transactions)==0:
            return Blockchain.generateHash('')
        transactions_hash=[]
        inicio=1
        for transacao in transactions:
            transactions_hash.append(Blockchain.generateHash(transacao))

        while (len(transactions_hash) != 1) or inicio==1:
            inicio=0
            transactions_hash = Blockchain.rootinho(transactions_hash)

        return transactions_hash[0]

    @staticmethod
    def rootinho(transacoes_hash):
        if len(transacoes_hash) == 0:
            return ''
        markle_root = []
        if len(transacoes_hash) % 2 != 0:
            transacoes_hash.append(transacoes_hash[-1])

        for i in range(0,len(transacoes_hash),2):

            markle_root.append(Blockchain.generateHash(transacoes_hash[i] + transacoes_hash[i+1]))

        return markle_root

    @staticmethod
    def generateHash(data):
        '''Retorna a hash SHA256 dos dados passados como argumento.'''
        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()

    @staticmethod
    def getBlockID(block):
        '''Retorna o ID do bloco passado como argumento. O ID de um bloco é o hash do seu cabeçalho.'''
        blockCopy = copy.copy(block)
        blockCopy.pop("transactions", None)
        return Blockchain.generateHash(blockCopy)

    @property
    def prevBlock(self):
        '''Retorna o último bloco da chain.'''
        return self.chain[-1]

    @staticmethod
    def getWifCompressedPrivateKey(private_key=None):
        '''Retorna a chave privada no formato WIF-compressed da chave privada hex.'''
        if private_key is None:
            private_key = bitcoinlib.random_key()
        return bitcoinlib.encode_privkey(bitcoinlib.decode_privkey((private_key + '01'), 'hex'), 'wif')
        
    @staticmethod
    def getBitcoinAddressFromWifCompressed(wif_pkey):
        '''Retorna o endereço Bitcoin da chave privada WIF-compressed.'''
        return bitcoinlib.pubtoaddr(bitcoinlib.privkey_to_pubkey(wif_pkey))

    @staticmethod
    def sign(wifCompressedPrivKey, message):
        '''Retorna a assinatura digital da mensagem e a respectiva chave privada WIF-compressed.'''
        return bitcoinlib.ecdsa_sign(message, wifCompressedPrivKey)

    @staticmethod
    def verifySignature(address, signature, message):
        '''Verifica se a assinatura é correspondente a mensagem e o endereço BTC.
        Você pode verificar aqui também: https://tools.bitcoin.com/verify-message/'''
        return bitcoinlib.ecdsa_verify(message, signature, address)
    
    def printChain(self):
        return self.chain# Mantenha seu método de impressão do blockchain feito nas práticas passadas.


# Teste
if __name__ == '__main__':

    blockchain = Blockchain()

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
        # lista = []
        # lista.append(transacao)
        # lista.append(transacao)
        # blockchain.generateMerkleRoot(lista)
        block = blockchain.createBlock()
        blockchain.mineProofOfWork(blockchain.prevBlock)

    blockchain.printChain()
