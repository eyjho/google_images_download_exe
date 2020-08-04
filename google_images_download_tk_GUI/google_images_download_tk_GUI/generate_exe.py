#!/usr/bin/env python
# coding: utf-8

'''
Use subprocess to create executable out of main script
'''
import subprocess
import PyInstaller


subprocess.call(r'pyinstaller main.py --name "Semiotics Engine" --exclude-module numpy --exclude-module cryptography')