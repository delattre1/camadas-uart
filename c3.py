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

    def send_package(self):
        self.com1.sendData(self.pacote)

    def receive_package(self):
        self.rxLen = self.com1.rx.getBufferLen()

        while self.rxLen == 0:
            self.rxLen = self.com1.rx.getBufferLen()

            self.elapsed_time = time.time() - self.start_time

            if self.elapsed_time >= 5:
                send_again = input('Time Out - Enviar novamente? (s/n)')
                if send_again == 's':
                    self.send_package()
                    time.sleep(1)
                    self.start_time = time.time()

                elif send_again == 'n':
                    print(f'Finalizar client...')
                    os._exit(os.EX_OK)

        self.rxBuffer, self.nRx = self.com1.getData(self.rxLen)

        self.r_head, self.r_payload, self.r_eop = receivement_handler(
            self.rxBuffer)

        #print(f'chegou {self.rxBuffer} com tamanho: {self.nRx}')
        len_from_header = list(self.r_head)[0]
        must_resend = list(self.r_head)[2]

        print(
            f'Tamanho de acordo com o header: {len_from_header}\nChegou: {self.nRx}\n')

        if must_resend == 22:
            print('Foi solicitado o reenvio pela outra parte - enviando novamente...\n')
            self.send_package()
            self.receive_package()
            print(f' must resend: {must_resend}')

        elif len_from_header != (self.nRx):
            print(f'Houve perda de dados na recepção - Solicitando pacote novamente...\n')
            self.pacote = datagram_builder(resend=True)
            self.receive_package()

    def waiting_handshake(self,):
        print(f'Verificando estado do servidor...')
        is_available = [b'\x11', b'\x01', b'\x11', b'\x11']

        self.pacote = datagram_builder(eop=is_available)
        self.send_package()

        while not self.finished_handshake:
            self.receive_package()

            if self.r_eop == b''.join(is_available):
                print(f'Handshake realizado,\nIniciando o envio dos pacotes...\n')
                self.finished_handshake = True

    def main(self,):
        print(f'Client inicializado...\n')

        self.start_time = time.time()
        while not self.finished_handshake:
            self.waiting_handshake()

        print(f'Iniciando o envio dos pacotes...')

        os._exit(os.EX_OK)


client = Client('imgs/advice.png')
client.main()
