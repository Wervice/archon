# Archon Backup Utility
###### Keeps your data safe.
Archon is an open source and easy-to-use python backup utility for Linux. Archon supports compressed backups (`xztar`) and encryption using AES. You can also backup your files to a FTP server with and without TLS. Archon is licensed under GNUv3.
> __You can you the brand-new GUI now__
## How to use?
1. Open the folder where Archon is stored
2. Enter `python3 __main__.py <command>`
### Commands
|Name|Command|Details|
|--|--|--|
|Folder Backup|`fbackup`|Backup one folder as a compressed `xztar` archive|
|Folder Backup over FTP|`fbackupftp`|Backup one folder as a compressed `xztar` archive on a ftp server|
|Folder Restore|`frestoreftp`|Restore a folder from a backup|
|Folder Restore FTP|`frestoreftp`|Restore a folder from a backup stored on a FTP server.
|History|`history`|List every backup task and see, where a backup is stored|
#### Archon History
The Archon History command helps you finding backups for folders. The command `python3 __main__.py history` will show you a list of backups and backup locations.

This is an example history entry:
`C:\users\me\photos\ => Z:\backups\photos\ : familiy_photos.tar.xz over file`

`C:\users\me\photos\` is the backuped folder.  
`Z:\backups\photos\` is the backup destination folder.  
`family_photos.tar.xz` is the backup name.  
`file` is the protocol name.
## Used modules
`termcolor`: MIT License licensed python module for colored terminal outputs. You find the license text under `legal/termcolor.txt`  

`pyAesCrypt`: Apache License 2.0 licensed python module for Aes encryption. You find the license text under `legal/pyaescrypt.txt`
## Used files
Every Icon in Archon's GUI is by [Icons8](https://icons8.com).
