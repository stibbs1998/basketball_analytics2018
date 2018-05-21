import numpy as np

def velo(data,steps):
    
    for key in list(data.keys()):
        
        game = data[key]
        
        for team in ['awayplayers','homeplayers']:
            
            for player in list(data[key][team].keys()):
                
                x, y = data[key][team][player]['x'], data[key][team][player]['y']
                x2, y2 = np.multiply(x,x) , np.multiply(y,y)
                dist = np.add(x2,y2)
                R = np.sqrt(dist)
                time = np.linspace(0, len(R), len(R))
                t = np.multiply(time,0.04)
                
                R1, R2 = R[1:], R[:-1]
                t1, t2 = t[1:], t[:-1]
                
                delta_t,delta_R = np.subtract(t1,t2), np.subtract(R1,R2)
                velocity = abs(np.divide(delta_R,delta_t))
                
                for i in range(0,len(velocity)):

                    if velocity[i] >= 40:
                        velocity[i] = velocity[i-1]
                        
                       
                for i in range(0,steps):
                    
                    v1,v2 = velocity[1:],velocity[:-1]
                    v_sum = np.add(v1,v2)
                    
                    
                    velocity = np.divide(v_sum,2)

                
                data[key][team][player]['velo'] = velocity
                data[key][team][player]['avg_velo'] = np.average(velocity)


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
