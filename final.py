import pprint
import record

import os
import subprocess

a={}
updates=[]



def write_record(fileobject):
	try:
		b=record.create('')#creates record of MOD13Q1 home page
		#pprint.pprint(b, width=1)
		for data in b:
			fileobject.write(data)	
			fileobject.write("\t")	
			fileobject.write(b[data])
			fileobject.write("\n")
	except :
		print "Could not identify file object "+fileobject

def create_dict(filename):
	
	try:	
		
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
		print "Could not read the contents of "+filename


if __name__ == "__main__":
	if 0!=subprocess.call('ls | grep MOD13Q1.txt',shell=True):#file doesnot exist
		os.system("touch MOD13Q1.txt")
		mod13q1=open("MOD13Q1.txt","r+")
		write_record(mod13q1)
		mod13q1.close()
		create_dict("MOD13Q1.txt")
	else :
		os.system("touch MOD13Q1_new.txt")
		mod13q1_new=open("MOD13Q1_new.txt","r+")
		write_record(mod13q1_new)
		mod13q1_new.close()
		oldrecord=create_dict("MOD13Q1.txt")
		newrecord=create_dict("MOD13Q1_new.txt")
		#pprint.pprint(oldrecord,width=1)
		#pprint.pprint(newrecord,width=1)
		for i in newrecord:
			if oldrecord[i]!=newrecord[i]:
				updates.append(i)
		print updates
				
			
	
