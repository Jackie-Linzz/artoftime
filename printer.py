#coding=utf8
import socket


IP = '192.168.1.5'
PORT = 9100

def gprint(content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    
    s.sendall(content)
    s.close()



if __name__ == '__main__':
    content = b'\x1b\x61\x00'
    content += bytes(u'永恒时光北京科技有限公司\n'.encode('gb18030'))
    gprint(content)
