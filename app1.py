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


def main():
    try:
        com1 = enlace(serialName)
        com1.enable()

        with open('img.png', "rb") as image:
            f = image.read()
            img_array = bytearray(f)

        txBuffer = img_array

        print(f'\n o array: { txBuffer}')
        print(f'len de txBuffer: {len(txBuffer)}')

        print('a transmissão vai começar...\n')
        com1.sendData(np.asarray(txBuffer))

        txSize = com1.tx.getStatus()
        print(f'\n txsize: {txSize}')

        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


if __name__ == "__main__":
    main()
