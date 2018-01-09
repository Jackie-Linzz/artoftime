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
    #content = b'\x1b\x61\x00'
    initialization = b'\x1b\x40'
    align_left = b'\x1b\x61\x00'
    align_center = b'\x1b\x61\x01'
    align_right = b'\x1b\x61\x02'
    content = initialization + align_left
    content += u'名称\t'.encode('gb18030')
    content += align_right
    content += ('%s %s\n' % (u'数量', u'价格')).encode('gb18030')
    content += align_left
    content += (u'-'*33).encode('gb18030')
    content += '\n\n\n\n\n\n\n\n'
    content = bytes(content)
    gprint(content)
