import selectors
import socket
import time
import queue
sel = selectors.DefaultSelector()
common_data={}
def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    try:
        conn.setblocking(False)
        target_sock = socket.socket()
        target_sock.connect(target_server)
        sel.register(target_sock,selectors.EVENT_READ,data=['backward',conn])
        sel.register(conn, selectors.EVENT_READ, data=['forward',target_sock]) #注册到selectors对象中，后面可循环调用
    except:
        conn.sendall('无法连接到远程服务器！'.encode())
        print('无法连接到远程服务器!')


    # target_sock.setblocking(False)
    # sel.register(target_sock, selectors.EVENT_READ, data=send_data)
    # print('1')

def read(conn,sock_target, mask):
    # common_data.clear()
    data=conn.recv(1024)     # Should be ready
    if data:
        print('recive:',data)
        F.write(data)
        sock_target.sendall(data)

    else:
        print('closing', conn)
        sel.unregister(conn)   #取消注册
        sel.unregister(sock_target)
        conn.close()
        sock_target.close()
def send_data(cul_sock,mask):
    pass


target_server=('127.0.0.1',9000)
sock = socket.socket()
sock.bind(('192.168.0.105', 1234))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, data=[None])
with open('out.log','wb') as F:
    while True:

        events = sel.select()

        for key, mask in events:
            # print(key.data)
            if key.data[0] is None:
                accept(key.fileobj,mask)
            if key.data[0]=='forward':
                read(key.fileobj,key.data[1],mask)
            if key.data[0]=='backward':
                read(key.fileobj,key.data[1],mask)

