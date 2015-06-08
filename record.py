from lxml import html
import pprint
import requests
import os
import subprocess
from collections import OrderedDict


tiles=['h27v08','h27v07','h26v08','h26v07','h26v06','h26v05','h25v08','h25v07','h25v06','h25v05','h24v07','h24v06','h24v05','h23v05','h23v06 h27v06','h24v08','h22v05']

'''
----------------------------------------------------------------------------------------------------------------------------------
This file contains the following functions :

def create(datetodownload): This funtion creates a dictionary that contains the scrapped contents of the MODIS webpage
			It can be used in two ways:
			1) When the argument is '' then it scraps the MOD13Q1 homepage and returns a dictionary containing 
			directory names and last modified date 
				ARGUMENTS : datetodownload in quotes ie;'2000.02.18'


def write(filename,date=''): This function writes the information form the above fucntion into a text file and save it. It stores 
			information for the tiles in the tiles list defined at the beginnig of the script
				ARGUMENTS : filename in quotes ie;'2000.02.18.txt', date in quotes ie;'2000.02.18'
					by default the date is '' to write infomation about MOD13Q1 homepage

def create_dict(filename): This function reads the contents of the text file created in the above function and puts the content 			in to a dictionay. 
				ARGUMENTS : filename should be in quotes ie;'2000.02.12.txt'


def juliandate(filename): This function extracts the julian date from the contents in the text files above. 					ie;'MOD13Q1.A2000049.h22v05.005.2006270085040.hdf', it returns 'A2000049'
				ARGUMENTS : filename should be in quotes ie;'2000.02.12.txt'


def listfile(date): This function creates a list file with name = datedate+'_MOD13Q1.txt' which is used by the "modis_download.py"
				ARGUMENTS : date should be in quotes ie;'2000.02.12'

def completed(date): This function writes the dates downloaded to completed.txt
			ARGUMENT : date in qoutes ie; '2000.02.18'
----------------------------------------------------------------------------------------------------------------------------------	
'''




def create(datetodownload):
	try:
		rec={}
		if datetodownload=='':
			page = requests.get('http://e4ftl01.cr.usgs.gov/MOLT/MOD13Q1.005/')
		else :
			page = requests.get('http://e4ftl01.cr.usgs.gov/MOLT/MOD13Q1.005/'+datetodownload+'/')
		tree = html.fromstring(page.text)
		mod_date = tree.xpath('//pre/text()')
		t=[x for x in mod_date if x.count('-')>1]
		m=[x.lstrip() for x in t ]
		p=[x.translate(None,'\n') for x in m ]
		mod=[x.split(' ')[0] for x in p]		
		#print mod
		content=tree.xpath('//a/text()')
		tmp=[x.translate(None,'/') for x in content]
		prod=[x for x in tmp if (x.translate(None,' ')).isalpha()==False]
		#print prod
		if len(mod)!=len(prod):
			raise "Len Error"
		if len(prod)==0|len(mod)==0:
			raise ValueError
		for i in range(0,len(prod)):
			rec[prod[i]]=mod[i]
		record=OrderedDict(sorted(rec.items(), key=lambda t: t[0]))

		#pprint.pprint(record, width=1)

		return record
	except "Len Error":
		print "record.create() :The lengths of lists donot match !! Correct the code"
	except ValueError:
		print "record.create():Is the date valid ?"
	except:
		print "record.create() : Could not create record"


def write(filename,date=''):
	try:
		if date=='':
			
			if 0!=subprocess.call('ls | grep '+filename,shell=True):#file doesnot exist
				os.system("touch "+filename)
				fileobject=open(filename,"r+")
				b=create('')#creates record of MOD13Q1 home page
				#pprint.pprint(b, width=1)
				for data in b:
					fileobject.write(data)	
					fileobject.write("\n")	
				fileobject.close()
			else:#file exits so delete it and create new file
				os.system('rm '+filename)
				os.system("touch "+filename)
				fileobject=open(filename,"r+")
				b=create('')#creates record of MOD13Q1 home page
				#pprint.pprint(b, width=1)
				for data in b:
					fileobject.write(data)	
					fileobject.write("\n")	
				fileobject.close()
			
		else :
			if 0!=subprocess.call('ls | grep '+filename,shell=True):#file doesnot exist
				os.system("touch "+filename)
				fileobject=open(filename,"r+")			
				b=create(date)#creates record of the given date directory in MOD13Q1 
				#pprint.pprint(b, width=1)
				for data in b:
					if '.jpg' not in data:
						for x in tiles:
							if x in data:
								fileobject.write(data)	
								fileobject.write("\t")	
								fileobject.write(b[data])
								fileobject.write("\n")	
				fileobject.close()

	except :
		print "record.write() : Could not write record into "+filename



def create_dict(filename):
	
	try:	
		a={}
		text=open(filename,"r")
		text.seek(0,0)
		line=text.readlines()
		for i in range(0,len(line)):
			line[i]=line[i].translate(None,'\n')
			content=line[i].partition("\t")#splits the line at the tab character
			a[content[0]]=content[2]
		#pprint.pprint(a,width=1)
		text.close()
		return a
	except:
		print "record.create_dict(): Could not read the contents of "+filename


def listfile(date):
	try:
		if 0!=subprocess.call('ls | grep '+date+'_MOD13Q1.txt',shell=True):#file doesnot exist
			os.system("touch "+date+'_MOD13Q1.txt')
			fileobject=open(date+'_MOD13Q1.txt',"r+")
			b=create(date)#creates record of MOD13Q1 home page
			#pprint.pprint(b, width=1)
			for data in b:
				if '.jpg' not in data:
					for x in tiles:
						if x in data:
							fileobject.write(data)	
							fileobject.write("\n")
			fileobject.close()
		
		
	except :
		print "record.listfile() : Could not write tiles info into "+date+'_MOD13Q1.txt'


def juliandate(filename):
	try:
		read=record.create_dict(filename)
		for x in read:
			if 'h26v05' in x :
				jdate=x.split('.h26v05')[0].split('.')[1]
		return jdate
	except :
		print "extract.juliandate() : could not extract date"



def completed(date):
	try:
		if 0!=subprocess.call('ls | grep completed.txt',shell=True):#file doesnot exist
			os.system("touch completed.txt")
			fileobject=open('completed.txt',"r+")	
			fileobject.write(date)
			fileobject.write('\n')
			fileobject.close()
		else:
		
			fileobject=open('completed.txt',"r+")	
			fileobject.write(date)
			fileobject.write('\n')
			fileobject.close()
	except:
		print "record.completed(): Could not write contents to completed.txt"
	



