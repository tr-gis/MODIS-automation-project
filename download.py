import os
import subprocess
import record
from termcolor import colored

os.system('touch completed.txt')#add checking for existence of file

record.write('dates.txt')
dates=record.create_dict('dates.txt')
completed=record.create_dict('completed.txt')

newdates=[x for x in dates if x not in completed]
#print newdates

for date in newdates:
	try:
		print date
		if 0!=subprocess.call('modis_download.py -f '+date+' -O -t h27v08,h27v07,h26v08,h26v07,h26v06,h26v05,h25v08,h25v07,h25v06,h25v05,h24v07,h24v06,h24v05,h23v05,h23v06,h27v06,h24v08,h22v05 -p MOD13Q1.005 /home/gis-admin/data',shell=True):#1
			print colored('Could not download tiles for '+date,'red')
			exit()
		else:
			print colored('Tiles downloaded successfully for'+date,'green')
		record.write(date+'.txt',date)
		record.completed(date)
	except:
		print 'Not Done'
