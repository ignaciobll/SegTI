import socket


HOST = 'localhost'
PORT = 4443


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Socket created and binded.")


def cipher(key, iv, text):
    data = "{}\t{}\t{}".format(key, iv, text)  # key iv text
    s.send(bytearray(data.encode('ascii')))
    r = s.recv(1024)
    return r


print("Remember to s.close() when you are done.")
