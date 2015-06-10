import os
import subprocess
import record
from termcolor import colored
import extract


datapath='/home/gis-admin/modis/data/' #path to store the .tif files
tmppath='/home/gis-admin/modis/tmp/' #path to store the .vrt files
rawpath='/home/gis-admin/modis/raw/' #path to store downloaded files


os.system('touch completed.txt')
record.write('dates.txt')
dates=record.create_dict('dates.txt')
completed=record.create_dict('completed.txt')

newdates=[x for x in dates if x not in completed]
#print newdates
print 'Number of new downloads %d '%len(newdates)

for date in newdates:
	try:
		print date
		subprocess.call('modis_download.py -f '+date+' -O -t h27v08,h27v07,h26v08,h26v07,h26v06,h26v05,h25v08,h25v07,h25v06,h25v05,h24v07,h24v06,h24v05,h23v05,h23v06,h27v06,h24v08,h22v05 -p MOD13Q1.005 '+rawpath,shell=True)#1
		print colored('Tiles downloaded successfully for '+date,'green')
		record.write(date+'.txt',date)#contains list of .hdf and .xml files downloaded on the 'date'
		record.completed(date)#add the downloaded date to completed list
	except:
		print 'Download of tiles for '+date+' failed'

	try:
		subset=[1,1]
		z=len(subset)
		Layers=extract.getlayers(date+'.txt')#returns a list of layers in the product
		for i in range(0,len(Layers)-z):
			subset.append(0)
		
		textname=extract.get_name("*.txt")
		mosaic_call='modis_mosaic.py -s "1 1 0 0" -o '+rawpath+'mosaick '+rawpath+textname #2
		subprocess.call(mosaic_call,shell=True)
		print colored('Tiles mosaicked successfully for '+date,'green')
					
	except:
		print 'Could not mosaic tiles for '+date

'''	try:
		vrtfiles=extract.get_name(subset,Layers)#returns the layers corresponding to the subset
		for x in vrtfiles:
			vrtfile=extract.get_name(x+'.vrt')
			convert_call='modis_convert.py -v -s "( 1 1 )" -o '+datapath+'final -e 4326 '+rawpath+'+vrtfile
			subprocess.call(convert_call,shell=True)
			subprocess.call('mv '+rawpath+vrtfile+' '+tmppath,shell=True)
	except:
		print "Conversion of files for "+date+' failed'
				
'''
