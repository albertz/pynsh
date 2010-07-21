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
		p = asyncproc.Process([self.execPath] + list(args))
		return Pipes(i=p.stdin, out=p.stdout, err=p.stderr)

class Pipes:
	def __init__(self, **pipes):
		self.pipes = pipes

def loadExecDir(d):
	pass

def reloadExecDirs():
	for c in pynshOSExecs: del globals()[c]
	del pynshOSExecs[:]
	for d in PYNSH_OSEXEC_DIRS: loadExecDir(d)


class Const:
	def __init__(self, v=None): self.value = v
	def __call__(self, context): return self.value

class FuncCall:
	def __init__(self):
		self.func = None
		self.args = []
		self.kwargs = {}
	@classmethod
	def Simple(cls, func):
		c = cls()
		c.func = Const(func)
		return c
	def __call__(self, context):
		func = self.func(context)
		f_args = [a() for a in self.args]
		f_kwargs = dict( (a,self.kwargs[a]()) for a in self.kwargs )
		return func(*f_args, **f_kwargs)

class Assignment:
	def __init__(self):
		self.vartuple = None # tuple/tree of varnames
		self.expr = None # e.g. FuncCall
	def __call__(self, context):
		value = self.expr(context)
		return unpack(context, self.vartuple, value)
	@staticmethod
	def unpack(context, vartuple, value):
		var = None
		if type(vartuple) == string:
			var = vartuple
		if len(vartuple) == 1:
			var = vartuple[0]
		if var != None:
			context[var] = value
		else:
			if len(vartuple) != len(value):
				raise ValueError, "need " + str(len(value)) + " values to unpack, got " + str(len(vartuple))
			else:
				for i in xrange(0, len(value)):
					unpack(context, vartuple[i], value[i])	

class For:
	def __init__(self):
		self.code = Code()
		self.vartuple = None
		self.expr = None
	def __call__(self, context):
		ret = None
		iter = self.expr(context)
		iter = iter.__iter__()
		while True:
			try: next = iter.next()
			except StopIteration: break
			Assignment.unpack(context, self.vartuple, next)
			ret = self.code(context)
		return ret

class While:
	def __init__(self):
		self.code = Code()
		self.expr = None
	def __call__(self, context):
		ret = None
		while self.expr(context):
			ret = self.code(context)
		return ret
	
class Function:
	def __init__(self):
		self.args = [] # list of varnames
		self.defaultArgValues = {} # varname -> obj
		self.variadicArgs = None # None or varname
		self.variadicKArgs = None # None or varname
		self.code = Code()
		self.vars = [] # list of varnames
		
	def __call__(self, *args, **kwargs):		
		funcname = self.__name__ + "()"
		f_kwargs = {}
		f_more_args = []
		f_more_kwargs = {}
		
		for i in xrange(0, len(args)):
			if i < len(self.args):
				if not self.args[i] in f_kwargs:
					f_kwargs[self.args[i]] = args[i]
				else:
					raise TypeError, funcname + " got multiple values for keyword argument '" + self.args[i] + "'"
			else:
				if not self.variadicArgs:
					raise TypeError, funcname + " takes at most " + str(len(self.args)) + " arguments (" + str(len(args)) + " given)"					
				f_more_args = args[i:]
				break
		
		for a in kwargs:
			if not a in f_kwargs:
				if a in self.args:
					f_kwargs[a] = kwargs[a]
				else:
					f_more_kwargs[a] = kwargs[a]
			else:
				raise TypeError, funcname + " got multiple values for keyword argument '" + self.args[i] + "'"

		if len(f_more_kwargs) > 0 and not self.variadicKArgs:
			raise TypeError, funcname + ": unknown parameters " + repr(f_more_kwargs)				
		
		if len(f_kwargs) < len(self.args):
			raise TypeError, funcname + " takes at least " + str(len(self.args)) + " arguments (" + str(len(f_kwargs)) + " given)"					

		context = f_kwargs.copy()
		if self.variadicArgs: context[self.variadicArgs] = f_more_args
		if self.variadicKArgs: context[self.variadicKArgs] = f_more_kwargs
		
		return self.code(context)

class NoOp: # alias 'pass'
	def __call__(self, context): pass

class Code:
	def __init__(self):
		self.cmds = None # iterable of commands (which have __call__(self, context))
	def __call__(self, context):
		ret = None
		for cmd in self.cmds:
			try:
				ret = cmd(context)
			except Exception as e:
				print e
		return ret

def locals():
	return {}

globalsCall = FuncCall.Simple(globals)

