import os
import subprocess

def get_name(filename):
	try:
		if filename=="*EVI.vrt":
			evi_name=subprocess.check_output('ls | grep *EVI.vrt',shell=True)
			evi_name=evi_name.translate(None,'\n')
			eviname=evi_name.translate(None,' ')
			os.rename(evi_name,eviname)
			return eviname
		elif filename=="*NDVI.vrt":
			ndvi_name=subprocess.check_output('ls | grep *NDVI.vrt',shell=True)
			ndvi_name=ndvi_name.translate(None,'\n')
			ndviname=ndvi_name.translate(None,' ')
			os.rename(ndvi_name,ndviname)
			return ndviname
		elif filename=="*.txt":
			text_name=subprocess.check_output('ls | grep *.txt',shell=True)
			text_name=text_name.translate(None,'\n')
			textname=text_name.translate(None,' ')
			os.rename(text_name,textname)
			return textname
	except (RuntimeError, TypeError, NameError,ValueError):
		print "can only accept *EVI.vrt or *NDVI.vrt or *.txt"
