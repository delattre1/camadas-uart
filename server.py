#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2020
# Aplicação
####################################################


# esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código!


from enlace import *
import time
import numpy as np

serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)


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
            print(f' recebeu o pacote com tamanho: {rxLen}\n')

            # try:
            #    is_finished_decoded_str = rxBuffer.decode('utf-8')
            #    print(is_finished_decoded_str)
            # except:
            #    print('ahah')

            com2.sendData(np.asarray(rxLen.to_bytes(2, 'big')))
            print(f'respondeu o cliente com o tamanho: {len(rxBuffer)}')

            pacotes_recebidos.append(rxBuffer)  # saving

        received_img = b''.join(pacotes_recebidos)

        with open('imagem-recebida.png', 'wb') as file:
            file.write(received_img)

        print(f'imagem salva...\n')

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        # com1.disable()

        # with open('img-recebido.png', 'wb') as file:
        #    file.write(rxBuffer)

        #print(f'imagem salva...\n')

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()


    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
