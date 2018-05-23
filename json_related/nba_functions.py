import numpy as np


def smoothing(a,n):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] /n



def velo(data,steps):
    
    for key in list(data.keys()):
        
        game = data[key]
        
        for team in ['awayplayers','homeplayers']:
            
            for player in list(data[key][team].keys()):

                x1,y1 = np.array(data[key][team][player]['x']), np.array(data[key][team][player]['y'])
                x,y = smoothing(x,5),smoothing(y,5)
                dx, dy = x[2:] - x[:-2], y[2:] - y[:-2]
                dist = np.sqrt(np.square(dx) + np.square(dy))
                velo = dist/0.08
                time = np.linspace(0,len(x1),len(x1))*0.04
                new_time = time[2:-2]
                velo_time = new_time[1:-1]
                data[key][team][player]['velo'] = velo
                data[key][team][player]['smoothX'] = x
                data[key][team][player]['smoothY'] = y
                data[key][team][player]['velotime'] = velo_time



#def kineticEnergy(data):
 #   for key in data.keys():
  #      game = data[key]
   #     for team in ['awayplayers','homeplayers']: 
		
#		return 2

def distance(xyz1, xyz2):

	delta = np.subtract(xyz1,xyz2)
	dist_squared = np.multiply(delta,delta)

	sum_dist_2 = sum(dist_squared)
	dist = np.sqrt(sum_dist_2) 
	
	return dist
	
	
# FUNCTION: Test if a player is on the court or not.
# This function will use the JSONL library to go through the 
# TRACKING files 
	
#	 We want to test if a player is on the court.  
#	 The best way to do this would be to implement a system where if the player is not on
#	 the court they are assigned a 'None' value, but would this interfere with the velocity function?
#	 Maybe we could import the data for whether or not they are on the court into a different parser,
#	 and then using JSON.load() to import the data and test it.  We could then close the data file as to not
# 	 take up a ton of memory space!
import jsonlines
import json
import numpy as np
from pprint import pprint

def court_bool(files_tracking,files_box_score):


    games = {}  # master dictionary

    # Open up the non-tracking files now

    gameFile = json.load(open('games.json'))
    playerFile = json.load(open('players.json'))


    for filename in files_tracking:

        ind = files_tracking.index(filename)
        box_score_filename = files_box_score[ind]
        box_score = json.load(open(box_score_filename))

        data = {}
        new_data = {}
        new_data['homeplayers'] = {}
        new_data['awayplayers'] = {}

        print('Reading in data from %s ...' % filename)

        with jsonlines.open(str(filename)) as f:
		
                new_data['gameclock'] = []
                new_data['period'] = []
                data['awayplayers'] = []
                data['homeplayers'] = []

                for line in f:

                        game_clock = line.get('gameClock')

                        new_data['gameclock'].append(game_clock)
                        new_data['period'].append(line.get('period'))

                        for i in range(0,len(line.get('awayPlayers'))):

                                data['awayplayers'].append(line.get('awayPlayers')[i])

                        for i in range(0,len(line.get('homePlayers'))):
                                data['homeplayers'].append(line.get('homePlayers')[i])

        print("Assigning data to players...")


        for i in range(0,len(data['awayplayers'])):

                away = data['awayplayers'][i]['playerId']

                if away not in list(new_data['awayplayers'].keys()):

                    new_data['awayplayers'][str(away)] = []

                period = new_data['period'][i/5]
                player_time = abs(new_data['gameclock'][i/5]-720.0)+ (period-1)*720.0
		
                new_data['awayplayers'][str(away)].append(player_time)


        playerFile = json.load(open('players.json'))
	
        for i in range(0,len(playerFile['players'])):

            player = playerFile['players'][i]
            playerId = player['id']

            if playerId in list(new_data['homeplayers'].keys()):
                name = str( player['firstName'] ) + str( player['lastName'] )
                new_data['homeplayers'][str(name)] = new_data['homeplayers'][playerId]
                del new_data['homeplayers'][playerId]
                new_data['homeplayers'][str(name)]['id']=playerId

            if playerId in list(new_data['awayplayers'].keys()):

                name = str(player['firstName'] ) + str( player['lastName'] )
                new_data['awayplayers'][str(name)] = new_data['awayplayers'][playerId]
                del new_data['awayplayers'][playerId]
		#new_data['awayplayers'][str(name)][u'id']=playerId



        return data, new_data
