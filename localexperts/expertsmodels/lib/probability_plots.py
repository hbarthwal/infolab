'''
Created on Apr 15, 2013

@author: Himanshu Barthwal
'''
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

from backstorm_model import BackStormModelGenerator



class Model():
    c = 0.0
    alpha = 0.0
    latitude = 0.0
    longitude = 0.0
    def __init__(self):
        pass
    
    def output(self):
        print (self.c, self.alpha, self.latitude, self.longitude)

class ModelPlot:

    @staticmethod
    def plot_peak(model, ax, X, Y, finalZ):
        distance = 0.0 + pow((X - model.longitude) ** 2 + (Y - model.latitude) ** 2, 0.5)
        Z = np.double(model.c * distance ** model.alpha)
        if finalZ == None:
            finalZ = Z
        i = 0
        while (i < len(Z)):
            j = 0
            while (j < len(Z[i])):
                if Z[i][j] >= model.c:
                    Z[i][j] = model.c
                if Z[i][j] > finalZ[i][j]:
                    finalZ[i][j] = Z[i][j]
                j = j + 1
            i = i + 1
        return finalZ

    @staticmethod
    def plot_multiple_peaks(models, title):
        fig = plt.figure()
        ax = Axes3D(fig)
        latitude_upper_left = 50
        latitude_lower_right = 26
        longitude_upper_left = -130
        longitude_upper_right = -66
        step_latitude = 1.0 * (latitude_upper_left - latitude_lower_right) / 100
        step_longitude = 1.0 * (longitude_upper_right - longitude_upper_left) / 100
    
        X = np.arange(longitude_upper_left, longitude_upper_right, step_longitude)
        Y = np.arange(latitude_lower_right, latitude_upper_left, step_latitude)
        X, Y = np.meshgrid(X, Y)
        
        # normalizing Z
        finalZ = None
        for model in models:
            finalZ = ModelPlot.plot_peak(model, ax, X, Y, finalZ)
        finalZ = ModelPlot.normalizing_z_matrix(finalZ)
    
        ax.plot_surface(X, Y, finalZ, rstride=1, cstride=1, cmap=cm.jet)
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_zlabel('Probability')
        plt.title(title)
        plt.show()
    
    @staticmethod
    def normalizing_z_matrix(Z):
        max_value = 0.0
        i = 0
        while (i < len(Z)):
            j = 0
            while (j < len(Z[i])):
                if Z[i][j] > max_value:
                    max_value = Z[i][j]
                j = j + 1
            i = i + 1
        
        finalZ = Z
        i = 0
        while (i < len(Z)):
            j = 0
            while (j < len(Z[i])):
                finalZ[i][j] = Z[i][j] / max_value
                j = j + 1
            i = i + 1
        return finalZ

def main():
    models = []
    dataDirectory = 'data/'
    modelGenerator = BackStormModelGenerator(dataDirectory)
    # dictModellist = modelGenerator.getModelsForAllExpertise()
    
    dictModellist = {'vc': [{'C': 0.10209873434416397,
                     'alpha': 0.4099257815602122,
                     'center': (38.00939497727273, -122.86621224166666),
                     'regionName': 'vc Region 9'}]}            
    
    
    
    for expertise in dictModellist:
        modellist = dictModellist[expertise]
        for modelDict in modellist:
            model = Model()
            model.latitude = modelDict['center'][0]
            model.longitude = modelDict['center'][1]
            model.c = modelDict['C']
            model.alpha = -modelDict['alpha']
            models.append(model)
        ModelPlot.plot_multiple_peaks(models, expertise)

if __name__ == "__main__":
    main()
