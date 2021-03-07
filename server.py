from enlace import *
import time
import numpy as np

serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)


def receivement_handler(rxBuffer):
    length = len(rxBuffer)
    rx_head = rxBuffer[:10]
    rx_payload = rxBuffer[10:length - 4]
    rx_eop = rxBuffer[length - 4: length]
    return rx_head, rx_payload, rx_eop


def create_package(payload):

    HEAD = bytes(10)
    EOP = bytes(4)
    pacote = HEAD + payload + EOP
    return np.asarray(pacote)


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
            received_package = receivement_handler(rxBuffer)[1]

            print(f'recebeu o pacote com tamanho: {rxLen}\n')
            response = rxLen.to_bytes(2, 'big')
            response = create_package(response)
            com2.sendData(response)
            print(f'respondeu o cliente com o tamanho: {len(rxBuffer)}')

            try:
                is_finished_decoded_str = received_package.decode()
                print("recebeu sinal pra desligar")
                if is_finished_decoded_str == "fechou":
                    break
            except:
                print('')

            pacotes_recebidos.append(received_package)  # saving

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
