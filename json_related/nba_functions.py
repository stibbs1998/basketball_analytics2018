import numpy as np


def smoothing(a,n):
    ret = np.nancumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] /n



def velo(data):

    for game in data.keys():

        for team in ['homeplayers','awayplayers']:

            for key in data[game][team].keys():
                x = data[game][team][key]['x']
                y = data[game][team][key]['y']
                dx = np.array(x[2:]) - np.array(x[:-2])
                dy = np.array(y[2:]) - np.array(y[:-2])
                dist = np.sqrt(np.square(dx)+np.square(dy))
                velo = dist/0.08
                data[game][team][key]['velo'] = velo

   


