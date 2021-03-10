import os
from enlace import *
import time
import sys
import numpy as np
from utils import datagram_builder, receivement_handler, open_image, separate_pacotes

#serialName = "/dev/ttyACM0"
serialName = "/dev/ttyVirtualS1"


class Client:
    def __init__(self, path):
        self.com1 = enlace(serialName)
        self.com1.enable()
        self.finished_handshake = False
        self.img_array = open_image(path)
        self.lista_pacotes = separate_pacotes(self.img_array)
        self.contador_pacotes = 0

    def send_package(self, pacote):
        self.com1.sendData(pacote)

    def receive_package(self):

        self.rxLen = self.com1.rx.getBufferLen()

        while self.rxLen == 0:
            self.rxLen = self.com1.rx.getBufferLen()

        self.rxBuffer, self.nRx = self.com1.getData(self.rxLen)

        self.r_head, self.r_payload, self.r_eop = receivement_handler(
            self.rxBuffer)

        print(f'chegou {self.rxBuffer} com tamanho: {self.nRx}')
        len_from_header = list(self.r_head)[0]
        print(f'Tamanho de acordo com o header: {len_from_header}')

    def send_all_packages(self, lista_pacotes):
        for i in range(len(lista_pacotes)):
            print(f'Enviando o pacote [{i}]\n')
            if i == len(lista_pacotes):
                pacote = datagram_builder(
                    payload=lista_pacotes[i], is_lastpackage=True)
                print(f'Todos os pacotes foram enviados...\n')
            else:
                self.pacote = datagram_builder(payload=lista_pacotes[i])

            pause = input('press enter to send package')
            self.send_package(self.pacote)
            print(f'tamanho do que foi é: {len(self.pacote)}')
            time.sleep(1.5)
            # self.must_resend()

    def must_resend(self,):
        self.rxLen = self.com1.rx.getBufferLen()

        while self.rxLen == 0:
            self.rxLen = self.com1.rx.getBufferLen()
            time.sleep(1)

        print('recebeu algo')
        self.rxBuffer, self.nRx = self.com1.getData(self.rxLen)
        self.r_head, self.r_payload, self.r_eop = receivement_handler(
            self.rxBuffer)

        if list(self.r_head)[2] == 22:
            time.sleep(0.5)
            pause = input('Press Enter TO resend package')
            # self.send_package(self.pacote)
            print(f'[22]: reenviando o pacote [{self.contador_pacotes}]\n')
            print(f'tamanho do que foi é: {len(self.pacote)}')
            # self.must_resend()
        print('Não precisou reenviar o pacote,\nEnviando o próximo...')
        self.contador_pacotes += 1

    def waiting_handshake(self,):
        print(f'Verificando estado do servidor...')
        is_available = [b'\x11', b'\x01', b'\x11', b'\x11']

        pacote = datagram_builder(eop=is_available)
        self.send_package(pacote)

        start_time = time.time()

        while not self.finished_handshake:
            elapsed_time = time.time() - start_time

            self.receive_package()

            if self.r_eop == b''.join(is_available):
                print(f'Handshake realizado,\nIniciando o envio dos pacotes...\n')
                self.finished_handshake = True

            elif elapsed_time >= 5:
                want_send_again = input(
                    'TIME OUT - Sem resposta servidor\nGostaria de mandar novamente? (s/n)')
                if want_send_again == 's':
                    self.send_package(pacote)
                    start_time = time.time()
                elif want_send_again == 'n':
                    print(f'finalizar client...')
                    os._exit(os.EX_OK)

    def main(self,):
        print(f'Client inicializado...\n')

        while not self.finished_handshake:
            self.waiting_handshake()

        print(f'Iniciando o envio dos pacotes...')

        os._exit(os.EX_OK)


client = Client('imgs/advice.png')
client.main()
