import numpy as np


def smoothing(a,n):
    ret = np.nancumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] /n



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
                data[game][team][key]['velo'] = velo
                dvx = velo[0][2:]-velo[0][:-2]
                dvy = velo[1][2:]-velo[1][:-2]
                dv = np.array((dvx,dvy))
                accel = dv/0.08

                data[game][team][key]['accel'] = accel	

   

def energy(data):	# W = F*d(cos(phi)) = $\delta$ KE
	
	for game in data.keys():

		for team in ['homeplayers','awayplayers']:

			for key in data[game][team].keys():
                                x = data[game][team][key]['x']
                                y = data[game][team][key]['y']
                                dx = np.array(x[4:]) - np.array(x[:-4])
                                dy = np.array(y[4:]) - np.array(y[:-4])
                                d = np.array((dx,dy))
                                mass = data[game][team][key]['mass']
                                acc = data[game][team][key]['accel']
                                force = np.multiply(mass,acc)
                                Work = np.multiply(force,d)	
                                data[game][team][key]['work'] = Work


def mass_warriors(data):

    playerdata = np.loadtxt('warriors_players.csv',delimiter=',',dtype=str,skiprows=1,unpack=True)
 
    for game in data.keys():

        for player in range(len(playerdata[0])):
            
            for team in ['homeplayers']:

                if (playerdata[1][player][1:-1]+playerdata[0][player][1:]) in data[game][team].keys():

                    data[game][team][playerdata[1][player][1:-1]+playerdata[0][player][1:]]['mass'] = float(playerdata[5][player][0:3])*0.453592



def mass_rockets(data):

    playerdata = np.loadtxt('rockets_weights.csv',delimiter=',',dtype=str,skiprows=1,unpack=True)
 
    for game in data.keys():

        for player in range(len(playerdata[0])):
            
            for team in ['awayplayers']:

                if (playerdata[1][player][1:-1]+playerdata[0][player][1:]) in data[game][team].keys():

                    data[game][team][playerdata[1][player][1:-1]+playerdata[0][player][1:]]['mass'] = float(playerdata[5][player][0:3])*0.453592


def ball_flagger(data):

    for game in data.keys():
       # so far this is based entirely on zone.... need to test for closest player as well 
        x_all = np.array(data[game]['ballXyz']['x'])
        right  =  x_all>0
        period = np.array( data[game]['period'] )
        first = period<0
        second = period >2
        rockets = (first and right) or (second and not right)
        warriors = not rockets 
