yum install mysql
yum install mysql-server
yum install mysql-client
# please edit, datadir to /home/mysql 
# and disable selinux
# NOTE: dont chage *.sock file location
# [root@centos ~]# vi /etc/sysconfig/selinux　←　SELinux設定ファイル編集
# SELINUX=enforcing
mysql_secure_installation
# set passwored "1234"

# create "kindle" database
mysql -u root -p
#enter << 1234
