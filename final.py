import pprint
import record

import os
import subprocess







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

	if 0!=subprocess.call('ls | grep OldDates.txt',shell=True):#file doesnot exist
		os.system("touch OldDates.txt")
		mod13q1=open("OldDates.txt","r+")
		write_record(mod13q1)
		mod13q1.close()
		old=create_dict("OldDates.txt")
		pprint.pprint(old,width=1)
		

	else:		
		old=create_dict("OldDates.txt")
		#print(old)		
		os.system("touch NewDates.txt")
		mod13q1_new=open("NewDates.txt","r+")
		write_record(mod13q1_new)
		mod13q1_new.close()
		new=create_dict("NewDates.txt")
		print(new)
		print(old)
		print new['2012.02.02']
		print old['2012.02.02']
		for i in new:
	     		if old[i]==new[i]:
	             		changed.append(i)
		#print changed

		
				
			
	
