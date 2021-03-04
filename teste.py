import time
import numpy as np

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
    pacotes[i].append(pacotes[i][0] + pacotes[i][-1])
    codigo = np.asarray(pacotes[i])
    #print(f' {pacotes[0]} {pacotes[-1]}\n')
    #print(f'sum of first and last bytes = {pacotes[0] + pacotes[-1]}')
    print(codigo)
