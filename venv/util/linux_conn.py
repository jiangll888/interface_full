import telnetlib
import time
import socket
socket.setdefaulttimeout(500)
import sys
import os
import subprocess
import pbs
from config import settings
import serial

def do_telnet(cmd,Host=settings.SQLITE_HOST, Port=settings.SQLITE_PORT, username=settings.SQLITE_USER, password=settings.SQLITE_PASSWD):
    # 连接Telnet服务器
    tn = telnetlib.Telnet(Host, Port, timeout=2)
    tn.set_debuglevel(3)

    # 输入登录用户名
    tn.read_until(b"login: ")
    tn.write((username + '\n').encode('utf-8'))
    # 输入登录密码
    tn.read_until(b"Password: ")
    tn.write((password + '\n').encode('utf-8'))

    # 判断密码错误提示，如果没有这个提示说明登录成功
    # finish = 'Login incorrect'.encode("utf-8")  # 密码错误提示
    # wrong_pass = tn.read_until(finish).decode('utf-8')
    # if "Login incorrect" in wrong_pass:
    #     print("****** 密码错误! *************\n")
    tn.read_until(b"\r\n~ # ",3)
    tn.write(("cd /data/sqlite3" + "\n").encode('utf-8'))
    tn.write((cmd+"\n").encode('utf-8'))
    command_result = tn.read_until(b"\r\n/data/sqlite3000 #",3).decode('utf-8')
    tn.close();
    return command_result

def do_com():
    serial1 = serial.Serial("COM1", 115200)   #打开COM1并设置波特率为115200，COM1只适用于Windows

    # serial1 = serial.Serial("/ dev/ttyS0", 115200)   #打开 / dev / ttyS0并设置波特率为115200, 只适用于Linux

    print(serial1.portstr)
    serial1.write("hello".encode("utf-8"))

if __name__ == '__main__':
    # file = "person_feature_record.db"
    # print(time.asctime(), ":   ****** begin", "\n")
    # password = ''
    # res = do_telnet("ls")
    # print(res)
    do_com()

