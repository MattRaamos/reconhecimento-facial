import sqlite3
import cv2
import os

def cadastrar_pessoa():
    # Conectar ao banco de dados
    conn = sqlite3.connect('pessoas.db')
    cursor = conn.cursor()

    # Coletar informações da pessoa
    pasta = "pessoas"
    nome = input('Digite o nome da pessoa: ')
    idade = input('Digite a idade da pessoa: ')
    profissao = input('Digite a profissão da pessoa: ')
    endereco = input('Digite o endereço da pessoa: ')

    # Inserir informações da pessoa na tabela
    cursor.execute('''INSERT INTO pessoas (nome, idade, profissao, endereco)
                      VALUES (?, ?, ?, ?)''', (nome, idade, profissao, endereco))
    conn.commit()

    # Salvar imagem da pessoa na pasta "pessoas"
    pasta_pessoas = 'pessoas'
    if not os.path.exists(pasta_pessoas):
        os.makedirs(pasta_pessoas)

    # Abrir câmera e tira uma foto
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        cv2.imshow('Captura de Imagem', frame)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break
        elif k == ord('s'):
            nome_arquivo = f"{pasta}/{nome}.jpg"
            cv2.imwrite(nome_arquivo, frame)
            print(f"Foto salva com sucesso em {nome_arquivo}")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    cadastrar_pessoa()