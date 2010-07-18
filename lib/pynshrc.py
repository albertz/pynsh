#!/usr/bin/python

import os, subprocess
import asyncproc

PYNSH_OSEXEC_DIRS = os.getenv("PATH").split(":")
pynshOSExecs = []

class OSExec:
	def __init__(self, execPath):
		self.execPath = execPath
		
	def __call__(self, *args, **kwargs):
		#p = subprocess.Popen([self.execPath] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		p = asyncproc.Popen([self.execPath] + args)


def loadExecDir(d):
	pass

def reloadExecDirs():
	for c in pynshOSExecs: del globals()[c]
	del pynshOSExecs[:]
	for d in PYNSH_OSEXEC_DIRS: loadExecDir(d)
