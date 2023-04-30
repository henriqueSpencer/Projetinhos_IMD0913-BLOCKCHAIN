[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=8374727&assignment_repo_type=AssignmentRepo)
# Atividade: Hashing (01-hashing)

Esta atividade tem como objetivo implementar o primeiro método no desenvolvimento do nosso **blockchain**. Este método estático será amplamente utilizado em várias etapas do processo, uma vez que *hashing* é uma das técnicas essenciais para o funcionamento deste modelo de blockchain.

## Metodologia e Avaliação

O desenvolvimento das atividades avaliativas deve ser realizada individualmente, em computador pessoal ou em computador do laboratório, com livre consulta a recursos na internet (*consulta != cópia*) e discussão entre colegas. Utilize a IDE de sua preferência (sugestão: Visual Studio Code).

As atividades são cumulativas, de forma que ao final teremos um blockchain funcional usando as técnicas e os conceitos téoricos vistos em sala de aula.

## Instruções de submissão

Submissão deve ser feita a partir do GitHub Classroom até às 18:30 do dia 05/11/2022. Basta realizar o *commit* do seu arquivo `blockchain.py` no repositório privado criado para você a partir do link disponibilizado (associe sua conta GitHub ao seu nome na plataforma). Qualquer dúvida nesta etapa consulte o professor. **Atenção!** Não mexer/editar o arquivo `test_github_classroom.py`.

## Instalação

Baixe o arquivo `./blockchain.py` para obter o *boilerplate* para esta atividade. Caso seja necessário, utilize o gerenciador de pacotes [pip](https://pip.pypa.io/en/stable/) para instalar os módulos necessários. Todos os *boilerplates* são compatíveis com o Python 3+.

## Descrição

A assinatura do método já está presente na classe `Blockchain`:

```python
@staticmethod
def generateHash(data):
```

Importe o módulo `hashlib` a sua classe e implemente o método `generateHash` para retornar a string referente ao *hash* **SHA256** do argumento passado. Note que o argumento passado pode ser um objeto Python, desde que esteja serializado (veja em [Dicas](#dicas)).

O arquivo contém um simples teste para verificar se o *output* do seu método está retornando o *hash* esperado para o *input* fornecido.

## Dicas

Confira a documentação do hashlib [https://docs.python.org/3/library/hashlib.html] para verificar como utilizar a função SHA256.

Usar `json.dumps()` do módulo `json` para serializar o objeto de entrada em uma string no formato JSON antes, e lembrar de manter a estrutura sempre ordenada (`sort_keys=True`). Assim temos a garantia de que a função irá retornar o mesmo *hash* independentemente da ordem em que as chaves são apresentadas, crucial para validação de algumas estruturas de nosso blockchain.

```python
json.dumps(data, sort_keys=True)
```

## Licença
[MIT](https://choosealicense.com/licenses/mit/)

