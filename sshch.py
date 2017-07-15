#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from sys import argv
import ConfigParser
import subprocess
import base64

conf_file = path.expanduser("~") + '/.config/sshch.conf'

conf = ConfigParser.RawConfigParser()
if not path.exists(conf_file):
  open(conf_file, 'w')
conf.read(conf_file)
if conf.has_section(argv[-1]):
  exec_string = ""
  if conf.has_option(argv[-1], "pass"):
    password = base64.b64decode(conf.get(argv[-1], "pass"))
    exec_string = "sshpass -p " + password + " "
  exec_string = exec_string + conf.get(argv[-1], "exec_string")
  p = subprocess.Popen(exec_string, shell=True, stderr=subprocess.PIPE, )
  streamdata = p.communicate()[0]
else:
  print "There is no '" + argv[-1] + "' section in config file"
