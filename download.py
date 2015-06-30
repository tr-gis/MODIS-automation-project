#!/usr/bin/python

import os
import subprocess
import record
from termcolor import colored
import extract

productname='MOD13Q1.005'
subset=[1,1]
tiles=' h27v08,h27v07,h26v08,h26v07,h26v06,h26v05,h25v08,h25v07,h25v06,h25v05,h24v07,h24v06,h24v05,h23v05,h23v06,h27v06,h24v08,h22v05 '

datapath='/home/gis-admin/modis/data/' #path to store the .tif files
tmppath='/home/gis-admin/modis/tmp/' #path to store the .vrt files
rawpath='/home/gis-admin/modis/raw/' #path to store downloaded files
libspath='/home/gis-admin/libs/'#path where the scripts are stored

os.system('touch completed.txt')
record.write('dates.txt')
dates=record.create_dict('dates.txt')
completed=record.create_dict('completed.txt')

newdates=[x for x in dates if x not in completed]
#print newdates
print 'Number of new downloads %d '%len(newdates)

for date in newdates:
	#print date
	
	try:#download the .hdf and .xml files	
		print date
		subprocess.call('modis_download.py -f '+date+' -O -p '+productname+' -t '+tiles+rawpath,shell=True)#1
		print colored('Tiles downloaded successfully for '+date,'green')
		record.write(date+'.txt',date)#contains list of .hdf and .xml files downloaded on the 'date'
		record.completed(date)#add the downloaded date to completed list
	except:
		print 'Download of tiles for '+date+' failed'
	
	try:#mosaicks the files
		
		z=len(subset)
		Layers=extract.getlayers(date+'.txt')#returns a list of layers in the product
		for i in range(0,len(Layers)-z):
			subset.append(0)
		
		textname=extract.get_name("*.txt")
		#modis_mosaic.py -s "1" -o /tmp/mosaik -v /tmp/listfileMOD11A1.005.txt
		mosaic_call='modis_mosaic.py -s "1 1 0 0" -o '+rawpath+' -v '+rawpath+textname #2
		subprocess.call(mosaic_call,shell=True)
		for x in os.listdir(rawpath):
			if x.endswith('.vrt'):
				n=x.replace(' ','_')
				os.rename(x,n)
		print colored('Tiles mosaicked successfully for '+date,'green')
					
	except:
		print 'Could not mosaic tiles for '+date

	
	try:#converts into tif files
		vrtfiles=extract.get_name(subset,Layers)#returns the layers corresponding to the subset
		julian=extract.juliandate(date+'.txt')		
		for x in vrtfiles:
			vrtfile=extract.get_name(x+'.vrt')
			convert_call='modis_convert.py -v -s "( 1 )" -o '+datapath+date+'final -e 4326 '+rawpath+vrtfile
			subprocess.call(convert_call,shell=True)
			subprocess.call('mv '+datapath+date+'final.tif'+' '+datapath+productname+'-'+x+'-'+julian+'-'+date+'.tif',shell=True)
			subprocess.call('mv '+rawpath+vrtfile+' '+tmppath,shell=True)
		print colored('.tif file conversion successful for '+date,'green')		
		
	except:
		print colored('.tif file conversion for '+date+' failed','red')
	

	try:#creates a .xml file for the mosicked file
		rec=record.create_dict(date+'.txt')
		parse_call='modis_multiparse.py -w new.xml'
		for x in rec:
			if '.xml' not in x:
				parse_call=parse_call+' '+x
		os.chdir(rawpath)
		subprocess.call(parse_call,shell=True)
		os.chdir(libspath)
		subprocess.call('mv '+rawpath+'new.xml'+' '+datapath+productname+'-'+julian+'-'+date+'.xml',shell=True)
		print colored('xml file for mosaic of '+date+' created','green')
	except:
		print colored('xml file for mosaic of '+date+' could NOT BE created','red')		
		
	record.completed(date)
	#exit()				
