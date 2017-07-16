#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from sys import argv
from optparse import OptionParser
from getpass import getpass
import ConfigParser
import subprocess
import base64

# https://github.com/zlaxy/sshch
version="%prog 0.2"
# path to conf file, default: ~/.config/sshch.conf
conf_file = path.expanduser("~") + '/.config/sshch.conf'

def Add(alias):
    if not conf.has_section(alias):
        conf.add_section(alias)
        promptadd = ("Enter connection string for new alias " +
                     "(example: ssh user@somehost.com):\n")
        string = ""
        while string == "":
            string = raw_input (promptadd)
        conf.set(alias, "exec_string", string)
        conf.write(open(conf_file, "w"))
    else:
        print "error: '" + alias + "' already exists."

def Edit(alias):
    if conf.has_section(alias):
        promptedit = ("Enter connection string for existing alias " +
                      "(example: ssh user@somehost.com):\n")
        string = ""
        while string == "":
            string = raw_input (promptedit)
        conf.set(alias, "exec_string", string)
        conf.write(open(conf_file, "w"))
    else:
        print "error: '" + alias + "' alias is not exists."

def List(option, opt, value, parser):
    print ' '.join(str(p) for p in conf.sections())

def Password(alias):
    if conf.has_section(alias):
        promptpass = ("[UNSAFE] Enter password for sshpass: ")
        string = ""
        while string == "":
            string = getpass (promptpass)
        string = base64.b64encode(base64.b16encode(base64.b32encode(string)))
        conf.set(alias, "password", string)
        conf.write(open(conf_file, "w"))
    else:
        print "error: '" + alias + "' alias is not exists."

def Remove(alias):
    if conf.has_section(alias):
        promptremove = ("Type 'yes' if you sure to remove " +
                        alias + " alias: ")
        string = raw_input (promptremove)
        if string == "yes":
            conf.remove_section(alias)
            conf.write(open(conf_file, "w"))
        else:
            print "'" + alias + "' alias was not deleted."
    else:
        print "error: '" + alias + "' alias is not exists."

def Connect(aliases, command):
    for alias in aliases:
        if conf.has_section(alias):
            exec_string = ""
            if conf.has_option(alias, "password"):
                password = base64.b32decode(base64.b16decode(
                    base64.b64decode(conf.get(alias, "password"))))
                exec_string = "sshpass -p " + password + " "
            exec_string = exec_string + conf.get(alias, "exec_string")
            if command:
                exec_string = exec_string + " " + command
            p = subprocess.Popen(exec_string, shell=True)
            streamdata = p.communicate()[0]
        else:
            print "error: '" + alias + "' alias is not exists."

def Options():
    class FormatedParser(OptionParser):
        def format_epilog(self, formatter):
            return self.epilog

    usage = "usage: %prog [options] [aliases]"
    progname = path.basename(__file__)
    epilog = ("Examples:\n  " + progname + " existingalias\n  " +
              progname + " -a newremoteserver\n  " + progname +
              " --edit=newremoteserver -p newremoteserver\n  " + progname +
              ' -c "ls -l" newremoteserver\n  ' + progname +
              " -c reboot existingalias newremoteserver\n" +
              "Examples of connection string:\n  " +
              "ssh user@somehost.com\n  " +
              "ssh gates@8.8.8.8 -p 667\n  " +
              "ssh root@somehost.com -t tmux a\n" +
              "Also, you can edit config file manually: " +
              conf_file + "\n")
    opts = FormatedParser(usage=usage, version=version, epilog=epilog)
    opts.add_option('-l', '--list', action = "callback", callback=List,
                    help="show list of all existing aliases")
    opts.add_option('-a', '--add', action="store",
                    type="string", dest="add",
                    metavar="alias", default=False,
                    help="add new alias for connection string")
    opts.add_option('-c', '--command', action="store",
                    type="string", dest="command",
                    metavar="command", default=False,
                    help="add command for executing alias")
    opts.add_option('-e', '--edit', action="store",
                    type="string", dest='edit',
                    metavar="alias", default=False,
                    help="edit existing connection string")
    opts.add_option('-p', '--password', action="store",
                    type="string", dest='password',
                    metavar="alias", default=False,
                    help="set and store password for sshpass [UNSAFE]")
    opts.add_option('-r', '--remove', action="store",
                    type="string", dest='remove',
                    metavar="alias", default=False,
                    help="remove existing alias of connection string")

    options, alias = opts.parse_args()
    if options.add:
        Add(options.add)
    if options.edit:
        Edit(options.edit)
    if options.password:
        Password(options.password)
    if options.remove:
        Remove(options.remove)
    if alias:
        Connect(alias, options.command)

conf = ConfigParser.RawConfigParser()
if not path.exists(conf_file):
    open(conf_file, 'w')
conf.read(conf_file)

Options()