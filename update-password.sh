#!/bin/bash

set -e

user=$1
password=$2

(/usr/bin/sudo /bin/echo $password; /usr/bin/sudo /bin/echo $password) | /usr/bin/sudo /usr/bin/smbpasswd -a $user
/usr/bin/sudo /bin/systemctl restart smbd