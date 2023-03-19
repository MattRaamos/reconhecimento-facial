import cadastrar_pessoa
import reconhecimento
import database

# Obter informações do usuário e salvar no banco de dados
nome = input("Digite seu nome: ")
idade = input("Digite sua idade: ")
profissao = input("Digite sua profissão: ")
endereco = input("Digite seu endereço: ")

cadastrar_pessoa(nome, idade, profissao, endereco)
print("Pessoa cadastrada com sucesso!")

# Tirar uma foto e tentar reconhecer o usuário
foto = reconhecimento.tirar_foto()
pessoa_encontrada = reconhecimento.reconhecer_pessoa(foto)

if pessoa_encontrada:
    nome, idade, profissao, endereco = database.obter_info_pessoa(pessoa_encontrada)
    print("Pessoa encontrada:")
    print(f"Nome: {nome}")
    print(f"Idade: {idade}")
    print(f"Profissão: {profissao}")
    print(f"Endereço: {endereco}")
else:
    print("Pessoa não encontrada.")
