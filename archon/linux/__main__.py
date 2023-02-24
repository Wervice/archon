import os
import sys
from termcolor import colored, cprint
import pyAesCrypt
import shutil
import random
import ftplib
from datetime import datetime

# wervice@proton.me
# This project is licensed under the GNUv3 license.
# Thanks to the developers of termcolor and pyAesCrypt.
# You find the license textes for termcolor and pyAesCrypt under legal.


def time_as_string():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")
def destroy(file):
    bi = 0
    string = ""
    while bi != 3:
        i = 0
        string = ""
        while i != os.stat(file).st_size:
            string = string+chr(random.randint(0, 100))
            i = i+1
        open(file, "w").write(string)
        bi = bi+1
    os.remove(file)
try:
    if len(sys.argv) == 1:
        help_doc_handel = open("assets/help.txt")
        help_doc = help_doc_handel.read()
        help_doc_handel.close()
        print(help_doc)
    elif sys.argv[1] == "help":
        help_doc_handel = open("assets/help.txt")
        help_doc = help_doc_handel.read()
        help_doc_handel.close()
        print(help_doc)
    elif sys.argv[1] == "fbackup":
        orig = input(colored("Folder: ", "blue"))
        dest = input(colored("Backup Location: ", "blue"))
        dirname = input(colored("Backup name: ", "blue"))
        encrypted = input(
            colored("Make encrypted backup? (y/N) ", "blue")) == "y"
        if encrypted:
            password = input(colored("Password: ", "blue"))
        if not encrypted:
            cprint("[-] Make compressed archive", "blue")
            shutil.make_archive(dest+dirname, "xztar", orig)
            if os.path.exists(dest+dirname+".tar.xz"):
                cprint("[*] Make compressed archive", "green")
        else:
            cprint("[-] Make compressed archive", "blue")
            shutil.make_archive(dest+dirname, "xztar", orig)
            if os.path.exists(dest+dirname+".tar.xz"):
                cprint("[*] Make compressed archive", "green")
            else:
                cprint("[x] Compression failed\nExiting now", "red")
                exit()
            cprint("[-] Encrypt archive", "blue")
            pyAesCrypt.encryptFile(
                dest+dirname+".tar.xz", dest+dirname+".tar.xz.e", passw=password, bufferSize=1024*64)
            if os.path.exists(dest+dirname+".tar.xz.e"):
                cprint("[*] Encrypt archive", "green")
            else:
                cprint("[x] Encryption failed\nExiting now", "red")
                exit()
            if input(colored("Do you want to overwrite unencrypted temporary data (y/N)? ", "blue")) == "y":
                destroy(dest+dirname+".tar.xz")
            else:
                os.remove(dest+dirname+".tar.xz")
        open("backup.log", "a").write("\n"+str(os.path.abspath(orig)) +
                                      ";"+str(os.path.abspath(dest))+";"+str(dirname)+";file")
        cprint("[*] Backup successfull", "green")
    elif sys.argv[1] == "frestore":
        backup = input(colored("Backup Location: ", "blue"))
        dest = input(colored("Folder to restore: ", "blue"))
        if not input(colored("Is the backup you want to use encrypted? (y/n) ", "blue")) == "y":
            cprint("[-] Restoring", "blue")
            shutil.unpack_archive(backup, dest)
        else:
            password = input(colored("Password: ", "blue"))
            cprint("[-] Restoring", "blue")
            shutil.copy(backup, "archon_restore_encrypted")
            pyAesCrypt.decryptFile(".\\archon_restore_encrypted",
                                   ".\\archon_restore_encrypted_d", passw=password, bufferSize=1024*64)
            shutil.unpack_archive(backup, dest, "xztar")
            os.remove("archon_restore_encrypted")
            destroy("archon_restore_encrypted_d")
        cprint("[*] Restored from backup", "green")
    elif sys.argv[1] == "fbackupftp":
        orig = input(colored("Folder: ", "blue"))
        bname = input(colored("Backup name: ", "blue"))
        sdest = input(colored("Destination path on server: ", "blue")) + bname + ".tar.xz"
        dest = "temp/"
        dirname = "ftp_upload"
        encrypted = input(
            colored("Make encrypted backup? (y/N) ", "blue")) == "y"
        hostname = input(colored("Hostname: ", "blue"))
        username = input(colored("Username: ", "blue"))
        lgpasswd = input(colored("Login Password: ", "blue"))
        tls = input(colored("Use TLS (y/N): ", "blue"))
        if encrypted:
            password = input(colored("Encryption password: ", "blue"))
        if not encrypted:
            cprint("[-] Make compressed archive", "blue")
            shutil.make_archive(dest+dirname, "xztar", orig)
            if os.path.exists(dest+dirname+".tar.xz"):
                cprint("[*] Make compressed archive", "green")
        else:
            cprint("[-] Make compressed archive", "blue")
            shutil.make_archive(dest+dirname, "xztar", orig)
            if os.path.exists(dest+dirname+".tar.xz"):
                cprint("[*] Make compressed archive", "green")
            else:
                cprint("[x] Compression failed\nExiting now", "red")
                exit()
            cprint("[-] Encrypt archive", "blue")
            pyAesCrypt.encryptFile(
                dest+dirname+".tar.xz", dest+dirname+".tar.xz.e", passw=password, bufferSize=1024*64)
            if os.path.exists(dest+dirname+".tar.xz.e"):
                cprint("[*] Encrypt archive", "green")
            else:
                cprint("[x] Encryption failed\nExiting now", "red")
                exit()
        if tls:
            ftp = ftplib.FTP_TLS(hostname)
        else:
            ftp = ftplib.FTP(hostname)
        cprint("[-] Connect to FTP Server", "blue")
        try:
            ftp.connect()
        except any:
            cprint("[x] Connection to FTP Server failed\nExiting now", "red")
            exit()
        cprint("[*] Connected", "green")
        cprint("[-] Login over FTP", "blue")
        try:
            ftp.login(username, lgpasswd)
        except ftplib.error_perm:
            cprint("[x] Login failed\nExiting now", "red")
            exit()
        cprint("[*] Uploading data", "green")
        try:
            ftp.storbinary("STOR %s" % (sdest), open(
                "temp/ftp_upload.tar.xz", "rb"))
        except FileNotFoundError:
            cprint("[x] File Not Found\nExiting now", "red")
            exit()
        except ftplib.error_perm:
            cprint("[x] Unknown Error\nExiting now", "red")
            exit()
        cprint("[*] Upload done", "green")
        cprint("[-] Close connection", "green")
        try:
            ftp.close()
        except ftplib.error_perm:
            cprint("[x] Error\nExiting now", "red")
            exit()
        if encrypted:
            if input(colored("Do you want to overwrite unencrypted temporary data (y/N)? ", "blue")) == "y":
                cprint("[-] Overwriting data", "blue")
                try:
                    destroy(dest+dirname+".tar.xz")
                except FileNotFoundError:
                    cprint(
                        "[x] Failed to destroy\nFile Not Found Error\nExiting now", "red")
                    exit()
            else:
                os.remove(dest+dirname+".tar.xz")
        open("backup.log", "a").write(
            "\n"+str(os.path.abspath(orig))+";"+str(hostname+"/"+sdest)+";"+str(bname)+";ftp")
        cprint("[*] Backup successfull", "green")
    elif sys.argv[1] == "frestoreftp":
        hostname = input(colored("Hostname: ", "blue"))
        username = input(colored("Username: ", "blue"))
        lgpasswd = input(colored("Login Password: ", "blue"))
        tls = input(colored("Use TLS (y/N): ", "blue"))
        backups = input(colored("Backup Location on server: ", "blue"))
        backup = "temp/archon_restore_ftp"
        dest = input(colored("Folder to restore: ", "blue"))
        if tls:
            ftp = ftplib.FTP_TLS(hostname)
        else:
            ftp = ftplib.FTP(hostname)
        cprint("[-] Connect to server", "blue")
        try:
            ftp.connect()
        except ftplib.error_perm:
            cprint("[x] Connection failed\nExiting now", "red")
            exit()
        cprint("[-] Login to server")
        try:
            ftp.login(username, lgpasswd)
        except ftplib.error_perm:
            cprint("[x] Login failed\nExiting now", "red")
            exit()
        cprint("[-] Donwload backup from server", "blue")
        try:
            ftp.retrbinary("RETR %s" % (backups), open(backup, "wb").write)
        except ftplib.error_perm:
            cprint("[x] Download failed\nExiting now", "red")
            exit()
        if not input(colored("Is the backup you want to use encrypted? (y/n) ", "blue")) == "y":
            cprint("[-] Restoring", "blue")
            shutil.unpack_archive(backup, dest, format="xztar")
        else:
            password = input(colored("Password: ", "blue"))
            cprint("[-] Restoring", "blue")
            shutil.copy(backup, "archon_restore_encrypted")
            pyAesCrypt.decryptFile(".\\archon_restore_encrypted",
                                   ".\\archon_restore_encrypted_d", passw=password, bufferSize=1024*64)
            shutil.unpack_archive(backup, dest, "xztar", format="xztar")
            os.remove("archon_restore_encrypted")
            destroy("archon_restore_encrypted_d")
        os.remove("temp/archon_restore_ftp")
        cprint("[*] Restored from backup", "green")
    elif sys.argv[1] == "history":
        print(colored("=>", "green")+"\tFolder => Backup Location")
        print(colored(":", "green")+"\tBackup name")
        print(colored("over", "green")+"\tProtocol name")
        data = open("backup.log", "r").read()
        for l in data.split("\n"):
            print(l.split(";")[0]+colored(" => ", "green")+l.split(";")[1]+colored(" : ", "green")+l.split(";")[2]+colored(" over ", "green")+l.split(";")[3])
except KeyboardInterrupt:
    try:
        if "Y" == input(colored("\nDo you want to cancel Archon? (Y/n) ", "red")):
            exit()
        else:
            pass
    except KeyboardInterrupt:
        exit()


if os.path.exists("temp/ftp_upload.tar.xz.e"):
    os.remove("temp/ftp_upload.tar.xz.e")
if os.path.exists("temp/ftp_upload.tar.xz"):
    os.remove("temp/ftp_upload.tar.xz")