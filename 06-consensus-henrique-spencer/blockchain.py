import hashlib, json, copy, time, random, time
import bitcoinlib 
import requests

DIFFICULTY = 4 # Quantidade de zeros (em hex) iniciais no hash valido.

class Blockchain(object):
    '''Classe utilizada para representar um blockchain privado baseado no protocolo Bitcoin.'''

    def __init__(self):
        self.chain = []
        self.memPool = []
        self.nodes = set() #set(["http://127.0.0.1:5000"]) # Conjunto para armazenar os nós registrados.
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
    def isValidChain(chain):
        '''
        Dado uma chain passada como parâmetro, faz toda a verificação se o blockchain é válido:
         1. PoW válido
         2. Transações assinadas e válidas
         3. Merkle Root válido
         4. Hash do bloco anterior válido.
        Retorna True se válido, False caso contrário.
        '''
        retorno = True
        while retorno ==True:
            for index, block in reversed(list(enumerate(chain))):
                retorno = Blockchain.isValidProof(block, block['nonce']) # VALIDA o NONCE - Proof of work
                retorno = Blockchain.isValidTransactions(block['transactions']) # Valida as transações
                retorno = Blockchain.isValidMerkleRoot(block['transactions'], block['merkleRoot']) #VALIDA O MERKLEROOT
                if index-1>=0:
                    retorno = Blockchain.isValidLastBlockHash(chain[index-1],block['previousHash'])# VALIDA O HASH DO BLOCO ANTERIOR
            break
        return retorno

    def resolveConflicts(self):
        ''' Consulta todos os nós registrados, e verifica se algum outro nó tem um blockchain mais comprido e válido. Em caso positivo, substitui seu próprio chain '''
        for no in self.nodes:

            chain_no = requests.get(f'{no}/chain').json()
            chain_valida = Blockchain.isValidChain(chain_no)
            if len(chain_no)>len(self.chain) and chain_valida:
                self.chain = chain_no


    @staticmethod
    def isValidProof(block, nonce):
        '''Retorna `True` caso o nonce passado como argumento seja válido para o block passado como argumento, `False` caso contrário.'''
        block['nonce'] = nonce
        return Blockchain.getBlockID(block)[:DIFFICULTY] == '0' * DIFFICULTY

    def createTransaction(self, sender, recipient, amount, timestamp, privWifKey):
        '''Cria, insere no mempool e retorna uma nova transação, assinada pela chave privada WIF do remetente.'''
        
        tx = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': timestamp
        }
 
        tx['signature'] = Blockchain.sign(privWifKey, json.dumps(tx, sort_keys=True))
        self.memPool.append(tx)

        return tx

    @staticmethod
    def isValidTransactions(transacoes):
        '''Retorna true caso as transações do bloco sejam validas'''
        retorno = True
        while retorno == True:
            for transacao in transacoes:
                message = copy.copy(transacao)
                message.pop("signature", None)
                message = json.dumps(message, sort_keys=True)
                retorno = Blockchain.verifySignature(transacao['sender'], transacao['signature'], message)
            break
                #address, signature, message

        return retorno

    @staticmethod
    def isValidLastBlockHash(block_anterior, block_anterior_hash):
        '''Retorna true caso o hash do bloco anterior seja o mesmo que esta escrito no atual'''
        if Blockchain.getBlockID(block_anterior) == block_anterior_hash:
            return True
        else:
            return False
    @staticmethod
    def isValidMerkleRoot(transactions,markle_root):
        '''Retorna true caso a merkleRoot passada seja igual a gerada pelas transações'''
        if markle_root == Blockchain.generateMerkleRoot(transactions):
            return True
        else:
            return False


    @staticmethod
    def generateMerkleRoot(transactions):
        '''Retorna a Merkle Root de um conjunto de transações.'''
        if len(transactions) == 0:
            return '0'*64

        txHashes = [] 
        for tx in transactions:
            txHashes.append(Blockchain.generateHash(tx))

        return Blockchain._hashTxHashes(txHashes)

    @staticmethod
    def _hashTxHashes(txHashes):
        ''' Função auxiliar recursiva para cálculo do MerkleRoot.'''
        if len(txHashes) == 1: # Condição de parada.
            return txHashes[0]

        if len(txHashes)%2 != 0: # Confere se a quantidade de hashes é par.
            txHashes.append(txHashes[-1]) # Se não for, duplica o último hash.

        newTxHashes = []
        for i in range(0,len(txHashes),2):       
            newTxHashes.append(Blockchain.generateHash(txHashes[i] + txHashes[i+1]))
        
        return Blockchain._hashTxHashes(newTxHashes)

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

        for block in reversed(self.chain) :

            if (block['index'] < len(self.chain)):
                print(32*' ', 'A', 39*' ')
                print(32*' ', '|', 39*' ')

            print(' __________________________________________________________________\n| {0:<0} |\
                \n ------------------------------------------------------------------\
                \n| Índice:         Timestamp:              Nonce:                   |\n| {1:<16d}{2:<24d}{3:<25d}|\
                \n|                                                                  |\
                \n| Merkle Root:                                                     |\n| {4:<0} |\
                \n|                                                                  |\
                \n| Transações:                                                      |\n| {5:<16d}                                                 |\
                \n|                                                                  |\
                \n| Hash do último bloco:                                            |\n| {6:<0} |\
                \n ------------------------------------------------------------------'\
                .format(Blockchain.getBlockID(block),block['index'],block['timestamp'],block['nonce'],block['merkleRoot'],len(block['transactions']),block['previousHash']))



# Implemente sua API com os end-points indicados no GitHub Classroom.
# Implemente um teste com ao menos 2 nós simultaneos.


# Teste
if __name__ == '__main__':

    blockchain = Blockchain()

    sender = '19sXoSbfcQD9K66f5hwP5vLwsaRyKLPgXF' # Você pode gerar novos endereços BTC em https://www.bitaddress.org/
    recipient = '1MxTkeEP2PmHSMze5tUZ1hAV3YTKu2Gh1N' # Você pode gerar novos endereços BTC em https://www.bitaddress.org/
    # blockchain.isValidChain(blockchain.chain)
    # blockchain.resolveConflicts()
    #Consulta todos os nós registrados, e verifica se algum outro nó tem um blockchain mais comprido e válido. Em caso positivo, substitui seu próprio chain
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

    #blockchain.isValidChain(blockchain.chain)
    blockchain.resolveConflicts()
    blockchain.printChain()

