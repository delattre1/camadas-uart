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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM6"                  # Windows(variacao de)


def main():
    try:
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()
        # Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.

        # aqui você deverá gerar os dados a serem transmitidos.
        # seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o
        # nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        pacotes_recebidos = []

        with open('img.png', "rb") as image:
            f = image.read()
            img_array = bytearray(f)
        len_img = len(img_array)
        resto = len_img % 1000
        pacotes = [img_array[i:i+1000]
                   for i in range(0, len_img - resto, 1000)]
        pacotes.append(img_array[len_img - resto:len_img])
        print(f'len de pacotes: {len(pacotes)}')
        # faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        print('a transmissão vai começar...\n')
        for i in range(len(pacotes)):
            com1.sendData(np.asarray(pacotes[i]))
            txSize = com1.tx.getStatus()
            print(f'\n Tamanho em tx: {txSize}')
            # Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
            print('vai começar a recepção...\n')
            # acesso aos bytes recebidos
            txLen = len(pacotes[i])
            rxBuffer, nRx = com1.getData(txLen)
            pacotes_recebidos.append(rxBuffer)
            print("recebeu {}" .format(rxBuffer))
            print(f'o tamnaho recebido: {nRx}')

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

        received_img = b''.join(pacotes_recebidos)
        print(received_img)

        with open('imagem-recebido.png', 'wb') as file:
            file.write(received_img)

        print(f'imagem salva...\n')

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
