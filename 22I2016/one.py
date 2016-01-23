from socket import socket
from time import sleep, asctime
from importlib import import_module

s=socket()
s.bind(('127.0.0.1', 3333))
s.listen(0)

def handle_request(conn):
    with conn:
        recv= conn.recv(1024)
        print('request', recv)
        try:
            path=recv.decode('utf-8').split(' ')[1][1:]
            print(path)
            module= import_module(path)
            module='\n<ul><li>'+'</li>\n<li>'.join(dir(module))+'</li></ul>'
        except Exception:
            module=''
        mess='HTTP/1.1 '+('200 OK' if module!='' else '404 Not found')+'''


        <title>Current time and module content</title>
        <style>
        body:first-line{text-decoration:underline; font-family:Arial; font-size:32px;}
        </style>
        '''+asctime()+module
        conn.sendall(mess.encode('utf8'))

while True:
    conn,addr=s.accept()
    handle_request(conn)