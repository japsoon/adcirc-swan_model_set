# Input  : ERA5.nc file with surface pressure and wind data (U10 V10)
# Output : fort.221.nc and fort.222.nc
# -*- coding: utf-8 -*-

import os
import datetime
import numpy as np
import netCDF4 as nc

# open ERA5 file
era     = nc.Dataset( 'adaptor.mars.internal-1693468947.7287068-16430-18-735891c8-0021-49d8-b2e6-7836dea7b67a.nc' )
# read data
tim_era = np.array(era[ 'time' ][:])
lon_era = np.array(era[ 'longitude' ][:])
lat_era = np.array(era[ 'latitude' ][:])
u10_era = np.array(era[ 'u10' ][:,:,:])
v10_era = np.array(era[ 'v10' ][:,:,:])
sp_era  = np.array(era[ 'sp' ][:,:,:])
# close file
era.close()

# determine dimensions
num_lon = np.shape(lon_era)[0]
num_lat = np.shape(lat_era)[0]
num_tim = np.shape(tim_era)[0]

# create fort.221.nc file
owi = nc.Dataset('fort.221.nc', 'w', format="NETCDF4")
# assign dimensions
tim_owi_dim = owi.createDimension( 'time'      , num_tim )
lon_owi_dim = owi.createDimension( 'longitude' , num_lon )
lat_owi_dim = owi.createDimension( 'latitude'  , num_lat )

## -------------------- time ---------------------- ##

tim_owi = owi.createVariable('time' , np.int64 , ('time',))

tim_owi.long_name = 'time'
tim_owi.calendar  = 'gregorian'
tim_owi.units     = 'hours since 1900-01-01 00:00:00.0'

tim_owi[:]        = tim_era

## -------------------- lat ----------------------- ##

lat_owi = owi.createVariable( 'latitude' , np.float64 , ('latitude','longitude') )

lat_owi.long_name   = "latitude"
lat_owi.units       = "degrees_north"
lat_owi.coordinates = "latitude longitude"

# write to new file
lat_era = np.tile( np.atleast_2d(lat_era).T , (1,num_lon) )
lat_owi[:,:] = lat_era

## -------------------- lon ----------------------- ##

lon_owi = owi.createVariable( 'longitude' , np.float64 , ('latitude','longitude') )

lon_owi.long_name   = "longitude"
lon_owi.units       = "degrees_east"
lon_owi.coordinates = "latitude longitude"

# write to new file
lon_era = np.tile( lon_era , (num_lat,1) )
lon_owi[:,:] = lon_era

## --------------------- sp ----------------------- ##

sp_owi = owi.createVariable( 'sp' , np.float32 , ('time','latitude','longitude'))

sp_owi.units         = "Pa"
sp_owi.missing_value = -32767
sp_owi.fill_value    = -32767
sp_owi.long_name     = "Surface pressure"
sp_owi.standard_name = "surface_air_pressure"

sp_owi[:,:,:]        = sp_era

## --------------------- U10 ----------------------- ##

u10_owi = owi.createVariable( 'u10' , np.float32 , ('time','latitude', 'longitude'))

u10_owi.missing_value = -32767
u10_owi.fill_value    = -32767
u10_owi.units         = "m s-1"
u10_owi.long_name     = "10 metre U wind component"

u10_owi[:,:,:]        = u10_era

## --------------------- V10 ------------------------ ##

v10_owi = owi.createVariable( 'v10' , np.float32 , ('time','latitude', 'longitude'))

v10_owi.missing_value = -32767
v10_owi.fill_value    = -32767
v10_owi.units         = "m s-1"
v10_owi.long_name     = "10 metre V wind component"

v10_owi[:,:,:]        = v10_era

# close fort.221.nc file
owi.close()

# copy to fort.222.nc file
os.system('copy fort.221.nc fort.222.nc')