#!/usr/bin/env python3

import ephem
import math
import sysv_ipc
import struct

TALON_SHM_KEY = 0x4e56361a
SHM_MJD_OFFSET = 0

# Site properties
SHM_LATITUDE_OFFSET = 8
SHM_LONGITUDE_OFFSET = 16
SHM_TEMPERATURE_OFFSET = 32
SHM_PRESSURE_OFFSET = 40
SHM_ELEVATION_OFFSET = 48

# Telescope properties
SHM_RA_OFFSET = 88
SHM_DEC_OFFSET = 96
SHM_TEL_STATE_OFFSET = 920
SHM_COVER_STATE_OFFSET = 976

SHM_RA_AXIS = 248
SHM_DEC_AXIS = SHM_RA_AXIS + 120
SHM_FOCUS_AXIS = SHM_RA_AXIS + 360
SHM_AXIS_CPOS = 96
SHM_AXIS_STEP = 4
SHM_AXIS_DF = 80
SHM_AXIS_POSLIM = 56
SHM_AXIS_NEGLIM = 64

def shm_read_double(data, offset):
    return struct.unpack_from('d', data.read(8, offset))[0]

def shm_read_int(data, offset):
    return struct.unpack_from('i', data.read(4, offset))[0]

data = sysv_ipc.SharedMemory(TALON_SHM_KEY)
print('mjd: {}'.format(shm_read_double(data, SHM_MJD_OFFSET)))
print('ra: {}'.format(shm_read_double(data, SHM_RA_OFFSET)))
print('dec: {}'.format(shm_read_double(data, SHM_DEC_OFFSET)))
print('tel_state: {}'.format(shm_read_int(data, SHM_TEL_STATE_OFFSET)))
print('cover_state: {}'.format(shm_read_int(data, SHM_COVER_STATE_OFFSET)))

print('ra axis:')
print('   poslim: {}'.format(shm_read_double(data, SHM_RA_AXIS + SHM_AXIS_POSLIM)))
print('   neglim: {}'.format(shm_read_double(data, SHM_RA_AXIS + SHM_AXIS_NEGLIM)))

print('dec axis:')
print('   poslim: {}'.format(shm_read_double(data, SHM_DEC_AXIS + SHM_AXIS_POSLIM)))
print('   neglim: {}'.format(shm_read_double(data, SHM_DEC_AXIS + SHM_AXIS_NEGLIM)))

print('focus axis:')
print('   cpos: {}'.format(shm_read_double(data, SHM_FOCUS_AXIS + SHM_AXIS_CPOS)))
print('   step: {}'.format(shm_read_int(data, SHM_FOCUS_AXIS + SHM_AXIS_STEP)))
print('   df: {}'.format(shm_read_double(data, SHM_FOCUS_AXIS + SHM_AXIS_DF)))
print('   poslim: {}'.format(shm_read_double(data, SHM_FOCUS_AXIS + SHM_AXIS_POSLIM)))
print('   neglim: {}'.format(shm_read_double(data, SHM_FOCUS_AXIS + SHM_AXIS_NEGLIM)))

obs = ephem.Observer()
obs.lon = shm_read_double(data, SHM_LONGITUDE_OFFSET)
obs.lat = shm_read_double(data, SHM_LATITUDE_OFFSET)
obs.elevation = shm_read_double(data, SHM_ELEVATION_OFFSET) * 6.37816e6
obs.temp = shm_read_double(data, SHM_TEMPERATURE_OFFSET)
obs.pressure = shm_read_double(data, SHM_PRESSURE_OFFSET)
print('sidereal time: {}'.format(float(obs.sidereal_time()) * 12 / math.pi))

