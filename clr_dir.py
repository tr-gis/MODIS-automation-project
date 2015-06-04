import os
f=os.listdir(os.getcwd())
for file in f:
	if file=='auto.py':
		f.remove('auto.py')
for files in f:
	os.remove(files)

