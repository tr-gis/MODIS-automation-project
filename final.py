import pprint
import record

import os
import subprocess





def write_record(filename):
	b=record.create('')#creates record of MOD13Q1 home page
	#pprint.pprint(b, width=1)
	for data in b:
		filename.write(data)	
		filename.write("\t")	
		filename.write(b[data])
		filename.write("\n")

if __name__=='__main__ ':
	if 0!=subprocess.call('ls | grep MOD13Q1*',shell=True):
		os.system("touch MOD13Q1.txt")
		mod13q1=open("MOD13Q1.txt","r+")
		write_record(mod13q1)
		mod13q1.close()
	else :
		os.system("touch MOD13Q1_new.txt")
		mod13q1_new=open("MOD13Q1.txt_new","r+")
		write_record(mod13q1_new)
		mod13q1_new.close()

	
