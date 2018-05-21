import json
file1 = open('data_file.json','w+')
reading = json.load(open('players.json'))
#filename = ['insert filenames here']


'''
f.write('data = {} \n')
f.write("data['key1']= [\n")
for i in range(1000):
	f.write('%d,\n' %i)
f.write("]") #\nprint data")
'''

'''
data = [1,2,3,4,5,6]
f.write(str(data))
'''


a = [1,2,3,4,5]
b = [6,7,8,9,0]

variables = {}
variables['a'] = a
variables['b'] = b

real_reading = reading['players']

# now we write the file
file1.write('{')
'''
for var in real_reading.keys():
	if var!=real_reading.keys()[-1]:
 
		name = str(var)
		print var
		file1.write("\"%s\":" % name)
		file1.write(str(real_reading[str(var)]))
		file1.write(',\n')

'''

for i in range(len(real_reading)):
#	print real_reading[i],i
	file1.write("%s, " % str(real_reading[i]))

file1.write('}')
