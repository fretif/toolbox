#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# CoverageProcessing is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# CoverageProcessing is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

# Lien vers le dossier de la lib
import sys
sys.path.append('../../timeseries-processing')

from timeserie.TimeSerie import TimeSerie
from timeserie.io.ascii.sirocco.SiroccoReader import SiroccoReader
from timeserie.io.ascii.ww3.WW3Reader import WW3Reader
from utils.stats import *
import logging
import numpy as np
import glob
import re
from os.path import basename

if __name__ == "__main__":
    print("Calcul statistiques")

    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)

    modelDir="/home/retf/work/fieldsites/med-cruesim/modelling/waves/med/outputs/w1/points/"
    obsDir="/home/retf/work/fieldsites/med-cruesim/observations/waves/"

    modelFiles = glob.glob(modelDir+"*-waves.ww3")

    statFile = open('/home/retf/work/fieldsites/med-cruesim/modelling/waves/med/outputs/w1/points/stat.csv', "w")
    statFile.write("#Buoy \t Parameter \t CORRELATION \t BIAS \t RMSE \t SI \t MAXERR\n")

    for file in modelFiles:

        filename = basename(file)
        m = re.search('^([A-Z]+[\-\_]*[A-Z]*)\-[a-z]+.*', filename)
        if m:
            name_station = m.group(1)
            logging.info("Station : "+str(name_station))

            obsFiles = glob.glob(obsDir+name_station+"_*.dat")

            if len(obsFiles) == 1:

                # modèle
                modelReader = WW3Reader(file)
                model = TimeSerie(modelReader,start='2013-03-03',end='2013-04-01',freq='30min');

                # observations
                obsReader = SiroccoReader(obsFiles[0])
                obs = TimeSerie(obsReader,start='2013-03-03',end='2013-04-01',freq='H');

                # join sur les données
                modelData = model.read_data()
                obsData = obs.read_data()

                result = obsData.join(modelData, how='inner',lsuffix='_obs', rsuffix='_model')

                var_cor = correlation(result.sea_surface_wave_significant_height_obs,result.sea_surface_wave_significant_height_model)
                var_bias = bias(result.sea_surface_wave_significant_height_obs,result.sea_surface_wave_significant_height_model)
                var_rmse = rmse(result.sea_surface_wave_significant_height_obs,result.sea_surface_wave_significant_height_model)
                var_si = si(result.sea_surface_wave_significant_height_obs,result.sea_surface_wave_significant_height_model)
                var_maxerr = maxerr(result.sea_surface_wave_significant_height_obs,result.sea_surface_wave_significant_height_model)

                statFile.write(str(name_station)+"\t sea_surface_wave_significant_height \t"+str(var_cor)+"\t" +str(var_bias)+"\t"+str(var_rmse)+"\t"+str(var_si)+"\t"+str(var_maxerr)+"\n")

                if 'sea_surface_wave_mean_period_obs' in result:
                    var_cor = correlation(result.sea_surface_wave_mean_period_obs,result.sea_surface_wave_mean_period_model)
                    var_bias = bias(result.sea_surface_wave_mean_period_obs,result.sea_surface_wave_mean_period_model)
                    var_rmse = rmse(result.sea_surface_wave_mean_period_obs,result.sea_surface_wave_mean_period_model)
                    var_si = si(result.sea_surface_wave_mean_period_obs,result.sea_surface_wave_mean_period_model)
                    var_maxerr = maxerr(result.sea_surface_wave_mean_period_obs,result.sea_surface_wave_mean_period_model)

                    statFile.write(str(name_station)+"\t sea_surface_wave_mean_period \t"+str(var_cor)+"\t" +str(var_bias)+"\t"+str(var_rmse)+"\t"+str(var_si)+"\t"+str(var_maxerr)+"\n")

                if 'sea_surface_wave_from_direction_obs' in result and 'sea_surface_wave_from_direction_model' in result:
                    var_cor = correlation(result.sea_surface_wave_from_direction_obs,result.sea_surface_wave_from_direction_model)
                    var_bias = bias(result.sea_surface_wave_from_direction_obs,result.sea_surface_wave_from_direction_model)
                    var_rmse = rmse(result.sea_surface_wave_from_direction_obs,result.sea_surface_wave_from_direction_model)
                    var_si = si(result.sea_surface_wave_from_direction_obs,result.sea_surface_wave_from_direction_model)
                    var_maxerr = maxerr(result.sea_surface_wave_from_direction_obs,result.sea_surface_wave_from_direction_model)

                    statFile.write(str(name_station)+"\t sea_surface_wave_from_direction \t"+str(var_cor)+"\t" +str(var_bias)+"\t"+str(var_rmse)+"\t"+str(var_si)+"\t"+str(var_maxerr)+"\n")

            else:
                logging.warn('No data found for the station '+str(name_station)+".")

    statFile.close()
    print 'End of programm'

def RMSE(predictions, targets):
    return np.sqrt(np.nanmean((predictions - targets) ** 2))

def COR(predictions, targets):
    return np.ma.corrcoef(predictions, targets, allow_masked=True)[0,1]
    
       
        
    
    
    
    
    
