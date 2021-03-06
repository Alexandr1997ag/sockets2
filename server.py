# Импортировать пакет сокетов
import socket, threading
import struct
import os
# Создаем объект сокета
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Получить локальный ip
host = socket.gethostname()
s_ip = socket.gethostbyname(host)
print(s_ip)
# Данный порт
port = 9090

# Укажите IP и порт сервера
server.bind((host, port))

# Максимальное количество подключений
server.listen(5)

print('Enter Enter для выхода с сервера')

# Создайте список клиентов
clients = list()
# Хранить клиентов, которые создали потоки
end = list()


# Блокировка ожидания подключения клиента, возврата объекта подключения и адреса косвенного объекта
def accept():
    while True:
        client, addr = server.accept()
        clients.append(client)
        print("\ r" + '-' * 5 + f'сервер подключен через {addr}: текущее количество подключений: ----- {len (clients)}' + '-' * 5, end = '\n') #Взаимодействие с другими людьми


def recv_data(client):
    while True:
        # Принимаем информацию от клиента. Если приходит текст - печатаем его. Если файл, вызываем функцию receive_file
        # получаем сообщение вместе с файлом
        try:

            indata = client.recv(1024)
            if 'Я прислал файл' in indata.decode('utf-8'):
                # Ищем индекс символа : , затем определяем имя клиента, записываем в переменную name
                index = indata.decode('utf-8').find(':')
                name = indata.decode('utf-8')[:index]
                # Проверяем каталог на наличие папки, если нет - создаем, если есть, кладем файл в нужную папку
                if os.path.exists(name):
                    if os.path.isdir(name):
                        print('Папка существует')
                        filepath = name+'/'+'image-received.png'
                else:
                    print('Папка не существует')
                    os.mkdir(name)
                    filepath = name + '/' + 'image-received.png'
                # выполняем сохранение в нужном каталоге
                receive_file(client, filepath)
                print(indata.decode('utf-8'))
            else:
                print(indata.decode('utf-8'))

        except Exception as e:
            # если мы закрываем одного из клиентов, срабатывает блок except для того, чтобы не возникало
            # ошибок в процессе работы
            clients.remove(client)
            end.remove(client)
            print("\ r" + '-' * 5 + f'Сервер отключен: текущее количество подключений: ----- {len (clients)}' + '-' * 5, end = '\n')
            break

        finally:
            for clien in clients:
                # Перенаправить информацию от клиента и отправить ее другим клиентам
                if clien != client:
                    clien.send(indata)
                else:
                    continue


        #print('Файл получен')

def outdatas():
    while True:

        # Введите информацию, которая будет предоставлена клиенту
        print('')
        outdata = input('Введите сообщение своим пользователям\n')
        print()
        if outdata == 'enter':
            break
            print('Отправить всем:% s' % outdata)
            # Отправлять информацию каждому клиенту
        for client in clients:
            client.send(f"Сервер: {outdata}".encode('utf-8)'))

def indatas():
    while True:
        # Выполните цикл подключенных клиентов и создайте соответствующий поток
        for clien in clients:
            # Если поток уже существует, пропустить
            if clien in end:
                continue
            index = threading.Thread(target=recv_data, args=(clien,))
            index.start()
            end.append(clien)

def receive_file_size(sck: socket.socket):

    # Эта функция обеспечивает получение байтов,
    # указывающих на размер отправляемого файла,
    # который кодируется клиентом с помощью
    # struct.pack(), функции, которая генерирует
    # последовательность байтов, представляющих размер файла.
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = bytes()
    while received_bytes < expected_bytes:
        chunk = sck.recv(expected_bytes - received_bytes)
        stream += chunk
        received_bytes += len(chunk)
    filesize = struct.unpack(fmt, stream)[0]
    return filesize


def receive_file(sck: socket.socket, filename):
    # Сначала считываем из сокета количество
    # байтов, которые будут получены из файла.
    filesize = receive_file_size(sck)
    # Открываем новый файл для сохранения
    # полученных данных.
    with open(filename, "wb") as f:
        received_bytes = 0
        # Получаем данные из файла блоками по
        # 1024 байта до объема
        # общего количество байт, сообщенных клиентом.
        while received_bytes < filesize:
            chunk = sck.recv(1024)
            if chunk:
                f.write(chunk)
                received_bytes += len(chunk)
        print('Файл получен')


# Создать многопоточность
# Создать получающую информацию, объект потока
t1 = threading.Thread(target=indatas, name='input')
t1.start()

# Создать отправляемое сообщение, объект потока

t2 = threading.Thread(target=outdatas, name='out')
t2.start()

# Ожидание подключения клиента, объект потока

t3 = threading.Thread(target=accept(), name='accept')
t3.start()

# Блокировать округ, пока подпоток не будет завершен, и основной поток не может закончиться
# t1.join()
t2.join()

# Выключите все серверы
for client in clients:
    client.close()
print('-' * 5 + 'сервер отключен' + '-' * 5)