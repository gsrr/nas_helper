import traceback
import sys
import os
import subprocess

def [module_name]_lib_test(HAServer, paraList):
    paras = {}
    ret = HAServer.setConfig("[module_name_upper]Config", "config_test", paras)
    HAServer.log(1, "[[module_name]lib]%s"%str(ret))  
    return {'status' : 0 , 'data' : "call lib successfully:%s"%str(ret)}
    
def [module_name]lib(HAServer, paraList):
	try:
		op = paraList['op']
		func = getattr(sys.modules[__name__], op)
		return func(HAServer, paraList)
	except:
		return {'status' : -999, 'exception' : traceback.format_exc()}

if __name__ == "__main__":
	try:
		sys.path.append("/usr/local/NAS/misc/HAAgent")
		from NASHAComm import *
		HA = NASHAComm("127.0.0.1")
		func = getattr(sys.modules[__name__], sys.argv[1])	
		func(HA)
	except:
		pass
	finally:
		HA.closeSocket()
		
