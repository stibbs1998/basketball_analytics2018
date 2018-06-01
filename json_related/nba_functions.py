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



def mass_away(data):

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
        left = x_all<0
        period = np.array( data[game]['period'] )
        first = period<3
        second = period >2
        away = np.logical_or(np.logical_and(first,right), np.logical_and(second,left)) # or (second and not right)
        warriors = np.logical_not(away)
        data[game]['home_poss'] = warriors
        data[game]['away_poss'] = away






