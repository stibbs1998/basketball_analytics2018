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
                dist = np.array(dx,dy)
                velo = dist/0.08
                data[game][team][key]['velo'] = velo
                dv = velo[2:]-velo[:-2]
                accel = dv/0.08
                data[game][team][key]['accel'] = accel	

   

def energy(data):	# W = F*d(cos(phi)) = $\delta$ KE
	
	for game in data.keys():

		for team in ['homeplayers','awayplayers']:

			for key in data[game][team].keys():
				dx = np.array(x[2:]) - np.array(x[:-2])
				dy = np.array(y[2:]) - np.array(y[:-2])
				d = np.array(dx,dy)
				mass = 0 # holder
				acc = data[game][team][key]['accel']
				force = np.multiply(mass,acc)
				F = np.array(force,force)
				Work = np.multiply(F,d)	
				data[game][team][key]['work'] = Work
