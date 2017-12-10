import socket


HOST = 'localhost'
PORT = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def cipher(key, iv, text):
    data = key + b'\t' + iv + b'\t' + text  # key iv text

    # print("="*30)
    # print(data)
    # print(str(len(key)) + "\t" + key.decode('ascii'))
    # print(str(len(iv))  + "\t" + iv.decode('ascii'))
    # print(str(len(text))+ "\t" + text.decode('ascii'))
    # print("-"*30)


    s.send(data)
    print("Enviado: {}".format(data))
    r = s.recv(1024)
    return r


print("Remember to client.s.close() when you are done.")
