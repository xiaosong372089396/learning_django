#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import paramiko

def  remote():
    #paramiko.util.log_to_file('paramiko.log')
    #private_key_path = '/root/soft/sgplogin.pem'
    private_key_path = 'E:\key\key\sgplogin.pem'
    key = paramiko.RSAKey.from_private_key_file(private_key_path)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('127.0.0.1 ', 22, 'ec2-user' ,pkey=key)
    stdin, stdout, stderr = ssh.exec_command('sudo rm -rf /data/cache/*')
    value = stdout.read()
    ssh.close()
    return True

