#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from os import path
from sys import argv
from optparse import OptionParser
from getpass import getpass
from curses import textpad, panel
from math import *
import ConfigParser
import subprocess
import base64
import curses

# https://github.com/zlaxy/sshch
version="0.3"
# path to conf file, default: ~/.config/sshch.conf
conf_file = path.expanduser("~") + '/.config/sshch.conf'

help_screen = (" Press:\n  'z'/'x' or arrows - navigation\n  'a' - " +
               "add new alias\n  'e' - edit existing alias\n  'p' - " +
               "set alias's password for sshpass [UNSAFE]\n  " +
               "'space' - select\n  'r' - remove selected alias/" +
               "aliases\n  'c' - execute specific command with " +
               "selected alias/aliases\n  'enter' - connect to " +
               "selected alias/aliases\n  'q' - quit\n Run sshch " +
               "with '--help' option to view command line help.\n " +
               "Also, you can edit config file manually:\n  " +
               conf_file)

def AddNewAlias(alias):
    if not conf.has_section(alias):
        conf.add_section(alias)
        conf.write(open(conf_file, "w"))
        return 1
    else:
        return "error: '" + alias + "' already exists"

def SetAliasString(alias, string):
    conf.set(alias, "exec_string", string)
    conf.write(open(conf_file, "w"))

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

def SetPassword(alias, string):
    string = base64.b64encode(base64.b16encode(
                              base64.b32encode(string)))
    conf.set(alias, "password", string)
    conf.write(open(conf_file, "w"))

def Password(alias):
    if conf.has_section(alias):
        promptpass = ("[UNSAFE] Enter password for sshpass: ")
        string = ""
        while string == "":
            string = getpass (promptpass)
        string = base64.b64encode(base64.b16encode(
                                  base64.b32encode(string)))
        conf.set(alias, "password", string)
        conf.write(open(conf_file, "w"))
    else:
        print "error: '" + alias + "' alias is not exists."

def RemoveAliases(aliases):
    for alias in aliases:
        conf.remove_section(alias)
        conf.write(open(conf_file, "w"))

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

def ConnectAlias(alias, command=False):
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

def CursesConnect(aliases, command=False):
    for alias in aliases:
        curses.endwin()
        print "Connecting to " + alias + "..."
        ConnectAlias(alias, command)
        print "... " + alias + " finished."
    exit()

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
              " --edit=newremoteserver -p newremoteserver\n  " +
              progname + ' -c "ls -l" newremoteserver\n  ' + progname +
              " -c reboot existingalias newremoteserver\n" +
              "Examples of connection string:\n  " +
              "ssh user@somehost.com\n  " +
              "ssh gates@8.8.8.8 -p 667\n  " +
              "ssh root@somehost.com -t tmux a\n" +
              "Also, you can edit config file manually: " +
              conf_file + "\n")
    opts = FormatedParser(usage=usage, version="%prog " + version,
                          epilog=epilog)
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

def TextBoxConfirm(value):
    if value == 10:
        value = 7
    return value
    
def Panel(screen, h, w, y, x, text, text_colorpair=0, deco_colorpair=0,
          confirm=0):
    new_window = curses.newwin(h, w, y, x)
    new_window.erase()
    new_window.attron(deco_colorpair)
    new_window.box()
    new_window.attroff(deco_colorpair)
    sub_window = new_window.subwin(h - 2, w - 2 , y + 1 , x + 1 )
    sub_window.addstr(0, 0, text)
    panel = curses.panel.new_panel(new_window)
    curses.panel.update_panels()
    screen.refresh()
    if confirm == "password":
        hidden_password = ""
        keych = ""
        position = 2
        while 1:
            keych = screen.getch()
            if keych == ord("\n"):
                break
            if keych == 27:
                hidden_password = ""
                break
            if keych == curses.KEY_BACKSPACE:
                if position > 2:
                    sub_window.addstr(1, position - 1, " ",
                                      text_colorpair)
                    sub_window.refresh()
                    position = position - 1
                    hidden_password = hidden_password[0:-1]
            else:
                hidden_password += curses.keyname(keych)
                sub_window.addstr(1, position, "*", text_colorpair)
                position += 1
                sub_window.refresh()
        return hidden_password
    elif confirm == "remove":
        keych = screen.getch()
        if keych == ord("y") or keych == ord("Y"):
            return "confirm"
        return False
    else:
        screen.getch()

def TextBox(screen, h, w, y, x, title="", value="", text_colorpair=0,
            deco_colorpair=0):
    new_window = curses.newwin(h + 3, w + 2, y - 1, x - 1)
    title_window = new_window.subwin(1, w , y , x)
    title_window.addstr(0, 0, title, text_colorpair)
    title_window.refresh()
    sub_window = new_window.subwin(h, w, y + 1, x)
    textbox_field = textpad.Textbox(sub_window, insert_mode=True)
    new_window.attron(deco_colorpair)
    new_window.box()
    new_window.attroff(deco_colorpair)
    new_window.refresh()
    sub_window.addstr(0, 0 , value, text_colorpair)
    sub_window.attron(text_colorpair)
    return textbox_field
    
def CursesExit(screen):
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    exit()

# curses template from: https://stackoverflow.com/a/30828805/6224462
def MainScreen():
    strings = conf.sections()
    row_num = len(strings)
    selected_strings = [" " for i in range(0, row_num + 1)]
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    screen.keypad(1)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    highlight_text = curses.color_pair(1)
    normal_text = curses.A_NORMAL
    height, width = screen.getmaxyx()
    screen.border(0)
    curses.curs_set(0)
    max_row = height - 5
    screen.addstr(1, 2, "sshch " + version + ", press 'h' for help")
    box = curses.newwin(max_row + 2, width - 2, 2, 1)
    box.box()
    pages = int(ceil(row_num / max_row))
    position = 1
    page = 1
    for i in range(1, max_row + 1):
        if row_num == 0:
            box.addstr(1, 1, "There aren't any aliases yet. Press 'a'" +
                       " to add new one.", highlight_text)
        else:
            if (i == position):
                box.addnstr(i, 2, "[" + selected_strings[i] + "] " +
                            str(i) + " " + strings[i - 1] + " (" +
                            conf.get(strings[i - 1], "exec_string") +
                            ")", width - 6, highlight_text)
            else:
                box.addnstr(i, 2, "[" + selected_strings[i] + "] " +
                            str(i) + " " + strings[i - 1] + " (" +
                            conf.get(strings[i - 1], "exec_string") +
                            ")", width - 6, normal_text)
            if i == row_num:
                break
    screen.refresh()
    box.refresh()
    key_pressed = screen.getch()
    while 1:
        if key_pressed == ord('q') or key_pressed == ord(
                              'Q') or key_pressed == 27:
            CursesExit(screen)
        if key_pressed == ord('h') or key_pressed == ord(
                              'H') or key_pressed == 265:
            Panel(screen, height - 4, width - 6, 2, 3, help_screen,
                  normal_text, highlight_text)
        if key_pressed == ord('a') or key_pressed == ord('A'):
            newalias = TextBox(screen, 1, width - 8, (height // 2) - 1,
                               4, "Enter new alias:", "", normal_text,
                               highlight_text)
            addalias = newalias.edit(TextBoxConfirm)
            if not addalias.rstrip() == "":
                addresult = AddNewAlias(addalias.rstrip())
                if not addresult == 1: Panel(screen, 3, width - 6,
                                             (height // 2) - 1, 3,
                                             addresult, normal_text,
                                             highlight_text)
                else:
                    addstr = ""
                    while addstr.rstrip() == "":
                        newstr = TextBox(screen, 3, width - 8,
                                         (height // 2) - 1, 4,
                                         "Enter full execution string:",
                                         "ssh ", normal_text,
                                         highlight_text)
                        addstr = newstr.edit(TextBoxConfirm)
                    SetAliasString(addalias.rstrip(), addstr.rstrip())
                    strings = conf.sections()
                    row_num = len(strings)
                    selected_strings.append(" ")
                    pages = int(ceil(row_num / max_row))
                    box.refresh()
        if key_pressed == ord('e') or key_pressed == ord('E'):
            editstr = ""
            while editstr.rstrip() == "":
                newstr = TextBox(screen, 3, width - 8,
                                 (height // 2) - 1, 4,
                                 "Enter new execution string:",
                                 conf.get(strings[position - 1],
                                          "exec_string"),
                                 normal_text, highlight_text)
                editstr = newstr.edit(TextBoxConfirm)
            SetAliasString(strings[position - 1], editstr.rstrip())
            strings = conf.sections()
        if key_pressed == ord('p') or key_pressed == ord('P'):
            password = ""
            password = Panel(screen, 4, width - 6, (height // 2) - 1, 3,
                             " Enter user password for sshpass and " +
                             "press 'enter':\n>", normal_text,
                             highlight_text, "password")
            if not password == "":
                SetPassword(strings[position - 1], password)
        if key_pressed == ord('r') or key_pressed == ord('R'):
            selected = []
            for i in range(1, row_num + 1):
                if selected_strings[i] == "*":
                    selected.append(strings[i - 1])
            if len(selected) > 0:
                remove_confirm = ("Are you sure to remove " +
                                 str(len(selected)) +
                                 " selected aliases? (y/N)")
            else:
                remove_confirm = ("Are you sure to remove '" +
                                 strings[position - 1] +
                                 "' alias? (y/N)")
                selected.append(strings[position - 1])
            remove = Panel(screen, 4, width - 6, (height // 2) - 1, 3,
                           remove_confirm, normal_text, highlight_text,
                           "remove")
            if remove == "confirm":
                RemoveAliases(selected)	
                strings = conf.sections()
                row_num = len(strings)
                selected_strings = [" " for i in range(0, row_num + 1)]
                pages = int(ceil(row_num / max_row))
                position = 1
                page = 1
                box.refresh()
        if key_pressed == ord('c') or key_pressed == ord('C'):
            selected = []
            for i in range(1, row_num + 1):
                if selected_strings[i] == "*":
                    selected.append(strings[i - 1])
            if not len(selected) > 0:
                selected.append(strings[position - 1])
            newcstr = TextBox(screen, 3, width - 8,
                              (height // 2) - 1, 4,
                              "Enter specific command to execute with" +
                              " selected alias/aliases:", "",
                              normal_text, highlight_text)
            cstr = newcstr.edit(TextBoxConfirm)
            CursesConnect(selected, cstr.rstrip())
        if key_pressed == curses.KEY_DOWN or key_pressed == ord(
                                     'x') or key_pressed == ord('X'):
            if page == 1:
                if position < i:
                    position = position + 1
                else:
                    if pages > 1:
                        page = page + 1
                        position = 1 + (max_row * (page - 1))
            elif page == pages:
                if position < row_num:
                    position = position + 1
            else:
                if position < max_row + (max_row * (page - 1)):
                    position = position + 1
                else:
                    page = page + 1
                    position = 1 + (max_row * (page - 1))
        if key_pressed == curses.KEY_UP or key_pressed == ord(
                                   'z') or key_pressed == ord('Z'):
            if page == 1:
                if position > 1:
                    position = position - 1
            else:
                if position > (1 + (max_row * (page - 1))):
                    position = position - 1
                else:
                    page = page - 1
                    position = max_row + (max_row * (page - 1))
        if key_pressed == curses.KEY_LEFT or (key_pressed == 
                          curses.KEY_PPAGE):
            if page > 1:
                page = page - 1
                position = 1 + (max_row * (page - 1))
    
        if key_pressed == curses.KEY_RIGHT or (key_pressed ==
                          curses.KEY_NPAGE):
            if page < pages:
                page = page + 1
                position = (1 + (max_row * (page - 1)))
        if key_pressed == ord("\n") and row_num != 0:
            selected = []
            for i in range(1, row_num + 1):
                if selected_strings[i] == "*":
                    selected.append(strings[i - 1])
            if not len(selected) > 0:
                selected.append(strings[position - 1])
            CursesConnect(selected)
        if key_pressed == 32:
            if selected_strings[position] == ' ':
                selected_strings[position] = '*'
            else: selected_strings[position] = ' '
        box.erase()
        screen.border(0)
        box.border(0)
        for i in range(1 + (max_row * (page - 1)), max_row + 1 +
                       (max_row * (page - 1))):
            if row_num == 0:
                box.addstr(1, 1, "There aren't any aliases yet. Press" +
                           " 'a' to add new one.", highlight_text)
            else:
                if (i + (max_row * (page - 1)) == (position +
                    (max_row * (page - 1)))):
                    box.addnstr(i - (max_row * (page - 1)), 2, "[" +
                                selected_strings[i] + "] " + str(i) +
                                " " + strings[i - 1] + " (" +
                                conf.get(strings[i - 1],
                                "exec_string") + ")", width - 6,
                                highlight_text)
                else:
                    box.addnstr(i - (max_row * (page - 1)), 2, "[" +
                                selected_strings[i] + "] " + str(i) +
                                " " + strings[i - 1] + " (" +
                                conf.get(strings[i - 1],
                                "exec_string") + ")", width - 6,
                                normal_text)
                if i == row_num:
                    break
        screen.refresh()
        box.refresh()
        key_pressed = screen.getch()    
    CursesExit(screen)

if __name__ == "__main__":
    conf = ConfigParser.RawConfigParser()
    if not path.exists(conf_file):
        open(conf_file, 'w')
    conf.read(conf_file)
    if len(argv) > 1:
        Options()
    else:
       	MainScreen()
