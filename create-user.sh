#!/bin/bash

set -e

user=$1
password=$2

/usr/bin/sudo /bin/dd if=/dev/zero of=/$user bs=1024 count=1M
/usr/bin/sudo /sbin/mkfs.ext4 /$user

/usr/bin/sudo /bin/mkdir -p /sambashares/$user

/usr/bin/sudo /bin/mount /$user /sambashares/$user

/usr/bin/sudo /bin/echo "/$user /sambashares/$user ext4 defaults 0 0" | /usr/bin/sudo /usr/bin/tee -a /etc/fstab

/usr/bin/sudo /usr/sbin/useradd $user

/usr/bin/sudo /bin/echo -e "$password\n$password\n" | /usr/bin/sudo /usr/bin/passwd $user
(/usr/bin/sudo /bin/echo $password; /usr/bin/sudo /bin/echo $password) | /usr/bin/sudo /usr/bin/smbpasswd -a $user

#passwd $user
#smbpasswd -a $user
#chown -R $user /sambashares/$user
/usr/bin/sudo /bin/chown -R $user:www-data /sambashares/$user
/usr/bin/sudo /bin/chmod -R 777 /sambashares/$user

/usr/bin/sudo /bin/cp /etc/samba/smb.conf /etc/samba/smb.conf_$(/bin/date +%Y-%m-%d_%H:%M:%S)

/usr/bin/sudo /bin/echo "[$user]
path = /sambashares/$user
valid users = $user
browseable = yes
writable = yes
public = no
guest ok = no
create mask = 0644
directory mask = 0777
read only = no" |  /usr/bin/sudo /usr/bin/tee -a /etc/samba/smb.conf

/usr/bin/sudo /bin/systemctl restart smbd