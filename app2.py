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

        print(f'comecando recepcao...\n')
        txLen = 3000
        rxBuffer, nRx = com2.getData(txLen)
        print("recebeu {}" .format(rxBuffer))
        print(f'o tamnaho recebido: {txLen}')
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        # com1.disable()

        with open('img-recebido.png', 'wb') as file:
            file.write(rxBuffer)

        print(f'imagem salva...\n')

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()

    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
