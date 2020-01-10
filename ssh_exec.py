import paramiko
import sys
import time
import os

def executeCommand(ip, passw, host):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(str(ip),port=22, username='root', password=str(passw), timeout=60)
        channel = client.invoke_shell()
        stdin = channel.makefile('wb')
        stdout = channel.makefile('rb')

        stdin.write('''
        sudo su
        echo "ssh-rsa " >> /root/.ssh/authorized_keys
        service sshd restart
        exit
        logout
        ''')
        
        print(stdout.read())
        file = open('results.txt','a')
        file.write('\nDone,' + host)

        stdout.close()
        stdin.close()
        client.close()
    except:
        file = open('results.txt','a')
        file.write('\nUnreachable,' + host)


file = open('ssh-exec.txt','r')
file = file.readlines()
for line in file:
    ip = line.split(',')[0]
    passw = line.split(',')[1]
    host = line.split(',')[2]
    executeCommand(ip, passw, host)
