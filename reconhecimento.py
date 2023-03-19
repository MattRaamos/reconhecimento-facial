import cv2
import os
import numpy as np
import sqlite3

def buscar_informacoes_pessoa(nome):
    # conectar ao banco de dados
    conn = sqlite3.connect('pessoas.db')
    cursor = conn.cursor()
    # buscar as informações da pessoa pelo nome
    cursor.execute("SELECT idade, profissao, endereco FROM pessoas WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    # fechar a conexão com o banco de dados
    conn.close()
    # retornar as informações da pessoa
    return resultado


# diretório com as imagens das pessoas
dir_path = "pessoas"
# tamanho da imagem
img_size = (200, 200)

# carregar o modelo pré-treinado
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

# lista para armazenar as faces e os labels
faces = []
labels = []

# dicionário que mapeia os labels com os nomes das pessoas
label_dict = {}

# iterar sobre as imagens de cada pessoa
for i, person_name in enumerate(os.listdir(dir_path)):
    # ler a imagem
    img_path = os.path.join(dir_path, person_name)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # detectar as faces na imagem
    faces_detected = face_cascade.detectMultiScale(img)
    # iterar sobre cada face detectada
    for x, y, w, h in faces_detected:
        # recortar a face da imagem
        face = img[y:y+h, x:x+w]
        # redimensionar a face
        face = cv2.resize(face, img_size)
        # adicionar a face na lista de faces
        faces.append(face)
        # adicionar o label na lista de labels
        labels.append(i)
    # armazenar o nome da pessoa no dicionário
    label_dict[i] = person_name.split(".")[0]

# treinar o modelo
recognizer.train(faces, np.array(labels))

# inicializar a webcam
cap = cv2.VideoCapture(0)

while True:
    # capturar o frame
    ret, frame = cap.read()
    # converter para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detectar as faces no frame
    faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # iterar sobre cada face detectada
    for x, y, w, h in faces_detected:
        # desenhar um retângulo ao redor da face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # recortar a face da imagem
        face = gray[y:y+h, x:x+w]
        # redimensionar a face
        face = cv2.resize(face, img_size)
        # fazer a predição da face
        label_id, confidence = recognizer.predict(face)
        # obter o nome da pessoa a partir do label
        label_name = label_dict[label_id]
        # buscar as informações da pessoa pelo nome
        informacoes_pessoa = buscar_informacoes_pessoa(label_name)
        # exibir as informações da pessoa (se encontradas)
        if informacoes_pessoa is not None:
            idade, profissao, endereco = informacoes_pessoa
            cv2.putText(frame, f"Idade: {idade}", (x, y + h + 25), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Profissao: {profissao}", (x, y + h + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Endereco: {endereco}", (x, y + h + 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        # exibir o nome da pessoa e a confiança da predição
        cv2.putText(frame, f"{label_name} ({confidence:.2f})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        # exibir o frame
        cv2.imshow("Reconhecimento Facial", frame)
        # aguardar uma tecla ser pressionada
        if cv2.waitKey(1) == ord("q"):
            break

# liberar a memória e encerrar o programa
cap.release()
cv2.destroyAllWindows()
