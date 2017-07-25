SSH connection manager with curses interface
======
sshch is released under DWTWL 2.5 license
![sshch](https://raw.githubusercontent.com/zlaxy/sshch/master/sshch_screenshot.png)
### Installing
To install for all users:
```
sudo python setup.py install
```
To install just for current user:
```
mkdir ~/.local/bin
cp sshch/sshch ~/.local/bin/
```
### Using
To run curses interface:
```
sshch
```
To run command line help:
```
sshch -h
```
**If you want to use unsafe 'password' feature you must install 'sshpass' first.**