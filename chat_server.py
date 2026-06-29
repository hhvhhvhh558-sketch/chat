import socket
import threading
import os

HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 8080))

clients = []

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(conn, addr):
    print(f'Подключился {addr}')
    clients.append(conn)
    try:
        while True:
            msg = conn.recv(1024)
            if not msg:
                break
            broadcast(msg, conn)
    except:
        pass
    finally:
        clients.remove(conn)
        conn.close()
        print(f'Отключился {addr}')

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f'Сервер чата запущен на порту {PORT}')
    try:
        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.daemon = True
            t.start()
    except KeyboardInterrupt:
        server.close()

if __name__ == '__main__':
    main()