rpm -Uvh dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-*.rpm
sudo rpm -Uvh dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-*.rpm
yum -y install redis
systemctl start redis.service
systemctl enable redis.service
# edit /etc/redis.conf
# bind .0.0.0
