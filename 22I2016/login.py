from socket import socket
from time import sleep, asctime
from urllib.parse import parse_qs

s=socket()
s.bind(('127.0.0.1', 4444))
s.listen(0)

def check(username, password):
    with open('passwords.txt') as f:
        for l in f:
            if l.strip()=='': continue
            u,p=l.strip().split(':', 1)
            if username==u and password==p: return True

def handle_request(conn):
    with conn:
        recv= conn.recv(1024)
        print('request', recv)
        try:
            path=recv.decode('utf-8').split(' ')[1]
        except Exception:
            path='/'
        if path=='/':
            mess='''HTTP/1.1 200 OK

            <title>Log in</title>
            <form action="\login">
            <input name="username"> <input name="password" type=password> <input type=submit>
            </form>
            '''
        elif path.startswith('/login?'):
            try:
                q=parse_qs(path.split('?',1)[1])
                username=q['username'][0]; password=q['password'][0]
            except Exception:
                username=password=''
            print(username, password)
            if check(username, password):
                mess='''HTTP/1.1 200 OK

                <title>Welcome!</title>'''+'Hello, '+username+'!'
            else:
                mess='''HTTP/1.1 403 Access denied

                <title>Access denied</title>You are not logged in :('''
        else:
                mess='''HTTP/1.1 404 Not found

                <title>Page not found</title>No such page on this server :('''
        conn.sendall(mess.encode('utf8'))

while True:
    conn,addr=s.accept()
    handle_request(conn)