import socket


sk = socket.socket()
sk.connect(("10.15.145.241",10001))
recv=sk.recv(1024*10)
message = str(recv,encoding="utf-8")
print(message)


def get_ip_status(ip, port):  #端口扫描
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((ip, port))
        print('{0} port {1} is open'.format(ip, port))
    except Exception as err:
        print('{0} port {1} is not open'.format(ip, port))
    finally:
        server.close()


# if __name__ == '__main__':
#     host = '127.0.0.1'
#     get_ip_status(host, 10001)
