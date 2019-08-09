#!/bin/bash

declare -A STANDARD_NAME
declare -A LONG_NAME
declare -A VARIABLE_NAME
declare -A CANONICAL_UNITS
declare -A GMT_SCRIPT
declare -A COLOR_PALETTES

STANDARD_NAME["sea_binary_mask"]="sea_binary_mask"
LONG_NAME["sea_binary_mask"]="Sea Binary Mask"
VARIABLE_NAME["sea_binary_mask"]="sea_mask"
CANONICAL_UNITS["sea_binary_mask"]="1"
GMT_SCRIPT["sea_binary_mask"]="2d_var"

STANDARD_NAME["land_binary_mask"]="land_binary_mask"
LONG_NAME["land_binary_mask"]="Land Binary Mask"
VARIABLE_NAME["land_binary_mask"]="land_mask"
CANONICAL_UNITS["land_binary_mask"]="1"
GMT_SCRIPT["land_binary_mask"]="2d_var"

STANDARD_NAME["wet_binary_mask"]="wet_binary_mask"
LONG_NAME["wet_binary_mask"]="Wet Binary Mask"
VARIABLE_NAME["wet_binary_mask"]="wet_mask"
CANONICAL_UNITS["wet_binary_mask"]="1"
GMT_SCRIPT["wet_binary_mask"]="2d_var"

STANDARD_NAME["mesh_size"]="mesh_size"
LONG_NAME["mesh_size"]="Mesh Size"
VARIABLE_NAME["mesh_size"]="mesh_size"
CANONICAL_UNITS["mesh_size"]="m"
GMT_SCRIPT["mesh_size"]="2d_var"

#################
# HYDRO
# Sea Surface
#################
STANDARD_NAME["sea_surface_height_above_mean_sea_level"]="sea_surface_height_above_mean_sea_level"
LONG_NAME["sea_surface_height_above_mean_sea_level"]="Sea Surface Height Above Mean Sea Level"
VARIABLE_NAME["sea_surface_height_above_mean_sea_level"]="ssh_msl"
CANONICAL_UNITS["sea_surface_height_above_mean_sea_level"]="m"
GMT_SCRIPT["sea_surface_height_above_mean_sea_level"]="2d_var"

STANDARD_NAME["sea_surface_height_above_geoid"]="sea_surface_height_above_geoid"
LONG_NAME["sea_surface_height_above_geoid"]="Sea Surface Height Above Geoid"
VARIABLE_NAME["sea_surface_height_above_geoid"]="ssh_geoid"
CANONICAL_UNITS["sea_surface_height_above_geoid"]="m"
GMT_SCRIPT["sea_surface_height_above_geoid"]="2d_var"

STANDARD_NAME["sea_surface_temperature"]="sea_surface_temperature"
LONG_NAME["sea_surface_temperature"]="Sea Surface Temperature"
VARIABLE_NAME["sea_surface_temperature"]="sea_surface_temperature"
CANONICAL_UNITS["sea_surface_temperature"]="C"
GMT_SCRIPT["sea_surface_temperature"]="2d_var"

STANDARD_NAME["sea_surface_salinity"]="sea_surface_salinity"
LONG_NAME["sea_surface_salinity"]="Sea Surface Salinity"
VARIABLE_NAME["sea_surface_salinity"]="sea_surface_salinity"
CANONICAL_UNITS["sea_surface_salinity"]="psu"
GMT_SCRIPT["sea_surface_salinity"]="2d_var"

STANDARD_NAME["sea_water_pressure_at_sea_water_surface"]="sea_water_pressure_at_sea_water_surface"
LONG_NAME["sea_water_pressure_at_sea_water_surface"]="Sea Water Pressure At Sea Water Surface"
VARIABLE_NAME["sea_water_pressure_at_sea_water_surface"]="sea_surface_water_pressure"
CANONICAL_UNITS["sea_water_pressure_at_sea_water_surface"]="dbar"
GMT_SCRIPT["sea_water_pressure_at_sea_water_surface"]="2d_var"

STANDARD_NAME["sea_surface_density"]="sea_surface_density"
LONG_NAME["sea_surface_density"]="Sea Surface Density"
VARIABLE_NAME["sea_surface_density"]="sea_surface_density"
CANONICAL_UNITS["sea_surface_density"]="kg m-3"
GMT_SCRIPT["sea_surface_density"]="2d_var"

STANDARD_NAME["sea_water_velocity_at_sea_water_surface"]="sea_water_velocity_at_sea_water_surface"
LONG_NAME["sea_water_velocity_at_sea_water_surface"]="Sea Water Velocity At Sea Water Surface"
VARIABLE_NAME["eastward_sea_water_velocity_at_sea_water_surface"]="u_sea_surface_vel"
VARIABLE_NAME["northward_sea_water_velocity_at_sea_water_surface"]="v_sea_surface_vel"
CANONICAL_UNITS["sea_water_velocity_at_sea_water_surface"]="m s-1"
GMT_SCRIPT["sea_water_velocity_at_sea_water_surface"]="vector_var"

#STANDARD_NAME["sea_water_speed_at_sea_water_surface"]="sea_water_speed_at_sea_water_surface"
#LONG_NAME["sea_water_speed_at_sea_water_surface"]="Sea Water Speed At Sea Water Surface"
#VARIABLE_NAME["sea_water_speed_at_sea_water_surface"]="sea_surface_speed"
#CANONICAL_UNITS["sea_water_speed_at_sea_water_surface"]="m s-1"
#GMT_SCRIPT["sea_water_speed_at_sea_water_surface"]="2d_var"

#STANDARD_NAME["sea_water_from_direction_at_sea_water_surface"]="sea_water_from_direction_at_sea_water_surface"
#LONG_NAME["sea_water_from_direction_at_sea_water_surface"]="Sea Water From Direction At Sea Water Surface"
#VARIABLE_NAME["sea_water_from_direction_at_sea_water_surface"]="sea_surface_from_dir"
#CANONICAL_UNITS["sea_water_from_direction_at_sea_water_surface"]="degree"  # from North=0"
#GMT_SCRIPT["sea_water_from_direction_at_sea_water_surface"]="dir_var"

#STANDARD_NAME["sea_water_to_direction_at_sea_water_surface"]="sea_water_to_direction_at_sea_water_surface"
#LONG_NAME["sea_water_to_direction_at_sea_water_surface"]="Sea Water To Direction At Sea Water Surface"
#VARIABLE_NAME["sea_water_to_direction_at_sea_water_surface"]="sea_surface_to_dir"
#CANONICAL_UNITS["sea_water_to_direction_at_sea_water_surface"]="degree"  # from North=0"
#GMT_SCRIPT["sea_water_to_direction_at_sea_water_surface"]="dir_var"

#################
# HYDRO
# Ground level
#################
STANDARD_NAME["sea_water_temperature_at_ground_level"]="sea_water_temperature_at_ground_level"
LONG_NAME["sea_water_temperature_at_ground_level"]="Sea Water Temperature At Ground Level"
VARIABLE_NAME["sea_water_temperature_at_ground_level"]="sea_bottom_temperature"
CANONICAL_UNITS["sea_water_temperature_at_ground_level"]="degree"
GMT_SCRIPT["sea_water_temperature_at_ground_level"]="2d_var"

STANDARD_NAME["sea_water_salinity_at_ground_level"]="sea_water_salinity_at_ground_level"
LONG_NAME["sea_water_salinity_at_ground_level"]="Sea Water Salinity At Ground Level"
VARIABLE_NAME["sea_water_salinity_at_ground_level"]="sea_bottom_salinity"
CANONICAL_UNITS["sea_water_salinity_at_ground_level"]="psu"
GMT_SCRIPT["sea_water_salinity_at_ground_level"]="2d_var"

STANDARD_NAME["sea_water_pressure_at_ground_level"]="sea_water_pressure_at_ground_level"
LONG_NAME["sea_water_pressure_at_ground_level"]="Sea Water Pressure At Sea Water Surface"
VARIABLE_NAME["sea_water_pressure_at_ground_level"]="sea_bottom_pressure"
CANONICAL_UNITS["sea_water_pressure_at_ground_level"]="dbar"
GMT_SCRIPT["sea_water_pressure_at_ground_level"]="2d_var"

STANDARD_NAME["sea_water_density_at_ground_level"]="sea_water_density_at_ground_level"
LONG_NAME["sea_water_density_at_ground_level"]="Sea Water Density At Ground Level"
VARIABLE_NAME["sea_water_density_at_ground_level"]="sea_water_density_at_ground_level"
CANONICAL_UNITS["sea_water_density_at_ground_level"]="kg m-3"
GMT_SCRIPT["sea_water_density_at_ground_level"]="2d_var"

STANDARD_NAME["sea_water_velocity_at_ground_level"]="sea_water_velocity_at_ground_level"
LONG_NAME["sea_water_velocity_at_ground_level"]="Sea Water Velocity At Ground Level"
VARIABLE_NAME["eastward_sea_water_velocity_at_ground_level"]="u_sea_bottom_vel"
VARIABLE_NAME["northward_sea_water_velocity_at_ground_level"]="v_sea_bottom_vel"
CANONICAL_UNITS["sea_water_velocity_at_ground_level"]="m s-1"
GMT_SCRIPT["sea_water_velocity_at_ground_level"]="2d_var"

STANDARD_NAME["sea_water_speed_at_ground_level"]="sea_water_speed_at_ground_level"
LONG_NAME["sea_water_speed_at_ground_level"]="Sea Water Speed At Ground Level"
VARIABLE_NAME["sea_water_speed_at_ground_level"]="sea_bottom_speed"
CANONICAL_UNITS["sea_water_speed_at_ground_level"]="m s-1"
GMT_SCRIPT["sea_water_speed_at_ground_level"]="2d_var"

STANDARD_NAME["sea_water_from_direction_at_ground_level"]="sea_water_from_direction_at_ground_level"
LONG_NAME["sea_water_from_direction_at_ground_level"]="Sea Water From Direction At Ground Level"
VARIABLE_NAME["sea_water_from_direction_at_ground_level"]="sea_bottom_from_dir"
CANONICAL_UNITS["sea_water_from_direction_at_ground_level"]="degree"
GMT_SCRIPT["longitude"]="2d_var"

STANDARD_NAME["sea_water_to_direction_at_ground_level"]="sea_water_to_direction_at_ground_level"
LONG_NAME["sea_water_to_direction_at_ground_level"]="Sea Water To Direction At Ground Level"
VARIABLE_NAME["sea_water_to_direction_at_ground_level"]="sea_bottom_to_dir"
CANONICAL_UNITS["sea_water_to_direction_at_ground_level"]="degree"
GMT_SCRIPT["longitude"]="2d_var"

#################
# HYDRO
# 2D
#################
STANDARD_NAME["bathymetry"]="bathymetry"
LONG_NAME["bathymetry"]="Bathymetry"
VARIABLE_NAME["bathymetry"]="bathymetry"
CANONICAL_UNITS["bathymetry"]="m"
GMT_SCRIPT["bathymetry"]="2d_var"

STANDARD_NAME["barotropic_sea_water_velocity"]="barotropic_sea_water_velocity"
LONG_NAME["barotropic_sea_water_velocity"]="Barotropic Sea Water Velocity"
VARIABLE_NAME["eastward_barotropic_sea_water_velocity"]="u_sea_water_bar_vel"
VARIABLE_NAME["northward_barotropic_sea_water_velocity"]="v_sea_water_bar_vel"
CANONICAL_UNITS["barotropic_sea_water_velocity"]="m s-1"
GMT_SCRIPT["barotropic_sea_water_velocity"]="vector_var"

#STANDARD_NAME["barotropic_sea_water_speed"]="barotropic_sea_water_speed"
#LONG_NAME["barotropic_sea_water_speed"]="Barotropic Sea Water Speed"
#VARIABLE_NAME["barotropic_sea_water_speed"]="sea_water_bar_speed"
#CANONICAL_UNITS["barotropic_sea_water_speed"]="m s-1"
#GMT_SCRIPT["longitude"]="2d_var"

#STANDARD_NAME["barotropic_sea_water_from_direction"]="barotropic_sea_water_from_direction"
#LONG_NAME["barotropic_sea_water_from_direction"]="Barotropic Sea Water From Direction"
#VARIABLE_NAME["barotropic_sea_water_from_direction"]="sea_water_bar_from_dir"
#CANONICAL_UNITS["barotropic_sea_water_from_direction"]="degree"  # from North=0"
#GMT_SCRIPT["longitude"]="2d_var"

#STANDARD_NAME["barotropic_sea_water_to_direction"]="barotropic_sea_water_to_direction"
#LONG_NAME["barotropic_sea_water_to_direction"]="Barotropic Sea Water To Direction"
#VARIABLE_NAME["barotropic_sea_water_to_direction"]="sea_water_bar_to_dir"
#CANONICAL_UNITS["barotropic_sea_water_to_direction"]="degree"  # from North=0"
#GMT_SCRIPT["longitude"]="2d_var"

#STANDARD_NAME["water_volume_transport_into_sea_water_from_rivers"]="water_volume_transport_into_sea_water_from_rivers"
#LONG_NAME["water_volume_transport_into_sea_water_from_rivers"]="Water Volume Transport Into Sea Water From Rivers"
#VARIABLE_NAME["water_volume_transport_into_sea_water_from_rivers"]="rivers_flux"
#CANONICAL_UNITS["water_volume_transport_into_sea_water_from_rivers"]="m3 s-1"
#GMT_SCRIPT["longitude"]="2d_var"

#################
# HYDRO
# 3D
#################
STANDARD_NAME["sea_water_turbidity"]="sea_water_turbidity"
LONG_NAME["sea_water_turbidity"]="Sea Water Turbidity"
VARIABLE_NAME["sea_water_turbidity"]="sea_water_turbidity"
CANONICAL_UNITS["sea_water_turbidity"]="FTU"
GMT_SCRIPT["longitude"]="2d_var"

STANDARD_NAME["sea_water_electrical_conductivity"]="sea_water_electrical_conductivity"
LONG_NAME["sea_water_electrical_conductivity"]="Sea Water Electrical Conductivity"
VARIABLE_NAME["sea_water_electrical_conductivity"]="sea_water_electrical_conductivity"
CANONICAL_UNITS["sea_water_electrical_conductivity"]="S m-1"
GMT_SCRIPT["longitude"]="2d_var"

STANDARD_NAME["sea_water_temperature"]="sea_water_temperature"
LONG_NAME["sea_water_temperature"]="Sea Water Temperature"
VARIABLE_NAME["sea_water_temperature"]="sea_water_temperature"
CANONICAL_UNITS["sea_water_temperature"]="degree"
GMT_SCRIPT["longitude"]="2d_var"

STANDARD_NAME["sea_water_salinity"]="sea_water_salinity"
LONG_NAME["sea_water_salinity"]="Sea Water Salinity"
VARIABLE_NAME["sea_water_salinity"]="sea_water_salinity"
CANONICAL_UNITS["sea_water_salinity"]="psu"
GMT_SCRIPT["longitude"]="2d_var"

STANDARD_NAME["sea_water_density"]="sea_water_density"
LONG_NAME["sea_water_density"]="Sea Water Density"
VARIABLE_NAME["sea_water_density"]="sea_water_density"
CANONICAL_UNITS["sea_water_density"]="kg m-3"
GMT_SCRIPT["longitude"]="2d_var"

STANDARD_NAME["baroclinic_eastward_sea_water_velocity"]="baroclinic_eastward_sea_water_velocity"
LONG_NAME["baroclinic_eastward_sea_water_velocity"]="Baroclinic Eastward Sea Water Velocity"
VARIABLE_NAME["baroclinic_eastward_sea_water_velocity"]="u_sea_water_vel"
CANONICAL_UNITS["baroclinic_eastward_sea_water_velocity"]="m s-1"
GMT_SCRIPT["longitude"]="2d_var"

STANDARD_NAME["baroclinic_northward_sea_water_velocity"]="baroclinic_northward_sea_water_velocity"
LONG_NAME["baroclinic_northward_sea_water_velocity"]="Baroclinic Northward Sea Water Velocity"
VARIABLE_NAME["baroclinic_northward_sea_water_velocity"]="v_sea_water_vel"
CANONICAL_UNITS["baroclinic_northward_sea_water_velocity"]="m s-1"
GMT_SCRIPT["longitude"]="2d_var"

STANDARD_NAME["baroclinic_sea_water_speed"]="baroclinic_sea_water_speed"
LONG_NAME["baroclinic_sea_water_speed"]="Baroclinic Sea Water Speed"
VARIABLE_NAME["baroclinic_sea_water_speed"]="sea_water_speed"
CANONICAL_UNITS["baroclinic_sea_water_speed"]="m s-1"
GMT_SCRIPT["longitude"]="2d_var"

STANDARD_NAME["baroclinic_sea_water_from_direction"]="baroclinic_sea_water_from_direction"
LONG_NAME["baroclinic_sea_water_from_direction"]="Baroclinic Sea Water From Direction"
VARIABLE_NAME["baroclinic_sea_water_from_direction"]="sea_water_from_dir"
CANONICAL_UNITS["baroclinic_sea_water_from_direction"]="degree"  # from North=0"
GMT_SCRIPT["longitude"]="2d_var"

STANDARD_NAME["baroclinic_sea_water_to_direction"]="baroclinic_sea_water_to_direction"
LONG_NAME["baroclinic_sea_water_to_direction"]="Baroclinic Sea Water To Direction"
VARIABLE_NAME["baroclinic_sea_water_to_direction"]="sea_water_to_dir"
CANONICAL_UNITS["baroclinic_sea_water_to_direction"]="degree"  # from North=0"
GMT_SCRIPT["longitude"]="2d_var"

#################
# WAVES
# Sea Surface
#################
STANDARD_NAME["sea_surface_wave_significant_height"]="sea_surface_wave_significant_height"
LONG_NAME["sea_surface_wave_significant_height"]="Sea Surface Wave Significant Height"
VARIABLE_NAME["sea_surface_wave_significant_height"]="hs"
CANONICAL_UNITS["sea_surface_wave_significant_height"]="m"
GMT_SCRIPT["sea_surface_wave_significant_height"]="2d_var"

STANDARD_NAME["sea_surface_wave_breaking_height"]="sea_surface_wave_breaking_height"
LONG_NAME["sea_surface_wave_breaking_height"]="Sea Surface Wave Breaking Height"
VARIABLE_NAME["sea_surface_wave_breaking_height"]="wch"
CANONICAL_UNITS["sea_surface_wave_breaking_height"]="m"
GMT_SCRIPT["sea_surface_wave_breaking_height"]="2d_var"

STANDARD_NAME["sea_surface_wave_mean_period"]="sea_surface_wave_mean_period"
LONG_NAME["sea_surface_wave_mean_period"]="Sea Surface Wave Mean Period"
VARIABLE_NAME["sea_surface_wave_mean_period"]="wave_mean_period"
CANONICAL_UNITS["sea_surface_wave_mean_period"]="s"
GMT_SCRIPT["sea_surface_wave_mean_period"]="2d_var"

STANDARD_NAME["sea_surface_wave_peak_period"]="sea_surface_wave_peak_period"
LONG_NAME["sea_surface_wave_peak_period"]="Sea Surface Wave Peak Period"
VARIABLE_NAME["sea_surface_wave_peak_period"]="wave_peak_period"
CANONICAL_UNITS["sea_surface_wave_peak_period"]="s"
GMT_SCRIPT["sea_surface_wave_peak_period"]="2d_var"

STANDARD_NAME["sea_surface_wave_from_direction"]="sea_surface_wave_from_direction"
LONG_NAME["sea_surface_wave_from_direction"]="Sea Surface Wave From Direction"
VARIABLE_NAME["sea_surface_wave_from_direction"]="wave_from_dir"
CANONICAL_UNITS["sea_surface_wave_from_direction"]="degree" # from North=0 / East=90"
GMT_SCRIPT["sea_surface_wave_from_direction"]="2d_var"

STANDARD_NAME["sea_surface_wave_to_direction"]="sea_surface_wave_to_direction"
LONG_NAME["sea_surface_wave_to_direction"]="Sea Surface Wave To Direction"
VARIABLE_NAME["sea_surface_wave_to_direction"]="wave_to_dir"
CANONICAL_UNITS["sea_surface_wave_to_direction"]="degree" # from North=0 / East=90"
GMT_SCRIPT["sea_surface_wave_to_direction"]="2d_var"

STANDARD_NAME["sea_surface_wave_stokes_drift_velocity"]="sea_surface_wave_stokes_drift_velocity"
LONG_NAME["sea_surface_wave_stokes_drift_velocity"]="Sea Surface Wave Stokes Drift Velocity"
VARIABLE_NAME["eastward_sea_surface_wave_stokes_drift_velocity"]="u_stokes_drift_vel"
VARIABLE_NAME["northward_sea_surface_wave_stokes_drift_velocity"]="v_stokes_drift_vel"
CANONICAL_UNITS["sea_surface_wave_stokes_drift_velocity"]="m s-1"
GMT_SCRIPT["sea_surface_wave_stokes_drift_velocity"]="2d_var"

STANDARD_NAME["radiation_pressure_bernouilli_head"]="radiation_pressure_bernouilli_head"
LONG_NAME["radiation_pressure_bernouilli_head"]="Radiation Pressure Bernouilli_Head"
VARIABLE_NAME["radiation_pressure_bernouilli_head"]="pres_bernouilli_head"
CANONICAL_UNITS["radiation_pressure_bernouilli_head"]="m2 s-2"
GMT_SCRIPT["radiation_pressure_bernouilli_head"]="2d_var"

STANDARD_NAME["sea_surface_wave_energy_flux_to_ocean"]="sea_surface_wave_energy_flux_to_ocean"
LONG_NAME["sea_surface_wave_energy_flux_to_ocean"]="Sea Surface Wave Energy Flux To Ocean"
VARIABLE_NAME["sea_surface_wave_energy_flux_to_ocean"]="wave_energy_flux_to_ocean"
CANONICAL_UNITS["sea_surface_wave_energy_flux_to_ocean"]="W m-2"
GMT_SCRIPT["sea_surface_wave_energy_flux_to_ocean"]="2d_var"

STANDARD_NAME["sea_surface_wave_energy_dissipation_at_ground_level"]="sea_surface_wave_energy_dissipation_at_ground_level"
LONG_NAME["sea_surface_wave_energy_dissipation_at_ground_level"]="Sea Surface Wave Energy Dissipation At Ground Level"
VARIABLE_NAME["sea_surface_wave_energy_dissipation_at_ground_level"]="wave_energy_dissip_bottom"
CANONICAL_UNITS["sea_surface_wave_energy_dissipation_at_ground_level"]="W m-2"
GMT_SCRIPT["sea_surface_wave_energy_dissipation_at_ground_level"]="2d_var"

#################
# WAVES
# Momentum flux
#################
STANDARD_NAME["atmosphere_momentum_flux_to_waves"]="atmosphere_momentum_flux_to_waves"
LONG_NAME["atmosphere_momentum_flux_to_waves"]="Atmosphere Momentum Flux To Waves"
VARIABLE_NAME["eastward_atmosphere_momentum_flux_to_waves"]="u_taw"
VARIABLE_NAME["northward_atmosphere_momentum_flux_to_waves"]="v_taw"
CANONICAL_UNITS["atmosphere_momentum_flux_to_waves"]="m2 s-1"
GMT_SCRIPT["atmosphere_momentum_flux_to_waves"]="2d_var"

STANDARD_NAME["waves_momentum_flux_to_ocean"]="waves_momentum_flux_to_ocean"
LONG_NAME["waves_momentum_flux_to_ocean"]="Waves Momentum Flux To Ocean"
VARIABLE_NAME["eastward_waves_momentum_flux_to_ocean"]="u_two"
VARIABLE_NAME["northward_waves_momentum_flux_to_ocean"]="v_two"
CANONICAL_UNITS["waves_momentum_flux_to_ocean"]="m2 s-1"
GMT_SCRIPT["waves_momentum_flux_to_ocean"]="2d_var"

#################
# METEO
# 2D
#################
STANDARD_NAME["topography"]="topography"
LONG_NAME["topography"]="Topography"
VARIABLE_NAME["topography"]="topography"
CANONICAL_UNITS["topography"]="m"
GMT_SCRIPT["topography"]="2d_var"

STANDARD_NAME["rainfall_amount"]="rainfall_amount"
LONG_NAME["rainfall_amount"]="Rainfall Amount"
VARIABLE_NAME["rainfall_amount"]="rainfall"
CANONICAL_UNITS["rainfall_amount"]="kg m-1"
GMT_SCRIPT["rainfall_amount"]="2d_var"

#################
# METEO
# Surface air
#################
STANDARD_NAME["surface_air_pressure"]="surface_air_pressure"
LONG_NAME["surface_air_pressure"]="Surface Air Pressure"
VARIABLE_NAME["surface_air_pressure"]="surface_air_pressure"
CANONICAL_UNITS["surface_air_pressure"]="Pa"
GMT_SCRIPT["surface_air_pressure"]="2d_var"

STANDARD_NAME["wind_stress"]="wind_stress"
LONG_NAME["wind_stress"]="Wind Stress"
VARIABLE_NAME["eastward_wind_stress"]="u_wind_stress"
VARIABLE_NAME["northward_wind_stress"]="v_wind_stress"
CANONICAL_UNITS["wind_stress"]="W m2"
GMT_SCRIPT["wind_stress"]="2d_var"

STANDARD_NAME["surface_downward_sensible_heat_flux"]="surface_downward_sensible_heat_flux"
LONG_NAME["surface_downward_sensible_heat_flux"]="Surface Downward Sensible Heat Flux"
VARIABLE_NAME["surface_downward_sensible_heat_flux"]="surface_downward_sensible_heat_flux"
CANONICAL_UNITS["surface_downward_sensible_heat_flux"]="W m2"
GMT_SCRIPT["surface_downward_sensible_heat_flux"]="2d_var"

STANDARD_NAME["surface_downward_latent_heat_flux"]="surface_downward_latent_heat_flux"
LONG_NAME["surface_downward_latent_heat_flux"]="Surface Downward Latent Heat Flux"
VARIABLE_NAME["surface_downward_latent_heat_flux"]="surface_downward_latent_heat_flux"
CANONICAL_UNITS["surface_downward_latent_heat_flux"]="W m2"
GMT_SCRIPT["surface_downward_latent_heat_flux"]="2d_var"

STANDARD_NAME["surface_air_temperature"]="surface_air_temperature"
LONG_NAME["surface_air_temperature"]="Surface Air Temperature"
VARIABLE_NAME["surface_air_temperature"]="surface_air_temperature"
CANONICAL_UNITS["surface_air_temperature"]="W m2"
GMT_SCRIPT["surface_air_temperature"]="2d_var"

STANDARD_NAME["dew_point_temperature"]="dew_point_temperature"
LONG_NAME["dew_point_temperature"]="Dew Point Temperature"
VARIABLE_NAME["dew_point_temperature"]="dew_point_temperature"
CANONICAL_UNITS["dew_point_temperature"]="K"
GMT_SCRIPT["dew_point_temperature"]="2d_var"

STANDARD_NAME["surface_downwards_solar_radiation"]="surface_downwards_solar_radiation"
LONG_NAME["surface_downwards_solar_radiation"]="Surface Downwards Solar Radiation"
VARIABLE_NAME["surface_downwards_solar_radiation"]="surface_downwards_solar_radiation"
CANONICAL_UNITS["surface_downwards_solar_radiation"]="W m2"
GMT_SCRIPT["surface_downwards_solar_radiation"]="2d_var"

STANDARD_NAME["surface_downwards_thermal_radiation"]="surface_downwards_thermal_radiation"
LONG_NAME["surface_downwards_thermal_radiation"]="Surface Downwards Thermal Radiation"
VARIABLE_NAME["surface_downwards_thermal_radiation"]="surface_downwards_thermal_radiation"
CANONICAL_UNITS["surface_downwards_thermal_radiation"]="W m2"
GMT_SCRIPT["surface_downwards_thermal_radiation"]="2d_var"

STANDARD_NAME["surface_solar_radiation"]="surface_solar_radiation"
LONG_NAME["surface_solar_radiation"]="Surface Solar Radiation"
VARIABLE_NAME["surface_solar_radiation"]="surface_solar_radiation"
CANONICAL_UNITS["surface_solar_radiation"]="W m2"
GMT_SCRIPT["surface_solar_radiation"]="2d_var"

STANDARD_NAME["surface_thermal_radiation"]="surface_thermal_radiation"
LONG_NAME["surface_thermal_radiation"]="Surface Thermal Radiation"
VARIABLE_NAME["surface_thermal_radiation"]="surface_thermal_radiation"
CANONICAL_UNITS["surface_thermal_radiation"]="W m2"
GMT_SCRIPT["surface_thermal_radiation"]="2d_var"

#################
# METEO
# At 10 m
#################
STANDARD_NAME["wind_10m"]="wind_10m"
LONG_NAME["wind_10m"]="Wind 10m"
VARIABLE_NAME["eastward_wind_10m"]="u_wind_10m"
VARIABLE_NAME["northward_wind_10m"]="v_wind_10m"
CANONICAL_UNITS["wind_10m"]="m s-1"
GMT_SCRIPT["wind_10m"]="vector_var"

STANDARD_NAME["wind_speed_to_direction_10m"]="wind_speed_to_direction_10m"
LONG_NAME["wind_speed_to_direction_10m"]="Wind Speed 10m To Direction"
VARIABLE_NAME["wind_speed_to_direction_10m"]="wind_speed_10m"
VARIABLE_NAME["dir_wind_speed_to_direction_10m"]="wind_to_dir_10m"
CANONICAL_UNITS["wind_speed_to_direction_10m"]="m s-1"
GMT_SCRIPT["wind_speed_to_direction_10m"]="dir_var"

STANDARD_NAME["wind_speed_from_direction_10m"]="wind_speed_from_direction_10m"
LONG_NAME["wind_speed_from_direction_10m"]="Wind Speed 10m From Direction"
VARIABLE_NAME["wind_speed_from_direction_10m"]="wind_speed_10m"
VARIABLE_NAME["dir_wind_speed_from_direction_10m"]="wind_from_dir_10m"
CANONICAL_UNITS["wind_speed_from_direction_10m"]="m s-1"
GMT_SCRIPT["wind_speed_from_direction_10m"]="dir_var"

