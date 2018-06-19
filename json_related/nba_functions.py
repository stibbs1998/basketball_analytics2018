import numpy as np


def smoothing(a,n):
    ret = np.nancumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    final = ret[n-1:]/n
    for i in range(len(final)):

        if np.any(np.isnan(np.array(a[i:i+n]))):
            final[i] = np.nan
    return final



def positional_smoothing(data):
        for game in data.keys():
            for team in ['homeplayers','awayplayers']:
                for key in data[game][team].keys():
                    data[game][team][key]['SmoothXYZ'] = {}

                    x =  smoothing(data[game][team][key]['x'], 5) 
                    y =  smoothing(data[game][team][key]['y'], 5) 
                    z =  smoothing(data[game][team][key]['z'], 5) 


                     

#                    x = x.astype('float')
#                    y = y.astype('float')
#                    z = z.astype('float')
#
#
#                    x[x==0] = np.NaN
#                    y[y==0] = np.NaN
#                    z[z==0] = np.NaN






                    data[game][team][key]['SmoothXYZ']['x'] = x 
                    data[game][team][key]['SmoothXYZ']['y'] = y
                    data[game][team][key]['SmoothXYZ']['z'] = z

def velo_accel_smoothing(data):

    for game in data.keys():

        for team in ['homeplayers','awayplayers']:

            for key in data[game][team].keys():
                x = data[game][team][key]['SmoothXYZ']['x']
                y = data[game][team][key]['SmoothXYZ']['y']
                dx = np.array(x[2:]) - np.array(x[:-2])
                dy = np.array(y[2:]) - np.array(y[:-2])
               # dist = np.sqrt(np.square(dx)+np.square(dy))
                dist = np.array((dx,dy))
                velo = dist/0.08
                mag_velo = np.sqrt(np.square(velo[0])+np.square(velo[1]))
                data[game][team][key]['smooth_velo'] = velo
                data[game][team][key]['smooth_velo_mag'] = mag_velo
                dvx = velo[0][2:]-velo[0][:-2]
                dvy = velo[1][2:]-velo[1][:-2]
                dv = np.array((dvx,dvy))
                accel = dv/0.08
                acc_mag = np.sqrt(np.square(accel[0])+np.square(accel[1]))
                data[game][team][key]['smooth_accel_mag'] = acc_mag
                data[game][team][key]['smooth_accel'] = accel



def velo_accel(data):

    for game in data.keys():

        for team in ['homeplayers','awayplayers']:

            for key in data[game][team].keys():
                x = data[game][team][key]['x']
                y = data[game][team][key]['y']
                dx = np.array(x[2:]) - np.array(x[:-2])
                dy = np.array(y[2:]) - np.array(y[:-2])
               # dist = np.sqrt(np.square(dx)+np.square(dy))
                dist = np.array((dx,dy))
                velo = dist/0.08
                mag_velo = np.sqrt(np.square(velo[0])+np.square(velo[1]))
                data[game][team][key]['velo'] = velo
                data[game][team][key]['velo_mag'] = mag_velo
                dvx = velo[0][2:]-velo[0][:-2]
                dvy = velo[1][2:]-velo[1][:-2]
                dv = np.array((dvx,dvy))
                accel = dv/0.08
                acc_mag = np.sqrt(np.square(accel[0])+np.square(accel[1]))
                data[game][team][key]['accel_mag'] = acc_mag
                data[game][team][key]['accel'] = accel


   

def smooth_energy(data):

    for game in data.keys():

        for team in ['homeplayers','awayplayers']:

            for key in data[game][team].keys():

                x = data[game][team][key]['SmoothXYZ']['x']
                y  = data[game][team][key]['SmoothXYZ']['y']
                dx =np.array(x[2:]-x[:-2])
                dy =np.array(y[2:]-y[:-2])
                dist = np.array((dx,dy))
                velo = dist/0.08*0.3048 # conversion from ft/s to m/s
                dvx = velo[0][2:] - velo[0][:-2]
                dvy = velo[1][2:] - velo[1][:-2]
                dv = np.array((dvx,dvy))
                acc = dv/0.08
                mass =  data[game][team][key]['mass']

                

                work = mass*np.multiply(acc,dist[:,1:-1])
                work = np.abs(work)
                
                data[game][team][key]['work'] = np.add(work[0],work[1])

                 







def mass_warriors(data):

    playerdata = np.loadtxt('warriors_players.csv',delimiter=',',dtype=str,skiprows=1,unpack=True)
 
    for game in data.keys():

        for player in range(len(playerdata[0])):
            
            for team in ['homeplayers','awayplayers']:

                if (playerdata[1][player][1:-1]+playerdata[0][player][1:]) in data[game][team].keys():

# convert the mass from lbs to kg

                    data[game][team][playerdata[1][player][1:-1]+playerdata[0][player][1:]]['mass'] = float(playerdata[5][player][0:3])*0.453592



def mass_away(data):

    playerdata = np.loadtxt('rockets_weights.csv',delimiter=',',dtype=str,skiprows=1,unpack=True)
 
    for game in data.keys():

        for player in range(len(playerdata[0])):
            
            for team in ['homeplayers','awayplayers']:

                if (playerdata[1][player][1:-1]+playerdata[0][player][1:]) in data[game][team].keys():

                    data[game][team][playerdata[1][player][1:-1]+playerdata[0][player][1:]]['mass'] = float(playerdata[5][player][0:3])*0.453592


def ball_flagger(data):

    for game in data.keys():
       # so far this is based entirely on zone.... need to test for closest player as well 
        x_all = np.array(data[game]['ballXyz']['x'])
        right  =  x_all>0
        left = x_all<0
        period = np.array( data[game]['period'] )
        first = period<3
        second = period >2
        away = np.logical_or(np.logical_and(first,right), np.logical_and(second,left)) # or (second and not right)
        warriors = np.logical_not(away)
        data[game]['home_poss'] = warriors
        data[game]['away_poss'] = away





def player_flagger(data):
    for game in data.keys():
        for team in ['homeplayers', 'awayplayers']:
            for key in data[game][team].keys():
                ind = data[game][team][key]['time_slice']
                team_poss =data[game][team[:4]+'_poss']
                data[game][team][key]['poss'] = team_poss[ind]
                
def distance(player,ball,time_ind):
    x = np.array(player['x'] )
    y = np.array(player['y'] )
    x2 =np.array( ball['x'])[time_ind]
    y2 =np.array( ball['y'])[time_ind]
    dist = np.sqrt(np.square(np.subtract(x2,x)) + np.square(np.subtract(y2,y)))
    return dist

def player_flagger2(data):
    for game in data.keys():
        ballxyz = data[game]['ballXyz']
        for team in ['homeplayers','awayplayers']:
            for key in data[game][team].keys():
                time_indexer = data[game][team][key]['time_slice']
               
                dist_ball = distance(data[game][team][key],ballxyz,time_indexer)
                near_ball = dist_ball <= 3
                ind_poss = np.logical_and(near_ball,data[game][team][key]['poss'])
                data[game][team][key]['ind_poss'] = ind_poss

#
#def closest_to_ball(data):
#    for game in data.keys():
#        ballxyz = data[game]['ballXyz']
#        for team in ['homeplayers', 'awayplayers']:
#            data[game][team[0:4]] = {}
#            
#            #########
#            for i in range(len(ballxyz['x'])):
#                data[game][team[0:4]][str(i)] = []
#
#            print('team done')
#            #########
#
#
#            for key in data[game][team].keys():
#
#                print(key,'player done')
#                ind = data[game][team][key]['time_slice']
#                dist = distance(data[game][team][key],ballxyz,ind)
#                #for i in ind:
#                #    index = ind.index(i)
#                #    data[game][team]['dist_to_ball'][str(i)].append(dist[index])
#
#            
#
import requests
from bs4 import BeautifulSoup
import re

def get_masses(data):

    for game in data.keys():

        home = str(game[14:17])
        away = str(game[11:14])

        for team in ['homeplayers','awayplayers']:

            url = 'http://www.espn.com/nba/team/roster/_/name/%s' %(home)
            if team == 'awayplayers':
                url = 'http://www.espn.com/nba/team/roster/_/name/%s' %(away)

            r = requests.get(url)
            dataa = r.text

            soup = BeautifulSoup(dataa,'html.parser')
            for row in soup('tr'):

                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]

                if len(cols) > 5 and cols[1] != 'NAME':

                    name = cols[1]
                    new_name = name.replace(" ", "")
                    if new_name in data[game][team].keys():
                        data[game][team][new_name]['mass'] = float(cols[5])*0.453592
                    


            for key in data[game][team].keys():
                if 'mass' not in data[game][team][key].keys():
                    if key == 'LucMbah a Moute':
                        data[game][team][key]['mass'] = 229*0.453592
                    elif key == 'FrankMason':
                        data[game][team][key]['mass'] = 194*0.453592
                    elif key == 'NoneNene':
                        data[game][team][key]['mass'] = 250*0.453592
                    elif key == 'TJLeaf':
                        data[game][team][key]['mass'] = 230*0.453592
                    elif key == 'OttoPorter Jr.':
                        data[game][team][key]['mass'] = 203*0.453592
                    elif key == 'KellyOubre Jr.':
                        data[game][team][key]['mass'] = 205*0.453592




                    else:
                        name = (re.sub('([A-Z])',r' \1', key))
                        name = name[1:]
                        newer_name = name.replace(" ","_")
                        ind = newer_name.index("_")+1
                        newest_name = newer_name.lower()
                        last_init = newest_name[ind]



                        print("Look up %s's mass" %key)
                        
                        url = 'http://www.landofbasketball.com/nba_players/%s/%s.htm' %(last_init,newest_name)
                        r = requests.get(url)
                        dataa = r.text
                        soup = BeautifulSoup(dataa,'html.parser')

                        for row in soup('tr'):

                            cols = row.find_all('td')
                            cols = [ele.text.strip() for ele in cols]
                            if cols[0] == 'Weight:':

                                w = cols[1][:3]
                                data[game][team][key]['mass'] = float(w)*0.453592
                                
