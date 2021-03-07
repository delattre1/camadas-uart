import numpy as np

HEAD = [bytes([0]) for i in range(10)]
PAYLOAD = [bytes([0]) for i in range(0)]
EOP = [bytes([0]) for i in range(4)]


def datagram_builder(head=HEAD, payload=PAYLOAD, eop=EOP):
    pacote = head + payload + eop
    return np.asarray(pacote)


def receivement_handler(rxBuffer):
    length = len(rxBuffer)
    rx_head = rxBuffer[:10]
    rx_payload = rxBuffer[10:length - 4]
    rx_eop = rxBuffer[length - 4: length]
    return rx_head, rx_payload, rx_eop


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
