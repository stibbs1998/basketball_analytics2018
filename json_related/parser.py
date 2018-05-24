import jsonlines
import json
import numpy as np
from pprint import pprint



def sorting(files_tracking, files_box_score):  # take in a LIST of MULTIPLE files
    
    games = {}  # master dictionary
    
    # Open up the non-tracking files now
    
    gameFile = json.load(open('tracking_box_hackathon/games.json'))
    playerFile = json.load(open('tracking_box_hackathon/players.json'))
    
    
    for filename in files_tracking:
        
        ind = files_tracking.index(filename)
        box_score_filename = files_box_score[ind]
        box_score = json.load(open(box_score_filename))
    
        data = {}
        new_data = {}
        new_data['awayplayers'] = {}
        new_data['homeplayers'] = {}

        print('Reading in data from  %s ...' % filename)

        with jsonlines.open(str(filename)) as f:

            data['awayplayers'] = []
            data['homeplayers'] = []
            new_data['period'] = []
            new_data['ball_xyz'] = []
            #new_data['wallclock'] = []
            new_data['gameclock'] = []
            new_data['on_court'] = []

            for line in f:
                
            # get data for clocks and the basketaball
                
                game_clock = line.get('gameClock')
                new_data['on_court'].append(line.get('gameClockStopped'))
                new_data['gameclock'].append(game_clock)
                new_data['period'].append(line.get('period'))
                new_data['ball_xyz'].append(line.get('ball'))
                #new_data['wallclock'].append(line.get('wallClock'))

                # We use temporary lists for the home/away teams so we can
                # first extract the data, and then sort it by player_ids

               
                for i in range(0,len(line.get('awayPlayers'))):


                    data['awayplayers'].append(line.get('awayPlayers')[i])
                 
               
                for i in range(0,len(line.get('homePlayers'))):
                    
                    data['homeplayers'].append(line.get('homePlayers')[i])
                
            

        print('Assigining data to players...')
        
        # this sorts the players from their temporary list to the game list
        # adds their xyz components, and a time indexer (still in progress)

        for i in range(0,len(data['awayplayers'])):


            away = data['awayplayers'][i]['playerId']
            
            if away not in list(new_data['awayplayers'].keys()):

                new_data['awayplayers'][str(away)] = {}
                new_data['awayplayers'][str(away)]['xyz'] = []
                new_data['awayplayers'][str(away)]['on_court'] = []

            time_in_out = new_data['on_court'][int(i/5)]

            period = new_data['period'][int(i/5)]
#            player_time = abs(new_data['gameclock'][int(i/5)]-720.0)+ (period-1)*720.0

            new_data['awayplayers'][str(away)]['on_court'].append(time_in_out)

            player_away = data['awayplayers'][i]['xyz']
            
            if len(player_away) < 3 or time_in_out == True:
                player_away = [np.NaN,np.NaN,np.NaN]
                
            new_data['awayplayers'][str(away)]['xyz'].append(player_away)

            
        for i in range(0,len(data['homeplayers'])):
            
            home = data['homeplayers'][i]['playerId']

            
            if home not in list(new_data['homeplayers'].keys()):

                new_data['homeplayers'][str(home)] = {}
                new_data['homeplayers'][str(home)]['xyz'] = []
                new_data['homeplayers'][str(home)]['on_court'] = []
		
            time_in_out = new_data['on_court'][int(i/5)]

            period = new_data['period'][int(i/5)]
#            player_time = abs(new_data['gameclock'][int(i/5)]-720.0)+ (period-1)*720.0

            new_data['awayplayers'][str(away)]['on_court'].append(time_in_out)

    
            player_home = data['homeplayers'][i]['xyz']
 
            
            # there are some points where the camera doesn't pick up a player's coordinates
            # in this case, we are just going to assume that their coordinates are (0,0,0)
    
           
            if len(player_home) < 3 or time_in_out == True:
                player_home = [np.NaN,np.NaN,np.NaN]

           
            new_data['homeplayers'][str(home)]['xyz'].append(player_home)
            


   

        print('organizing xyz and time data...')
    
        # similar to taking the transpose of a Matrix, this switches the data from ~100,000 [x,y,z]
        # points per player to 3 arrays, 'x','y','z' that are of length of ~ 100,000

        for key in list(new_data['awayplayers'].keys()):


            xyz = new_data['awayplayers'][str(key)]['xyz']

            zipped_xyz = list(zip(*xyz))
            new_data['awayplayers'][str(key)]['x'], new_data['awayplayers'][str(key)]['y'], new_data['awayplayers'][str(key)]['z'] = zipped_xyz
           
        for key in list(new_data['homeplayers'].keys()):

            xyz = new_data['homeplayers'][str(key)]['xyz']
            
            zipped_xyz = list(zip(*xyz))
            new_data['homeplayers'][str(key)]['x'], new_data['homeplayers'][str(key)]['y'], new_data['homeplayers'][str(key)]['z'] = zipped_xyz
       
       
       
        xyz = new_data['ball_xyz']
        new_data['ballXyz'] = {}



        for i in range(0,len(xyz)):

            if len(xyz[i]) < 3:
                xyz[i] = xyz[i-1]

        zipped_xyz = list(zip(*xyz))
        new_data['ballXyz']['x'], new_data['ballXyz']['y'], new_data['ballXyz']['z'] = zipped_xyz
 
        # maps player names from their ids, renames their keys as their names for readability sake
        # and then stores their id as a seperate key in case it is needed later on

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
                new_data['awayplayers'][str(name)]['id']=playerId



        


        # attaches all game stats to each player
        # and then stores team stats seperately
        new_data['gameclock'] = list(np.add( abs(np.subtract(new_data['gameclock'],720.0)) , (np.subtract(new_data['period'], 1)*720.0) )) 
	
	
        new_data['gameStatus'] = box_score['game-state']

        new_data['teamStats'] = {}


        for team in ['homeplayers','awayplayers']:

            for key1 in list(new_data[team].keys()):

                new_data[team][key1]['stats'] = {}


                
                for key2 in list(box_score.keys()):

                    player_ID = str(new_data[team][key1]['id'])

                    if type(box_score[key2]) == list and 'player_id' in list(box_score[key2][0].keys()):

                        for i in range(0, len( box_score[key2] ) ):

                            if box_score[key2][i]['player_id'] == player_ID:

                                new_data[team][key1]['stats'][key2] = box_score[key2][i]

                    else:


                        new_data['teamStats'][key2] = box_score[key2]


        print('Done with game %d !' % files_tracking.index(filename))

        
        # After finally finishing this, we find the date of the game played and append this 
        # as a key into the games dictionary
       

        for i in range(0,len(gameFile['games'])):

            if gameFile['games'][i]['id'] == new_data['gameStatus']['game_id']:

                date = gameFile['games'][i]['path']

                games[str(date)] = new_data


    return games






# Warriors

# Rockets

def player_masses(games, team_weights):
    
    
    csv_data = np.loadtxt(str(team_weights),delimiter=',',dtype=str,skiprows=1,unpack=True)
    last_names = csv_data[0]
    first_names = csv_data[1]
    player_weights = player_info[5]
   
    for game in games:
        for i in range(0,len(last_names)):
            full = str(first_names[i][1:-1] + last_names[i][1:])
            player_information['names'].append(full)
            if full in list(warriors_data[game]['homeplayers'].keys()):
                warriors_data[game]['homeplayers'][full]['mass'] = float(player_weights[i][0:3])
