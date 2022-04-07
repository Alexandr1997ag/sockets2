import socket, threading
import os
import struct

# Создать клиентский объект
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Целевой хост
host = input('целевой IP-адрес входа')

while True:
    name = input('Пожалуйста, введите личный ник, не более десяти символов, менее одного символа')
    if 1 < len(name) < 10:
        break

# Порт назначения
port = 9090

# Подключить клиента
client.connect((host, port))
print('-' * 5 + 'подключился к серверу' + '-' * 5)
print('-' * 5 + 'Enter, чтобы закрыть соединение с сервером' + '-' * 5)

def send_file_func():
    send_file(client, "divan.png")
    print('File has sent')


def outdatas():
    while True:

        # Введите информацию, которая будет отправлена на сервер
        outdata = input('')

        if outdata == 'enter':
            break
            # Отправить на сервер
        client.send(f'{name}:{outdata}'.encode('utf-8'))



        print('%s:%s' % (name, outdata))


def indatas():
    while True:
        # Принимаем информацию с сервера
        indata = client.recv(1024)
        # Закодировать полученную информацию
        print(indata.decode('utf-8'))

        if ('Сервер:' and f'Пришли файл, {name}') in indata.decode('utf-8'):
            client.send(f'{name}:Я прислал файл'.encode('utf-8'))
            send_file_func()
            #client.send(f'{name}:Я прислал файл'.encode('utf-8'))




def send_file(sck: socket.socket, filename):
    # Получение размера файла.
    filesize = os.path.getsize(filename)
    # В первую очередь сообщим серверу,
    # сколько байт будет отправлено.
    sck.sendall(struct.pack("<Q", filesize))
    # Отправка файла блоками по 1024 байта.
    with open(filename, "rb") as f:
        while read_bytes := f.read(1024):
            sck.sendall(read_bytes)

# Создать многопоточность
# Установить получение информации, объект потока
t1 = threading.Thread(target=indatas, name='input')

# Создание выходной информации, объект потока
t2 = threading.Thread(target=outdatas, name='out')

# Начать многопоточность
t1.start()
t2.start()

# Заблокировать поток, основной поток не может завершиться, пока не завершится выполнение дочернего потока.
# t1.join()
t2.join()

# Закрыть соединение
print('-' * 5 + 'сервер отключен' + '-' * 5)
client.close()