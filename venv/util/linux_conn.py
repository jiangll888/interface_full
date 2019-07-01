import telnetlib
import time
import socket
socket.setdefaulttimeout(500)
import sys
import os
import subprocess
import pbs
from config import settings

def do_telnet(cmd,Host=settings.SQLITE_HOST, Port=settings.SQLITE_PORT, username=settings.SQLITE_USER, password=settings.SQLITE_PASSWD):
    # 连接Telnet服务器
    tn = telnetlib.Telnet(Host, Port, timeout=1)
    tn.set_debuglevel(3)

    # 输入登录用户名
    tn.read_until(b"login: ")
    tn.write((username + '\n').encode('utf-8'))
    # 输入登录密码
    tn.read_until(b"Password: ")
    tn.write((password + '\n').encode('utf-8'))

    # 判断密码错误提示，如果没有这个提示说明登录成功
    # if tn.read_until(finish):
    #     print("****** login incorrect!\n")
    tn.read_until(b"\r\n~ # ")
    tn.write(("cd /data/sqlite3" + "\n").encode('utf-8'))
    tn.write((cmd+"\n").encode('utf-8'))
    tn.read_until(b"\r\n/data/sqlite3000 #",3)
    # tn.write(("tftp -l {} -r {} -p {}".format(file,file,settings.win_ip) + "\n").encode('utf-8'))
    # tn.read_until(b"\r\n/data/sqlite3 #")
    # print("copy {} success".format(file))
    tn.close();


if __name__ == '__main__':
    # Host = input("IP:")  # Telnet服务器IP
    # Port = input("Port:")  # Telnet服务器端口
    Host = "192.168.11.88"
    Port = "23"
    username = 'root'  # 登录用户名
    password = ''
    # finish = 'Login incorrect'.encode("utf-8")  # 密码错误提示
    file = "person_feature_record.db"
    Index = 0
    print(time.asctime(), ":   ****** begin", "\n")
    password = ''
    do_telnet("ls")
