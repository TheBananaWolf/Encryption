#!/usr/bin/python3
import os
import os.path
import datetime
from os import listdir
from os.path import isfile, join
from Cryptodome import Random
from Cryptodome.Cipher import AES
import time
import hashlib

class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        print("*****************************\nEncrypting file: "+str(file_name))
        startTime = datetime.datetime.now()
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)   
        os.remove(file_name)
        endTime = datetime.datetime.now()
        print("*****************************\nEncryption done for file: "+ str(file_name) + " and the execution time is "+ str((endTime-startTime).seconds)+ " seconds")

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CFB, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        print("*****************************\nDecrypting file: "+str(file_name))
        startTime = datetime.datetime.now()
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)
        endTime = datetime.datetime.now()
        print("*****************************\nDecryption done for file: " + str(file_name) + " and the execution time is "+ str((endTime-startTime).seconds)+ " seconds")

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'Encrption_Windows.py' and fname != 'data.txt.enc'):
                    dirs.append(dirName + "\\" + fname)
        return dirs

    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)

keys = hashlib.sha256(input("Input the key: \n").encode('utf-8')).hexdigest() 
key = bytes.fromhex(keys)
enc = Encryptor(key)
clear = lambda: os.system('cls')
run = lambda: os.system("python .\Encryption_Windows.py")
excutionTime = 0
if os.path.isfile('data.txt.enc'):
    while True:
        password = str(input("Enter password: "))
        enc.decrypt_file("data.txt.enc")
        p = ''
        with open("data.txt", "r") as f:
            p = f.readlines()
        if p[0] == password:
            enc.encrypt_file("data.txt")
            break

    while True:
        clear()
        if excutionTime != 0:
            print ("The total execution time is " + str((excutionTime)))
        choice = int(input(
            "1. Press '1' to encrypt file.\n2. Press '2' to decrypt file.\n3. Press '3' to Encrypt all files in the directory.\n4. Press '4' to decrypt all files in the directory.\n5. Press '5' to exit.\n"))
        clear()
        if choice == 1:
            enc.encrypt_file(str(input("Enter name of file to encrypt: ")))

        elif choice == 2:
            enc.decrypt_file(str(input("Enter name of file to decrypt: ")))

        elif choice == 3:
            startTime = datetime.datetime.now()
            enc.encrypt_all_files()
            endTime = datetime.datetime.now()
            excutionTime = endTime - startTime

        elif choice == 4:
            startTime = datetime.datetime.now()
            enc.decrypt_all_files()
            endTime = datetime.datetime.now()
            excutionTime = endTime - startTime

        elif choice == 5:
            exit()
        else:
            print("Please select a valid option!")

else:
    while True:
        clear()
        password = str(input("Setting up stuff. Enter a password that will be used for decryption: "))
        repassword = str(input("Confirm password: "))
        if password == repassword:
            break
        else:
            print("Passwords Mismatched!")
    f = open("data.txt", "w+")
    f.write(password)
    f.close()
    enc.encrypt_file("data.txt")
    clear()
    print("The program will re-run after 5s and required for the same key which encrypted the data.txt file")
    time.sleep(5)
    clear()
    run()