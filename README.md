SSH connection and aliases manager with curses and command line interface
======
sshch is released under DWTWL 2.55 license

sshch compatible with pyhon2 and python3, no additional libraries are required
### Screenshot
![sshch](https://raw.githubusercontent.com/zlaxy/sshch/master/sshch_screenshot.png)
### Installing
**You can install a release version from pip:**
```bash
pip install sshch
```
**Manual installation from the package or git repository also available:**
To install for all users:
```bash
sudo python setup.py install
```
To install just for current user:
```bash
mkdir ~/.local/bin
cp sshch/sshch ~/.local/bin/
```
### Using
To run curses interface:
```bash
sshch
```
To run command line help:
```bash
sshch -h
```
For exit from current ssh session press `Ctrl+D`.
**Additional Features**
- If you want to use unsafe 'password' feature you must install `sshpass` first.
- If you want to use bash autocompletion function with sshch, copy autocompletion script to /etc/bash_completion.d/:
```bash
sudo cp completion/sshch_bash_completion.sh /etc/bash_completion.d/sshch
```
(changes will come into effect with new bash session)
- If you want to use zsh autocompletion:
1) Place File in a Directory where ZSH can find it
     -> Search Path is Stored in $fpath
     -> echo $fpath
2) Rename File to '_sshch'
