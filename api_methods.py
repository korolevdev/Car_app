import MySQLdb
import socket
from app import *

def hello():
    res = {}
    sock = socket.socket()
    res["Hello"] = sock.recv(1024)
    sock.close()

    return res
