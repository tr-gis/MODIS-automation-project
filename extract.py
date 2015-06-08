import record

def juliandate(filename):
	try:
		read=record.create_dict(filename)
		for x in read:
			if 'h26v05' in x :
				jdate=x.split('.h26v05')[0].split('.')[1]
		return jdate
	except :
		print "extract.juliandate() : could not extract date"
