#GENERAL INFORMATON :
#the script has been written to download the MOD13Q1.005 product by default form http://e4ftl01.cr.usgs.gov/
#*******************************************************************************************************************************
#How to edit : 

#For the syntax of arguments to the scripts visit pymodis webpage

#1 Tiles and Date :

#to change the tiles and date, edit the line marked 1 on the rightside
#to change mosaik output folder and mosaic type, edit line marked 2 on the rightside
#*******************************************************************************************************************************

#2 Output path, filename  and format :

#to change the ouput folder of the downloads,mosaic and converted files replace /home/gis-admin/data with the desired path
#to change converted file name and location, edit line marked 3 on the rightside
#*******************************************************************************************************************************

#3 SpectralLayer selections :

#the spectral selection (ie;the -s options in the script calls) depends on the modis product
#for example the MOD13Q1 product has 12 layers and hence the -s string should have 12 characters of 1's and 0's
#here we are downloading the first two layers ie;NDVI and EVI
#to find the number of layers  https://lpdaac.usgs.gov/ -> data products -> modis -> modis product tables -> select_product ->layers
#*******************************************************************************************************************************

#code starts here :

import os
from termcolor import colored
import name
import subprocess

subprocess.call('clear',shell=True)

print colored('Downloading Tiles','white')

if 0!=subprocess.call('modis_download.py -f 2012-12-05 -O -t h27v08,h27v07,h26v08,h26v07,h26v06,h26v05,h25v08,h25v07,h25v06,h25v05,h24v07,h24v06,h24v05,h23v05,h23v06,h27v06,h24v08,h22v05 -p MOD13Q1.005 /home/gis-admin/data',shell=True):#1
	print colored('Download of tiles unsuccessful','red')
	exit()
else:
	print colored('Tiles downloaded successfully','green')


textname=name.get_name("*.txt")

#format of -s 'NDVI EVDI ......'

mosaic_call='modis_mosaic.py -s "1 1 0 0" -o /home/gis-admin/data/mosaik -v /home/gis-admin/data/'+textname #2

	     

if 0!=subprocess.call(mosaic_call,shell=True):
	print colored('Possible Cause - Please make sure that auto.py is in the same directory as the .hdf files','red')
	exit()
else:
	print colored('Tiles have been mosaiced','green')


eviname=name.get_name("*EVI.vrt")
ndviname=name.get_name("*NDVI.vrt")


convert_call_ndvi='modis_convert.py -v -s "( 1 )" -o /home/gis-admin/data/final_NDVI -e 4326 /home/gis-admin/data/'+ndviname #3
                 

#convert_call_evi='modis_convert.py -v -s "( 0 1 )" -o /home/gis-admin/data/final_EVI -e 4326 /home/gis-admin/data/'+eviname #3
'''
if 0!=subprocess.call(convert_call_evi,shell=True):
	print colored('EVI Conversion Failed','red')
	exit()
else:
	print colored('EVI conversion complete','green')
'''
if 0!=subprocess.call(convert_call_ndvi,shell=True):
	print colored('NDVI Conversion Failed','red')
	exit()
else:
	print colored('NDVI conversion complete','green')

print colored('Exiting auto.py','magenta') 
exit()
