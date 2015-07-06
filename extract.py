import record
import os
import subprocess

datapath='/home/gis-admin/modis/data/' #path to store the .tif files
tmppath='/home/gis-admin/modis/tmp/' #path to store the .vrt files
rawpath='/home/gis-admin/modis/raw/' #path to store downloaded files
libspath='/home/gis-admin/libs/'#path where the scripts are stored

'''
-----------------------------------------------------------------------------------------------------------------------------------
def juliandate(filename) : finds the juilan date. 'filename' should be the date.txt file ie; say 2000.02.18.txt

def get_name(filename,layers=0): this function returns the name of the file type supplied. When the 'filename' is '.txt' then it 					searches for files of the extension '.txt' and returns their name.
				When called with the layers specified, it returns the name of the layer corresponding to the subset

def getlayers(textfilename): finds all the layers the are in the .hdf files. 'textfilename' should be the date.txt file ie; say 
				2000.02.18.txt

-----------------------------------------------------------------------------------------------------------------------------------
'''

def juliandate(filename):#get the julian dates of the files
	try:
		read=record.create_dict(filename)
		for x in read:
			if 'h26v05' in x :
				jdate=x.split('.h26v05')[0].split('.')[1]
		return jdate
	except :
		print "extract.juliandate() : could not extract date"



def get_name(filename,layers=0):#find the name of the vrt files and text files as stored in the directory
	try:
		
		if layers!=0:
			os.chdir(rawpath)
			subset=filename
			vrts=layers
			#vrts=[x.split('days')[1].translate(None,'_') for x in layers ]
			vrtname=[vrts[i] for i in range(0,12) if subset[i]==1]
			return vrtname
				
		
		else :
			os.chdir(rawpath)
			text_name=subprocess.check_output('ls | grep '+filename,shell=True)
			text_name=text_name.translate(None,'\n')
			textname=text_name.replace(' ','_')
			os.rename(text_name,textname)
			return textname
		
	except (RuntimeError, TypeError, NameError,ValueError):
		print "extract.get_name(): can not find files with "+filename
		

def getlayers(textfilename):#gets the layers in the hdf file
	
	try:
		os.chdir(libspath)
		tiles=record.create_dict(textfilename)
		for x in tiles:
			if '.xml' not in x:
				hdffilename=x
		os.chdir(rawpath)
		sub=subprocess.check_output('gdalinfo '+hdffilename+'|grep  SUBDATASET*',shell=True)
		#split=[x for x in sub.split() if 'SUBDATASET' in x if 'NAME' in x]
		tmp=[x for x in sub.split('\n') if 'SUBDATASET' in x if 'NAME' in x]
		lay=[x[(x.rfind(':')+1):] for x in tmp]
		#lay=[tmp[i].split(split[i])[1] for i in range(0,len(tmp))]
		#if  len(split)!=len(lay):
		#	raise ValueError
		layers=[x.replace(' ','_') for x in lay] 
		return layers

	except ValueError:
		print "Check the code for extract.getlayers()"
		
	except:
		print "extract.getlayers(): could not get layer information"
		

