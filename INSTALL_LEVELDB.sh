sudo cp ./leveldb/include/leveldb /usr/local/include -rf
sudo cp ./leveldb/out-shared/libleveldb.* /usr/local/lib  
# sudo vi /etc/ld.so.conf.d/usrlocallib.conf
# ## add below line:
# /usr/local/lib
sudo ldconfig
sudo pip install plyvel
