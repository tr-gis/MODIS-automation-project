from lxml import html
import pprint
import requests




def create(datetodownload):
	date=[]
	record={}
	if datetodownload=='':
		page = requests.get('http://e4ftl01.cr.usgs.gov/MOLT/MOD13Q1.005/')
	else :
		page = requests.get('http://e4ftl01.cr.usgs.gov/MOLT/MOD13Q1.005/'+datetodownload+'/')
	tree = html.fromstring(page.text)
	modified = tree.xpath('//pre/text()')
	for i in range(0,len(modified)):
		if i>4:
			modified[i]=modified[i].lstrip()
			date_time=modified[i].partition(' ')
			modified[i]=date_time[0]
			date.append(modified[i])
			
	
	name=tree.xpath('//a/text()')
	for i in range(0,len(name)):
		name[i]=name[i].translate(None,'/')

	for i in range(0,len(date)):
		record[name[i+5]]=date[i]
	#pprint.pprint(record, width=1)
	return record

	

