#!/usr/bin/env python

"""Setup script for sshch"""

def main():
    from distutils.core import setup

    setup(name='sshch',
          author='zlaxy',
          author_email='zlaxyi@gmail.com',
          url='https://github.com/zlaxy/sshch/',
          description='Ssh connection and aliases manager',
          long_description='SSH connection and aliases manager with curses and command line interface',
          long_description_content_type='text/x-rst',
          license='DWTWL 2.55',
          version='1.0',
          py_modules=['sshch'],
          scripts=['sshch/sshch'],
          keywords='sshch ssh aliases manager',
          python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',

          # http://pypi.python.org/pypi?%3Aaction=list_classifiers
          classifiers=[
              'Development Status :: 5 - Production/Stable',
              'Environment :: Console :: Curses',
              'Intended Audience :: System Administrators',
              'License :: Freeware',
              'Natural Language :: English',
              'Operating System :: POSIX',
              'Programming Language :: Python',
              'Topic :: Internet',
              'Topic :: System :: Networking',
              'Topic :: System :: Systems Administration',
              'Topic :: Utilities'])

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
