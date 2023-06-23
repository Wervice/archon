import tkinter
from tkinter import *
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
from termcolor import cprint
import shutil
import pyAesCrypt
import os
import random
import ftplib

cprint("Archon Backup Utility GUI", "blue")

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

def fbackup():
    def show_success():
        mb.showinfo(title="Successfull", message="Finished backup successfully")
    def pick_folder():
        global dir 
        dir = fd.askdirectory()+"/"
        fbackup_picker_button.configure(background="#1fb521", activebackground="#047d18")
    def pick_dest():
        global destdir 
        destdir = fd.askdirectory()+"/"
        fbackup_picker_button_dest.configure(background="#1fb521", activebackground="#047d18")
    def start_backup():
        orig = dir
        dest = destdir
        dirname = backupname.get().replace(" ", "_")
        cprint("[-] Make compressed archive", "blue")
        shutil.make_archive(dest+dirname, "xztar", orig)
        if os.path.exists(dest+dirname+".tar.xz"):
            cprint("[*] Make compressed archive", "green")
        else:
                cprint("[x] Compression failed\nExiting now", "red")
                mb.showerror(title="Compression failed", message="The compression failed. Archon will close now.")
                exit()
        forig = os.path.abspath(orig)
        fdirn = dirname
        fdest = os.path.abspath(dest)
        open("backup.log", "a").write(str(forig)+";"+str(fdest)+";"+fdirn+";file\n")
        cprint("[*] Backup successfull", "green")
        show_success()
    def start_backup_e():
        orig = dir
        dest = destdir
        dirname = backupname.get().replace(" ", "_")
        encrypted = True
        if encrypted:
            password = sd.askstring(title="Enter encryption password", prompt="Enter password for encryption", show="*")
        if not encrypted:
            cprint("[-] Make compressed archive", "blue")
            shutil.make_archive(dest+dirname, "xztar", orig)
            if os.path.exists(dest+dirname+".tar.xz"):
                cprint("[*] Make compressed archive", "green")
            else:
                cprint("[x] Compression failed\nExiting now", "red")
                exit()
        else:
            cprint("[-] Make compressed archive", "blue")
            shutil.make_archive(dest+dirname, "xztar", orig)
            if os.path.exists(dest+dirname+".tar.xz"):
                cprint("[*] Make compressed archive", "green")
            else:
                cprint("[x] Compression failed\nExiting now", "red")
                mb.showerror(title="Compression failed", message="The compression failed. Archon will close now.")
                exit()
            cprint("[-] Encrypt archive", "blue")
            pyAesCrypt.encryptFile(
                dest+dirname+".tar.xz", dest+dirname+".tar.xz.e", passw=password, bufferSize=1024*64)
            if os.path.exists(dest+dirname+".tar.xz.e"):
                cprint("[*] Encrypt archive", "green")
            else:
                cprint("[x] Encryption failed\nExiting now", "red")
                mb.showerror(title="Encryption failed", message="The encryption failed. Archon will close now.")
                exit()
            destroy(dest+dirname+".tar.xz")
        forig = os.path.abspath(orig)
        fdirn = dirname
        fdest = os.path.abspath(dest)
        open("backup.log", "a").write(str(forig)+";"+str(fdest)+";"+fdirn+";file\n")
        cprint("[*] Backup successfull", "green")
        show_success()
    window.destroy()
    fbackup_window = Tk()
    global backupname 
    backupname = StringVar(master=fbackup_window)
    icon_picker = PhotoImage(file = os.path.abspath(r"assets/picker.png"))
    icon_lock = PhotoImage(file = os.path.abspath(r"assets/padlock.png"))
    icon_make = PhotoImage(file = os.path.abspath(r"assets/start.png"))
    fbackup_window.title("Folder Backup")
    fbackup_window.geometry("250x250")
    fbackup_window.configure(bg='white')
    fbackup_window.resizable(0,0)
    fbackup_picker_button = Button(master=fbackup_window, text="  Pick folder", command=pick_folder, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_picker)
    fbackup_picker_button.place(x=20, y=20)
    fbackup_picker_button_dest = Button(master=fbackup_window, text="  Pick destination", command=pick_dest, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_picker)
    fbackup_picker_button_dest.place(x=20, y=60)
    fbackup_entry_name = Entry(master=fbackup_window, border=1, borderwidth=1, background="white", textvariable=backupname)
    fbackup_entry_name.place(x=20, y=100)
    fbackup_button_make = Button(master=fbackup_window, text="  Start backup", command=start_backup, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_make)
    fbackup_button_make.place(x=20, y=140)
    Label(master=fbackup_window, text="Or", background="white").place(x=20, y=177)
    fbackup_button_make_enc = Button(master=fbackup_window, text="  Start encrypted backup", command=start_backup_e, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_lock)
    fbackup_button_make_enc.place(x=20, y=200)
    fbackup_window.mainloop()

def fbackupftp():
    def pick_folder():
        global dir 
        dir = fd.askdirectory()+"/"
        fbackup_picker_button.configure(background="#1fb521", activebackground="#047d18")
    def start_fbackupftp():
        orig = dir
        bname = backupname.get().replace(" ", "_")
        sdest = sd.askstring("Destination folder", prompt="Where do you want to store the backup?")
        dest = "temp/"
        dirname = "ftp_upload"
        encrypted = True
        hostname = sd.askstring(title="Hostname", prompt="Enter the hostname of the FTP server.")
        username = sd.askstring(title="Username", prompt="Enter the username to login at the FTP server.")
        lgpasswd = sd.askstring(title="Password", prompt="Enter the password to login at the FTP server.", show="*")
        tls = mb.askyesno("Use TLS?", message="Do you want to use FTP over TLS (FTPS)?")
        if not encrypted:
            cprint("[-] Make compressed archive", "blue")
            shutil.make_archive(dest+dirname, "xztar", orig)
            if os.path.exists(dest+dirname+".tar.xz"):
                cprint("[*] Make compressed archive", "green")
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
            mb.showerror(title="Failed", message="Login failed\nArchon will close now")
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
            mb.showerror(title="Failed", message="Unknown Error\nArchon will close now")
            exit()
        cprint("[*] Upload done", "green")
        cprint("[-] Close connection", "green")
        try:
            ftp.close()
        except ftplib.error_perm:
            cprint("[x] Error\nExiting now", "red")
            exit()
        cprint("[-] Overwriting data", "blue")
        try:
            destroy(dest+dirname+".tar.xz")
        except FileNotFoundError:
            cprint(
                "[x] Failed to destroy\nFile Not Found Error\nExiting now", "red")
            exit()
        open("backup.log", "a").write(
            "\n"+str(os.path.abspath(orig))+";"+str(hostname+"/"+sdest)+";"+str(bname)+";ftp")
        cprint("[*] Backup successfull", "green")
        forig = os.path.abspath(orig)
        fdirn = dirname
        fdest = os.path.abspath(dest)
        open("backup.log", "a").write(str(forig)+";"+str(fdest)+";"+fdirn+";file\n")
        mb.showinfo(title="Success", message="Backuped to server")
    def start_fbackupftp_e():
        orig = dir
        bname = backupname.get().replace(" ", "_")
        sdest = sd.askstring("Destination folder", prompt="Where do you want to store the backup?")
        dest = "temp/"
        dirname = "ftp_upload"
        encrypted = True
        hostname = sd.askstring(title="Hostname", prompt="Enter the hostname of the FTP server.")
        username = sd.askstring(title="Username", prompt="Enter the username to login at the FTP server.")
        lgpasswd = sd.askstring(title="Password", prompt="Enter the password to login at the FTP server.", show="*")
        tls = mb.askyesno("Use TLS?", message="Do you want to use FTP over TLS (FTPS)?")
        if encrypted:
            password = sd.askstring(title="Password", prompt="Enter password for encryption")
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
            mb.showerror(title="Failed", message="Login failed\nArchon will close now")
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
            mb.showerror(title="Failed", message="Unknown Error\nArchon will close now")
            exit()
        cprint("[*] Upload done", "green")
        cprint("[-] Close connection", "green")
        try:
            ftp.close()
        except ftplib.error_perm:
            cprint("[x] Error\nExiting now", "red")
            exit()
        if encrypted:
            if True:
                cprint("[-] Overwriting data", "blue")
                try:
                    destroy(dest+dirname+".tar.xz")
                except FileNotFoundError:
                    cprint(
                        "[x] Failed to destroy\nFile Not Found Error\nExiting now", "red")
                    exit()
            else:
                os.remove(dest+dirname+".tar.xz")
        forig = os.path.abspath(orig)
        fdirn = dirname
        fdest = os.path.abspath(dest)
        open("backup.log", "a").write(str(forig)+";"+str(fdest)+";"+fdirn+";file\n")
        cprint("[*] Backup successfull", "green")
        mb.showinfo(title="Success", message="Backuped to server")
    window.destroy()
    fbackup_windowftp = Tk()
    global backupname 
    backupname = StringVar(master=fbackup_windowftp)
    icon_picker = PhotoImage(file = os.path.abspath(r"assets/picker.png"))
    icon_lock = PhotoImage(file = os.path.abspath(r"assets/padlock.png"))
    icon_make = PhotoImage(file = os.path.abspath(r"assets/start.png"))
    fbackup_windowftp.title("Folder Backup FTP")
    fbackup_windowftp.geometry("250x250")
    fbackup_windowftp.configure(bg='white')
    fbackup_windowftp.resizable(0,0)
    fbackup_picker_button = Button(master=fbackup_windowftp, text="  Pick folder", command=pick_folder, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_picker)
    fbackup_picker_button.place(x=20, y=20)
    fbackup_entry_name = Entry(master=fbackup_windowftp, border=1, borderwidth=1, background="white", textvariable=backupname)
    fbackup_entry_name.place(x=20, y=100)
    fbackup_button_make = Button(master=fbackup_windowftp, text="  Start backup", command=start_fbackupftp, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_make)
    fbackup_button_make.place(x=20, y=140)
    Label(master=fbackup_windowftp, text="Or", background="white").place(x=20, y=177)
    fbackup_button_make_enc = Button(master=fbackup_windowftp, text="  Start encrypted backup", command=start_fbackupftp_e, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_lock)
    fbackup_button_make_enc.place(x=20, y=200)
    fbackup_windowftp.mainloop()

def frestore():
    def pick_folder():
        global dir 
        dir = fd.askdirectory()+"/"
        fbackup_picker_button.configure(background="#1fb521", activebackground="#047d18")
    def pick_bck():
        global bck 
        bck = fd.askopenfilename()
        fbackup_picker_button_dest.configure(background="#1fb521", activebackground="#047d18")
    def start_restore():
        cprint("[-] Restoring", "blue")
        shutil.unpack_archive(bck, dir, format="xztar")
        cprint("[*] Restored from backup", "green")
    def start_restore_d():
        cprint("[-] Restoring", "blue")
        shutil.copy(dir, "archon_restore_encrypted")
        pyAesCrypt.decryptFile(".\\archon_restore_encrypted",
                                ".\\archon_restore_encrypted_d", passw=sd.askstring(title="Encrypted backup", prompt="Enter password for decryption"), bufferSize=1024*64)
        shutil.unpack_archive(".\\archon_restore_encrypted_d", dir, "xztar")
        os.remove("archon_restore_encrypted")
        destroy("archon_restore_encrypted_d")
        cprint("[*] Restored from backup", "green")
    # Commands missing at all
    # Copy code from command-line version and paste it here
    # Edit the code
    # Check what we need from the GUI and what now
    window.destroy()
    frestore_window = Tk()
    global backupname 
    backupname = StringVar(master=frestore_window)
    icon_picker = PhotoImage(file = os.path.abspath(r"assets/picker.png"))
    icon_lock = PhotoImage(file = os.path.abspath(r"assets/padlock.png"))
    icon_make = PhotoImage(file = os.path.abspath(r"assets/start.png"))
    frestore_window.title("Folder Restore")
    frestore_window.geometry("250x250")
    frestore_window.configure(bg='white')
    frestore_window.resizable(0,0)
    fbackup_picker_button = Button(master=frestore_window, text="  Pick folder", command=pick_folder, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_picker)
    fbackup_picker_button.place(x=20, y=20)
    fbackup_picker_button_dest = Button(master=frestore_window, text="  Pick backup", command=pick_bck, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_picker)
    fbackup_picker_button_dest.place(x=20, y=60)
    fbackup_button_make = Button(master=frestore_window, text="  Start backup", command=start_restore, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_make)
    fbackup_button_make.place(x=20, y=140)
    Label(master=frestore_window, text="Or", background="white").place(x=20, y=177)
    fbackup_button_make_enc = Button(master=frestore_window, text="  Start & decrypt backup", command=start_restore_d, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_lock)
    fbackup_button_make_enc.place(x=20, y=200)
    frestore_window.mainloop()
def frestoreftp():
    def pick_folder():
        global dir 
        dir = fd.askdirectory()+"/"
        fbackup_picker_button.configure(background="#1fb521", activebackground="#047d18")
    def start_restore():
        hostname = sd.askstring(title="Hostname", prompt="Enter hostname to login to FTP server.")
        username = sd.askstring(title="Username", prompt="Enter username to login to FTP server.")
        lgpasswd = sd.askstring(title="Password", prompt="Enter password to login to FTP server.", show="*")
        tls = mb.askyesno(title="Use FTP over TLS?", message="Do you want to protect your FTP connection using TLS?")
        backups = sd.askstring(title="Backup Location", prompt="Where is the backup stored on you server?")
        backup = "temp/archon_restore_ftp"
        dest = dir
        if tls:
            ftp = ftplib.FTP_TLS(hostname)
        else:
            ftp = ftplib.FTP(hostname)
        cprint("[-] Connect to server", "blue")
        try:
            ftp.connect()
        except ftplib.error_perm:
            cprint("[x] Connection failed\nExiting now", "red")
            mb.showerror(title="FTP Error", message="FTP Connection failed. Archon will close now.")
            exit()
        cprint("[-] Login to server")
        try:
            ftp.login(username, lgpasswd)
        except ftplib.error_perm:
            cprint("[x] Login failed\nExiting now", "red")
            mb.showerror(title="FTP Error", message="FTP Login failed. Archon will close now.")
            exit()
        cprint("[-] Donwload backup from server", "blue")
        try:
            ftp.retrbinary("RETR %s" % (backups), open(backup, "wb").write)
        except ftplib.error_perm:
            cprint("[x] Download failed\nExiting now", "red")
            mb.showerror(title="FTP Error", message="FTP Download failed. Archon will close now.")
            exit()
        cprint("[-] Restoring", "blue")
        shutil.unpack_archive(backup, dest, format="xztar")
        os.remove("temp/archon_restore_ftp")
        cprint("[*] Restored from backup", "green")
    def start_restore_d():
        hostname = sd.askstring(title="Hostname", prompt="Enter hostname to login to FTP server.")
        username = sd.askstring(title="Username", prompt="Enter username to login to FTP server.")
        lgpasswd = sd.askstring(title="Password", prompt="Enter password to login to FTP server.", show="*")
        tls = mb.askyesno(title="Use FTP over TLS?", message="Do you want to protect your FTP connection using TLS?")
        backups = sd.askstring(title="Backup Location", prompt="Where is the backup stored on you server?")
        backup = "temp/archon_restore_ftp"
        dest = dir
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
        password = sd.askstring(title="Decryption password", prompt="Please enter the decryption password for your backup.", show="*")
        cprint("[-] Restoring", "blue")
        shutil.copy(backup, "archon_restore_encrypted")
        pyAesCrypt.decryptFile(".\\archon_restore_encrypted",
                                ".\\archon_restore_encrypted_d", passw=password, bufferSize=1024*64)
        shutil.unpack_archive(backup, dest, "xztar", format="xztar")
        os.remove("archon_restore_encrypted")
        destroy("archon_restore_encrypted_d")
        os.remove("temp/archon_restore_ftp")
        cprint("[*] Restored from backup", "green")
    window.destroy()
    frestoreftp_window = Tk()
    global backupname 
    backupname = StringVar(master=frestoreftp_window)
    icon_picker = PhotoImage(file = os.path.abspath(r"assets/picker.png"))
    icon_lock = PhotoImage(file = os.path.abspath(r"assets/padlock.png"))
    icon_make = PhotoImage(file = os.path.abspath(r"assets/start.png"))
    frestoreftp_window.title("Folder Restore FTP")
    frestoreftp_window.geometry("250x250")
    frestoreftp_window.configure(bg='white')
    frestoreftp_window.resizable(0,0)
    fbackup_picker_button = Button(master=frestoreftp_window, text="  Pick folder", command=pick_folder, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_picker)
    fbackup_picker_button.place(x=20, y=20)
    fbackup_button_make = Button(master=frestoreftp_window, text="  Start backup", command=start_restore, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_make)
    fbackup_button_make.place(x=20, y=140)
    Label(master=frestoreftp_window, text="Or", background="white").place(x=20, y=177)
    fbackup_button_make_enc = Button(master=frestoreftp_window, text="  Start & decrypt backup", command=start_restore_d, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_lock)
    fbackup_button_make_enc.place(x=20, y=200)
    frestoreftp_window.mainloop()
def history():
    os.system("open backup.log")

window = Tk()
window.resizable(0,0)
icon_backup = PhotoImage(file = os.path.abspath(r"assets/backup.png"))
icon_backupftp = PhotoImage(file = os.path.abspath(r"assets/ftp.png"))
icon_restore = PhotoImage(file = os.path.abspath(r"assets/restore.png"))
icon_restoreftp = PhotoImage(file = os.path.abspath(r"assets/ftprestore.png"))
icon_history = PhotoImage(file = os.path.abspath(r"assets/history.png"))
window.configure(bg='white')
window.title("Archon")
window.geometry("250x250")
fbackup_button = Button(master=window, text="  Folder Backup", command=fbackup, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_backup)
fbackup_button.place(x=20, y=20)
fbackup_button = Button(master=window, text="  Folder Backup FTP", command=fbackupftp, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_backupftp)
fbackup_button.place(x=20, y=60)
fbackup_button = Button(master=window, text="  Restore Folder", command=frestore, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_restore)
fbackup_button.place(x=20, y=100)
fbackup_button = Button(master=window, text="  Restore Folder FTP", command=frestoreftp, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_restoreftp)
fbackup_button.place(x=20, y=140)
fbackup_button = Button(master=window, text="  History", command=history, border=0, borderwidth=0, background="white", compound=LEFT, image = icon_history)
fbackup_button.place(x=20, y=180)
window.mainloop()