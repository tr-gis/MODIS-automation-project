import record
import os
import subprocess

datapath='/home/gis-admin/modis/data/' #path to store the .tif files
tmppath='/home/gis-admin/modis/tmp/' #path to store the .vrt files
rawpath='/home/gis-admin/modis/raw/' #path to store downloaded files
libspath='/home/gis-admin/libs/'#path where the scripts are stored

'''def move(subset,layers):
	#should read the .vrt name from lapers

'''

def juliandate(filename):
	try:
		read=record.create_dict(filename)
		for x in read:
			if 'h26v05' in x :
				jdate=x.split('.h26v05')[0].split('.')[1]
		return jdate
	except :
		print "extract.juliandate() : could not extract date"



def get_name(filename,layers=0):
	try:
		os.chdir(rawpath)
		if layers!=0:
			subset=filename
			vrts=[x.split('days')[1].translate(None,'_') for x in layers ]
			vrtname=[vrts[i] for i in range(0,12) if subset[i]==1]
			return vrtname
				
		
		else :
			text_name=subprocess.check_output('ls | grep '+filename,shell=True)
			text_name=text_name.translate(None,'\n')
			textname=text_name.translate(None,' ')
			os.rename(text_name,textname)
			return textname
		os.chdir(libspath)
	except (RuntimeError, TypeError, NameError,ValueError):
		print "extract.get_name(): can not find files with "+filename
		os.chdir(libspath)

def getlayers(textfilename):
	
	try:
		tiles=record.create_dict(textfilename)
		for x in tiles:
			if '.xml' not in x:
				hdffilename=x
		os.chdir(rawpath)
		sub=subprocess.check_output('gdalinfo '+hdffilename+'|grep  SUBDATASET*',shell=True)
		split=[x for x in sub.split() if 'SUBDATASET' in x if 'NAME' in x]
		tmp=[x for x in sub.split('\n') if 'SUBDATASET' in x if 'NAME' in x]
		lay=[tmp[i].split(split[i])[1] for i in range(0,len(tmp))]
		if  len(split)!=len(lay):
			raise ValueError
		layers=[x.replace(' ','_') for x in lay] 
		os.chdir(libspath)
		return layers

	except ValueError:
		print "Check the code for extract.getlayers()"
		os.chdir(libspath)
	except:
		print "extract.getlayers(): could not get layer information"
		os.chdir(libspath)

'''	
def finalname(layername,juliandate):
	os.system(mv tifffile/to/final/location)
	os.chdir(path/to/save/tifffile)
	convert julian date to standard
	newname='MOD13Q1'+layername+juliandate+standarddate.'tif'
	os.rename(source,newname)
'''	

