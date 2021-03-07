from enlace import *
import time
import numpy as np
from server import receivement_handler, create_package
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)


def separate_pacotes(img_array):

    len_img = len(img_array)
    tamanho_pacote = 114
    resto = len_img % tamanho_pacote
    pacotes = [img_array[i:i+tamanho_pacote]
               for i in range(0, len_img - resto, tamanho_pacote)]
    pacotes.append(img_array[len_img - resto:len_img])
    return pacotes


def open_image(path):
    with open(path, "rb") as image:
        f = image.read()
        img_array = bytearray(f)
    return img_array


def main(img_path):
    try:
        com1 = enlace(serialName)
        com1.enable()
        print(f'Inicializado client - transmissão...\n')

        img_array = open_image(img_path)
        pacotes = separate_pacotes(img_array)

        len_recebido_servidor = 0
        contador = 0
        start_time = time.time()
        for PAYLOAD in pacotes:
            pacote = create_package(PAYLOAD)
            com1.sendData(pacote)

            print(f'Enviou a pacote: {contador}...\n')
            contador += 1

            rxLen = com1.rx.getBufferLen()

            while True:  # esperando confirmação recebimento
                if rxLen != 0:
                    break
                rxLen = com1.rx.getBufferLen()

            rxBuffer, nRx = com1.getData(rxLen)
            resposta = receivement_handler(rxBuffer)[1]
            int_tamanho_recebido = int.from_bytes(resposta, 'big')
            len_recebido_servidor += int_tamanho_recebido
            print(f'recebeu de volta o tamanho: {int_tamanho_recebido}')

        print(
            f'O tamanho da imagem era: {len(img_array)}\nTotal recebido servidor: {len_recebido_servidor}\n')

        if len(img_array) == len_recebido_servidor:
            print('Sucesso, encerrando a comunicação')
            elapsed_time = time.time() - start_time
            print(
                f'tempo gasto: {elapsed_time:.2f}\nvelocidade: {(len_recebido_servidor / elapsed_time):.2f} b/s')

            str_fim = "fechou"
            str_as_bytes = str_fim.encode()
            end_package = create_package(str_as_bytes)
            com1.sendData(end_package)
            print('enviando sinal pra desligar...\n')

            print("-------------------------")
            print("Comunicação encerrada")
            print("-------------------------")

        else:
            print('Não deu certo :(')

        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


if __name__ == "__main__":
    main('imgs/advice.png')
