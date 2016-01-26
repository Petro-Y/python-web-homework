from socket import socket
from urllib.parse import parse_qs

class PseudoFlask:
    def __init__(self, *args):
        self.routes={}

    def route(self, path):
        def wrapper(f):
            self.routes[path]=f
            return f
        return wrapper

    def run(self):
        print('Starting PseudoFlask...')
        s=socket()
        s.bind(('127.0.0.1', 5000))
        s.listen(0)
        def handle_request(conn):
            with conn:
                recv= conn.recv(1024)
                print('request', recv)
                try:
                    path=recv.decode('utf-8').split(' ')[1]
                except Exception:
                    path='/'
                if path in self.routes:
                    mess='HTTP/1.1 200 OK\n\n'+self.routes[path]()
                else:
                    mess='HTTP/1.1 404 Not found\n\n<title>Page not found</title>No such page on this server :('
                conn.sendall(mess.encode('utf8'))
        while True:
            conn,addr=s.accept()
            handle_request(conn)

app=PseudoFlask(__name__)

@app.route('/')
def hello():
    return 'Hello, world!'

if __name__ == '__main__':
    app.run()