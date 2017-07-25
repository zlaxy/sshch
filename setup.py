#!/usr/bin/env python

"""Setup script for sshch"""

def main():
    from distutils.core import setup

    setup(name='sshch',
          author='zlaxy',
          url='https://github.com/zlaxy/sshch/',
          description='Ssh connection manager',
          license='DWTWL 2.5',
          version='0.6',
          py_modules=['sshch'],
          scripts=['sshch/sshch'],

          # http://pypi.python.org/pypi?%3Aaction=list_classifiers
          classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Console :: Curses',
              'Intended Audience :: System Administrators',
              'License :: Freeware',
              'Natural Language :: English',
              'Operating System :: POSIX',
              'Programming Language :: Python :: 2.7',
              'Topic :: Internet',
              'Topic :: System :: Networking',
              'Topic :: System :: Systems Administration',
              'Topic :: Utilities'])

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
