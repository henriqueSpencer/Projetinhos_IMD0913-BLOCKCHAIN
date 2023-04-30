import hashlib, json

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.memPool = []
        self.createGenesisBlock()

    def createGenesisBlock(self):
        # Implemente aqui o método para gerar o bloco Genesis, invocado no construtor da classe,
        # chamando o método createBlock() previamente implementado.
        # O índice do bloco gênesis deve ser 0 (zero), e o previousBlock dele ser 0x0, com 64 dígitos 
        # hexadecimais (256 bits), codificados como uma string.
        # O método deve retornar o bloco genesis criado.

        return genesis_block 

    def createBlock(self):
        # Implemente aqui o método para retornar um bloco (formato de dicionário).
        # Lembre que o hash do bloco anterior é o hash na verdade somente do CABEÇALHO do bloco anterior.
        # Inclua o bloco criado na lista `chain`, por enquanto não precisamos valida-lo.
        # O método deve retornar o bloco recém-criado.
        return block

    @staticmethod
    def getBlockID(block):
        # Implemente aqui um método auxiliar para gerar o ID de um bloco passado como parâmetro.
        # Lembra o que é o ID de um bloco?!?! Hash do seu cabeçalho! 
        # Dica: as transações de um bloco não fazem parte de seu cabeçalho...
        # Dica2: não deixe de usar seus método previamente implementados.
        return block_id

    @staticmethod
    def generateHash(data):
        # var1 = json.dumps(data, sort_keys=True)
        #
        # h = hashlib.new('sha256')
        #
        # hash_object = hashlib.sha256(str(var1).encode('utf-8'))
        #
        # return hash_object.hexdigest()
        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()

    def printChain(self):
        # Implemente aqui um método para imprimir de maneira verbosa e intuitiva o blockchain atual.
        pass

# Teste, fique a vontade para modificar.
blockchain = Blockchain()
for x in range(0, 3): blockchain.createBlock()
blockchain.printChain()
