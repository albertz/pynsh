#!/usr/bin/python





def mainloop():
	
	
	try:
		nextexecstep()
	except e:
		if have_lower_exc_handle(e):
			raise e
		else:
			yield_interactive()
			