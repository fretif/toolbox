# SYMPHONIE Extract Point #
Ce script permet d'extraire une série temporelle à partir d'un point donnée.
Il utilise un fichier de configuration de cette forme.

	#################################
	#	Variable to extract 		#
	#################################
	scanDir=/data/fieldsites/taiwan/modelling/large-scale/polar-grid-822x322x40/simulations/KUNSHEN-ECMWF-001/graphiques/

	outfile="/data/fieldsites/taiwan/modelling/large-scale/polar-grid-822x322x40/simulations/KUNSHEN-ECMWF-001/basic-processing/track_SSH_at_Chung-Chin.dat"

	startTime="2011-09-01T00:00:00"
	endTime="2011-11-01T00:00:00"
	var="ssh"
	#level=0

	#Tidal Chung-Chin New Station
	lat=23.2125
	long=120.083056

	#Optional
	printNearestPointCoordinate=1

# Utilisation
./extract_S_point.sh KUNSHEN-ECMWF-001_SSH_ADCP7m.conf

# Sorties
Les sorties sont sous forme de fichiers ASCII

