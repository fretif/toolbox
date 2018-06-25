#!/bin/bash

find `pwd` -maxdepth 1 -type f -name "*gridS*.nc" | sort > list_var_S
find `pwd` -maxdepth 1 -type f -name "*gridT*.nc" | sort > list_var_T
find `pwd` -maxdepth 1 -type f -name "*gridT*.nc" | sort > list_var_SSH
find `pwd` -maxdepth 1 -type f -name "*gridU*.nc" | sort > list_var_U
find `pwd` -maxdepth 1 -type f -name "*gridV*.nc" | sort > list_var_V

find `pwd` -maxdepth 1 -type f -name "*mesh_hgr*.nc" | sort > list_grid_T
find `pwd` -maxdepth 1 -type f -name "*mesh_hgr*.nc" | sort > list_grid_U
find `pwd` -maxdepth 1 -type f -name "*mesh_hgr*.nc" | sort > list_grid_V

