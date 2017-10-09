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
from timeserie.io.ascii.candhis.CandhisReader import CandhisReader
from timeserie.io.ascii.ww3.WW3Reader import WW3Reader
from timeserie.utils.stats import *
import logging

if __name__ == "__main__":
    print("Calcul statistiques")

    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)

    # modèle
    modelReader = WW3Reader("CANDHIS-waves.ww3")
    model = TimeSerie(modelReader,start='2013-12-01',end='2014-01-01',freq='30min');

    # observations
    obsReader = CandhisReader("CANDHIS_wave_data.csv")
    obs = TimeSerie(obsReader,start='2013-12-01',end='2014-01-01',freq='30min');

    # join sur les données
    modelData = model.read_data()
    obsData = obs.read_data()

    result = obsData.join(modelData, how='inner',lsuffix='_obs', rsuffix='_model')

    var_cor = correlation(result.sea_surface_wave_significant_height_obs,result.sea_surface_wave_significant_height_model)
    var_bias = bias(result.sea_surface_wave_significant_height_obs,result.sea_surface_wave_significant_height_model)
    var_rmse = rmse(result.sea_surface_wave_significant_height_obs,result.sea_surface_wave_significant_height_model)
    var_si = si(result.sea_surface_wave_significant_height_obs,result.sea_surface_wave_significant_height_model)
    var_maxerr = maxerr(result.sea_surface_wave_significant_height_obs,result.sea_surface_wave_significant_height_model)

    print('COR=',var_cor,'BIAS=',var_bias,'MAXERR=',var_maxerr,'RMSE=',var_rmse)


    print('End of programm')

    
       
        
    
    
    
    
    
