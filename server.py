from enlace import *
import time
import numpy as np

serialName = "/dev/ttyVirtualS0"           # Ubuntu (variacao de)


def main():
    try:
        com2 = enlace(serialName)
        com2.enable()

        print(f'Inicializado server - começando recepcao...\n')

        pacotes_recebidos = []
        while True:

            rxLen = com2.rx.getBufferLen()

            while True:  # esperando um pacote do cliente
                if rxLen != 0:
                    break
                rxLen = com2.rx.getBufferLen()

            rxBuffer, nRx = com2.getData(rxLen)
            print(f'recebeu o pacote com tamanho: {rxLen}\n')

            com2.sendData(np.asarray(rxLen.to_bytes(2, 'big')))
            print(f'respondeu o cliente com o tamanho: {len(rxBuffer)}')

            try:
                is_finished_decoded_str = rxBuffer.decode()
                print("recebeu sinal pra desligar")
                if is_finished_decoded_str == "fechou":
                    break
            except:
                print('')

            pacotes_recebidos.append(rxBuffer)  # saving

        received_img = b''.join(pacotes_recebidos)

        with open('imagem-recebida.png', 'wb') as file:
            file.write(received_img)

        print(f'imagem salva...\n')

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com2.disable()
        exit()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()


if __name__ == "__main__":
    main()
