import json

def writeToJsonFile(path,filename,data):
	filePathNameWExt = './' + path + '/' + filename
	with open(filePathNameWExt, 'w') as fp:
		json.dump(data,fp)


#data = json.load(open('2017122521_nba-okc_BOX.json'))
 

#writeToJsonFile('./','dummy.json',data)
