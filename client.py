#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2020
# Aplicação
####################################################


from enlace import *
import time
import numpy as np

serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)


def separate_pacotes(img_array):

    len_img = len(img_array)
    tamanho_pacote = 200
    resto = len_img % tamanho_pacote
    pacotes = [img_array[i:i+tamanho_pacote]
               for i in range(0, len_img - resto, tamanho_pacote)]
    pacotes.append(img_array[len_img - resto:len_img])
    return pacotes


def main():
    try:
        com1 = enlace(serialName)
        com1.enable()
        print(f'Inicializado client - transmissão...\n')
        with open('advice.png', "rb") as image:
            f = image.read()
            img_array = bytearray(f)

        txBuffer = img_array
        pacotes = separate_pacotes(img_array)

        len_recebido_servidor = 0
        contador = 0
        for msg in pacotes:

            com1.sendData(np.asarray(msg))
            #print(f'enviou a mensagem {np.asarray(msg)}...\n')
            print(f'enviou a mensagem {contador}...\n')
            contador += 1

            #txSize = com1.tx.getStatus()

            rxLen = com1.rx.getBufferLen()

            while True:  # esperando confirmação recebimento
                if rxLen != 0:
                    break
                rxLen = com1.rx.getBufferLen()

            rxBuffer, nRx = com1.getData(rxLen)

            int_tamanho_recebido = int.from_bytes(rxBuffer, 'big')
            len_recebido_servidor += int_tamanho_recebido
            print(f'recebeu de volta o tamanho: {int_tamanho_recebido}')

        print(
            f'O tamanho da imagem era: {len(img_array)}\nTotal recebido servidor: {len_recebido_servidor}\n')

        if len(img_array) == len_recebido_servidor:
            print('Sucesso, encerrando a comunicação')
            str_sucesso = "foi tudo amigao"
            str_as_bytes = str.encode(str_sucesso)
            com1.sendData(np.asarray(str_as_bytes))

        else:
            print('Não deu certo :(')

        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


if __name__ == "__main__":
    main()
